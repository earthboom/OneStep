using System.Diagnostics;
using System.Security.Cryptography;
using Newtonsoft.Json.Linq;
using UAssetAPI;
using UAssetAPI.ExportTypes;
using UAssetAPI.UnrealTypes;

namespace OneStep.UnrealAssets;

internal static class AssetReader
{
    private const long MaxBytes = 256L * 1024 * 1024;

    public static JObject Read(Options options)
    {
        var timer = Stopwatch.StartNew();
        if (!string.Equals(System.IO.Path.GetExtension(options.Path), ".uasset", StringComparison.OrdinalIgnoreCase))
            throw new ReaderException("input", "Only single-file uncooked .uasset packages are supported.");
        // FileShare.Read prevents concurrent writes on Windows. The library sees no file path and
        // receives only this snapshot; it cannot auto-load adjacent exports or dependency assets.
        byte[] bytes;
        using (var input = new FileStream(options.Path, FileMode.Open, FileAccess.Read, FileShare.Read))
        {
            if (input.Length < 32 || input.Length > MaxBytes)
                throw new ReaderException("input_size", "Input must be between 32 bytes and 256 MiB.");
            bytes = new byte[(int)input.Length];
            input.ReadExactly(bytes);
        }
        if (!bytes.AsSpan(0, 4).SequenceEqual(new byte[] { 0xC1, 0x83, 0x2A, 0x9E }))
            throw new ReaderException("package_signature", "Not a supported little-endian Unreal package.");

        var flags = CustomSerializationFlags.SkipPreloadDependencyLoading |
                    CustomSerializationFlags.SkipParsingBytecode | CustomSerializationFlags.SkipLoadingExports;
        var asset = new UAsset(options.Engine, customSerializationFlags: flags);
        using var stream = new ExportBoundedStream(bytes);
        using var reader = new StrictAssetBinaryReader(stream, asset);
        try { asset.Read(reader); }
        catch (Exception) when (Unsupported(asset))
        {
            // A stripped/split package may fail while the library reads later header sections.
            // Its already-read flags still explain why this tool cannot accept that package.
            throw new ReaderException("unsupported_package", "Cooked, editor-stripped or unversioned package.");
        }
        if (Unsupported(asset))
            throw new ReaderException("unsupported_package",
                "Cooked, editor-stripped or unversioned packages are outside the initial reader scope.");

        // Reject body ranges outside the one supplied file, including split .uexp payloads.
        foreach (var export in asset.Exports)
            if (export.SerialOffset < 0 || export.SerialSize < 0 ||
                export.SerialOffset > bytes.LongLength || export.SerialSize > bytes.LongLength - export.SerialOffset)
                throw new ReaderException("export_range", "An export is truncated or needs an external payload.");

        var resolver = new IndexResolver(asset);
        var selected = Enumerable.Range(0, asset.Exports.Count).ToArray();
        if (options.Object != null)
        {
            selected = selected.Where(i => asset.Exports[i].ObjectName.ToString() == options.Object ||
                resolver.Resolve(i + 1) == options.Object).ToArray();
            if (selected.Length != 1)
                throw new ReaderException("object_selection", "Object selector must match exactly one export; use its full path.");
        }
        var objects = new JArray();
        bool partial = false, foundProperty = options.Property == null;
        foreach (int index in selected)
        {
            if (options.Properties)
            {
                var declared = asset.Exports[index];
                stream.SetExportRange(declared.SerialOffset, declared.SerialSize);
                asset.CustomSerializationFlags = flags & ~CustomSerializationFlags.SkipLoadingExports;
                if (asset.ObjectVersionUE5 >= ObjectVersionUE5.SCRIPT_SERIALIZATION_OFFSET &&
                    declared.ScriptSerializationStartOffset > 0 &&
                    resolver.Name(declared.ClassIndex.Index)?.EndsWith("ImportData", StringComparison.Ordinal) == true)
                {
                    // ImportData subclasses serialize source JSON before their UObject tags.
                    // Use the package's declared tag range rather than guessing from that prefix.
                    asset.Exports[index] = ReadPrefixedImportData(reader, declared, bytes);
                }
                else asset.ParseExport(reader, index, true);
                if (stream.RangeViolation)
                    throw new ReaderException("export_range", "Export parsing attempted to cross its declared byte range.");
            }
            var export = asset.Exports[index];
            var item = new JObject
            {
                ["index"] = index + 1,
                ["name"] = export.ObjectName.ToString(),
                ["path"] = resolver.Resolve(index + 1),
                ["class_name"] = resolver.Name(export.ClassIndex.Index),
                ["class_path"] = resolver.Resolve(export.ClassIndex.Index),
                ["outer_index"] = export.OuterIndex.Index,
                ["super_index"] = export.SuperIndex.Index,
                ["template_index"] = export.TemplateIndex.Index,
                ["serial_offset"] = export.SerialOffset,
                ["serial_size"] = export.SerialSize,
                ["is_asset"] = export.bIsAsset,
                ["property_status"] = "not_requested"
            };
            if (options.Properties)
            {
                var projection = Analysis.Properties(asset, export, resolver, options.Property);
                item["properties"] = projection.Values;
                if (projection.Rows != null) item["rows"] = projection.Rows;
                item["references"] = projection.References;
                item["opaque_bytes"] = projection.OpaqueBytes;
                item["property_status"] = projection.Status;
                item["backend_export_type"] = export.GetType().Name;
                partial |= projection.Status != "decoded";
                foundProperty |= projection.Values.Count > 0;
            }
            objects.Add(item);
        }
        if (!foundProperty)
            throw new ReaderException("property_selection", "No selected export contains that decoded top-level property.");

        var imports = new JArray(asset.Imports.Select((entry, i) => new JObject
        {
            ["index"] = -(i + 1), ["name"] = entry.ObjectName.ToString(),
            ["path"] = resolver.Resolve(-(i + 1)), ["class_name"] = entry.ClassName.ToString(),
            ["outer_index"] = entry.OuterIndex.Index
        }));
        var limitations = new JArray(
            "Serialized facts only; no effective inherited defaults or runtime behavior are inferred.",
            "Import catalogue and decoded property references are not a transitive dependency closure.",
            "Bytecode, graph semantics, animation tracks and rendered appearance are not interpreted.",
            "Specialized native fields other than decoded DataTable rows are not projected.");
        if (partial) limitations.Add("Some selected export/property data or native trailing bytes remain opaque.");
        var report = new JObject
        {
            ["schema_version"] = 1, ["status"] = partial ? "partial" : "complete",
            ["scope"] = options.Properties ? "serialized_properties" : "structure",
            ["backend"] = new JObject { ["name"] = "UAssetAPI", ["version"] = "1.1.0" },
            ["input"] = new JObject { ["name"] = System.IO.Path.GetFileName(options.Path),
                ["bytes"] = bytes.LongLength, ["sha256"] = Convert.ToHexString(SHA256.HashData(bytes)).ToLowerInvariant() },
            ["package"] = new JObject
            {
                ["engine_selection"] = options.Engine.ToString(),
                ["saved_by_engine"] = $"{asset.RecordedEngineVersion.Major}.{asset.RecordedEngineVersion.Minor}.{asset.RecordedEngineVersion.Patch}",
                ["object_version"] = (int)asset.ObjectVersion,
                ["object_version_ue5"] = (int)asset.ObjectVersionUE5,
                ["flags"] = asset.PackageFlags.ToString(),
                ["export_count"] = asset.Exports.Count, ["import_count"] = asset.Imports.Count,
                ["selected_export_count"] = objects.Count
            },
            ["analysis"] = Analysis.Family(asset, resolver),
            ["objects"] = objects, ["imports"] = imports,
            ["soft_package_references"] = new JArray(asset.SoftPackageReferenceList?.Select(x => x.ToString()) ?? []),
            ["limitations"] = limitations
        };
        timer.Stop();
        report["inspection_elapsed_ms"] = Math.Round(timer.Elapsed.TotalMilliseconds, 3);
        return report;
    }

