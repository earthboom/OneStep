using UAssetAPI.UnrealTypes;

namespace OneStep.UnrealAssets;

internal sealed class ReaderException(string code, string message) : Exception(message)
{
    public string Code { get; } = code;
}

internal sealed record Options(string Path, EngineVersion Engine, bool Properties,
    string? Object, string? Property, bool Pretty, bool Help = false)
{
    public const string Usage = """
        OneStep read-only uncooked asset reader
        Usage: dotnet OneStep.UnrealAssets.dll FILE.uasset [options]
          --engine 4.27|5.7   Explicit library engine version; otherwise use package versions
          --properties        Decode serialized properties (default: structure only)
          --object NAME|PATH  Select one export by exact name or outer-qualified path
          --property NAME     Select a top-level property; implies --properties
          --pretty            Indent JSON
          --help              Show this help
        Exit: 0 requested scope complete, 1 partial decoding, 2 invalid/unsupported/failed.
        Does not write assets, follow dependencies, interpret bytecode or decode animation tracks.
        """;

    public static Options Parse(string[] args)
    {
        if (args.Length == 1 && args[0] == "--help")
            return new("", EngineVersion.UNKNOWN, false, null, null, false, true);
        if (args.Length == 0 || args[0].StartsWith("--"))
            throw new ReaderException("arguments", "Supply exactly one .uasset input; use --help.");
        string? engineText = null, selector = null, property = null;
        bool properties = false, pretty = false;
        var seen = new HashSet<string>(StringComparer.Ordinal);
        for (int i = 1; i < args.Length; i++)
        {
            var option = args[i];
            if (!seen.Add(option)) throw new ReaderException("arguments", $"Duplicate option: {option}");
            if (option == "--properties") { properties = true; continue; }
            if (option == "--pretty") { pretty = true; continue; }
            if (option is not ("--engine" or "--object" or "--property"))
                throw new ReaderException("arguments", $"Unknown option: {option}");
            if (++i >= args.Length || string.IsNullOrWhiteSpace(args[i]) || args[i].StartsWith("--"))
                throw new ReaderException("arguments", $"Missing value for {option}");
            if (option == "--engine") engineText = args[i];
            if (option == "--object") selector = args[i];
            if (option == "--property") { property = args[i]; properties = true; }
        }
        var engine = EngineVersion.UNKNOWN;
        if (engineText != null)
        {
            // Numeric Enum.Parse input and AUTOMATIC aliases must not silently select a version.
            string name = "VER_UE" + engineText.Replace('.', '_');
            if (!System.Text.RegularExpressions.Regex.IsMatch(engineText, @"^[45]\.\d{1,2}(EA)?$") ||
                !Enum.TryParse(name, out engine) || !Enum.IsDefined(engine))
                throw new ReaderException("engine_version", $"Unsupported engine selection: {engineText}");
        }
        return new(args[0], engine, properties, selector, property, pretty);
    }
}