    private static bool Unsupported(UAsset asset) => asset.PackageFlags.HasFlag(EPackageFlags.PKG_Cooked) ||
        asset.IsFilterEditorOnly || asset.HasUnversionedProperties || asset.IsUnversioned;

    private static NormalExport ReadPrefixedImportData(AssetBinaryReader reader, Export declared, byte[] bytes)
    {
        long start = declared.ScriptSerializationStartOffset, end = declared.ScriptSerializationEndOffset;
        if (start < 0 || end <= start || end > declared.SerialSize)
            throw new ReaderException("script_range", "Invalid declared import-data property range.");
        var normal = declared.ConvertToChildExport<NormalExport>();
        reader.BaseStream.Position = declared.SerialOffset + start;
        normal.Read(reader, checked((int)(declared.SerialOffset + declared.SerialSize)));
        long guidBytes = declared.ObjectFlags.HasFlag(EObjectFlags.RF_ClassDefaultObject) ? 0 :
            normal.ObjectGuid.HasValue ? 20 : 4;
        if (reader.BaseStream.Position != declared.SerialOffset + end + guidBytes)
            throw new ReaderException("script_range", "Import-data properties did not consume their declared tag range exactly.");
        long suffixStart = reader.BaseStream.Position;
        int suffixBytes = checked((int)(declared.SerialOffset + declared.SerialSize - suffixStart));
        normal.Extras = new byte[checked((int)start + suffixBytes)];
        bytes.AsSpan((int)declared.SerialOffset, (int)start).CopyTo(normal.Extras);
        bytes.AsSpan((int)suffixStart, suffixBytes).CopyTo(normal.Extras.AsSpan((int)start));
        return normal;
    }
}

internal sealed class ExportBoundedStream(byte[] bytes) : MemoryStream(bytes, writable: false)
{
    private long? rangeStart;
    private long rangeEnd;
    public bool RangeViolation { get; private set; }

    public void SetExportRange(long offset, long size)
    {
        rangeStart = offset;
        rangeEnd = checked(offset + size);
        RangeViolation = false;
        base.Position = offset;
    }

    private void CheckPosition(long position)
    {
        if (rangeStart is { } start && (position < start || position > rangeEnd))
        {
            RangeViolation = true;
            throw new ReaderException("export_range", "Seek exceeds the declared export range.");
        }
    }

    private void CheckRead(int count)
    {
        CheckPosition(base.Position);
        if (rangeStart != null && count > rangeEnd - base.Position)
        {
            RangeViolation = true;
            throw new ReaderException("export_range", "Read exceeds the declared export range.");
        }
    }

    public override long Position { get => base.Position; set { CheckPosition(value); base.Position = value; } }
    public override long Seek(long offset, SeekOrigin origin)
    {
        long position = base.Seek(offset, origin);
        CheckPosition(position);
        return position;
    }
    public override int Read(byte[] buffer, int offset, int count)
    {
        CheckRead(count);
        return base.Read(buffer, offset, count);
    }
    public override int Read(Span<byte> buffer) { CheckRead(buffer.Length); return base.Read(buffer); }
    public override int ReadByte() { CheckRead(1); return base.ReadByte(); }
}

internal sealed class StrictAssetBinaryReader(Stream stream, UAsset asset) : AssetBinaryReader(stream, asset)
{
    public override FName ReadFName()
    {
        int index = ReadInt32();
        int number = ReadInt32();
        // UAssetAPI otherwise renders an out-of-range index as a numeric string.
        if (index < 0 || index >= Asset.GetNameMapIndexList().Count || number < 0)
            throw new ReaderException("name_index", "Serialized name is outside the package name map.");
        return new FName(Asset, index, number);
    }
}

internal sealed class IndexResolver(UAsset asset)
{
    public string? Name(int index) => index == 0 ? null : index > 0
        ? asset.Exports[Checked(index - 1, asset.Exports.Count)].ObjectName.ToString()
        : asset.Imports[Checked(-(long)index - 1, asset.Imports.Count)].ObjectName.ToString();

    public string? Resolve(int index)
    {
        if (index == 0) return null;
        var names = new List<string>();
        var seen = new HashSet<int>();
        while (index != 0)
        {
            if (!seen.Add(index)) throw new ReaderException("object_index", "Cycle in object outer indices.");
            names.Add(Name(index)!);
            index = index > 0 ? asset.Exports[Checked(index - 1, asset.Exports.Count)].OuterIndex.Index
                             : asset.Imports[Checked(-(long)index - 1, asset.Imports.Count)].OuterIndex.Index;
        }
        names.Reverse();
        return string.Join('.', names);
    }

    private static int Checked(long index, int count) => index >= 0 && index < count ? (int)index
        : throw new ReaderException("object_index", "Object reference is outside the import/export tables.");
}
