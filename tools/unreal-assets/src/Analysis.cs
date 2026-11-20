using Newtonsoft.Json.Linq;
using UAssetAPI;
using UAssetAPI.ExportTypes;
using UAssetAPI.PropertyTypes.Objects;

namespace OneStep.UnrealAssets;

internal sealed record PropertyProjection(JArray Values, JArray References, long OpaqueBytes, string Status, JArray? Rows = null);

internal static class Analysis
{
    // A new family needs a small rule, not another binary parser. Exact class names avoid
    // guessing from filenames or unrelated imported asset classes.
    private static readonly (string Family, string[] Classes, string[] Focus)[] Families =
    [
        ("widget", ["/Script/UMGEditor.WidgetBlueprint", "/Script/UMG.WidgetBlueprintGeneratedClass"], ["WidgetTree", "Bindings", "Animations"]),
        ("montage", ["/Script/Engine.AnimMontage"], ["SlotAnimTracks", "CompositeSections", "Notifies", "BlendIn", "BlendOut"]),
        ("animation", ["/Script/Engine.AnimSequence", "/Script/Engine.AnimSequenceBase", "/Script/Engine.AnimComposite", "/Script/Engine.AnimBlueprint", "/Script/Engine.AnimBlueprintGeneratedClass", "/Script/Engine.BlendSpace", "/Script/Engine.BlendSpace1D", "/Script/Engine.AimOffsetBlendSpace", "/Script/Engine.AimOffsetBlendSpace1D"], ["Skeleton", "Notifies", "SequenceLength", "RateScale", "RawCurveData"]),
        ("data", ["/Script/Engine.DataTable", "/Script/Engine.DataAsset", "/Script/Engine.PrimaryDataAsset", "/Script/Engine.PrimaryAssetLabel", "/Script/Engine.CurveTable", "/Script/Engine.StringTable"], ["RowStruct", "Rules", "ExplicitAssets"]),
        ("blueprint", ["/Script/Engine.Blueprint", "/Script/Engine.BlueprintGeneratedClass"], ["ParentClass", "SimpleConstructionScript", "UbergraphPages", "FunctionGraphs", "ImplementedInterfaces"])
    ];

    public static JObject Family(UAsset asset, IndexResolver resolver)
    {
        var classes = asset.Exports.Where(x => x.OuterIndex.Index == 0)
            .Select(x => resolver.Resolve(x.ClassIndex.Index)).ToHashSet();
        foreach (var rule in Families)
            if (rule.Classes.Any(classes.Contains))
                return new JObject { ["family"] = rule.Family,
                    ["basis"] = "root export class identity", ["focus_properties"] = new JArray(rule.Focus),
                    ["semantics"] = "structure and serialized properties only" };
        return new JObject { ["family"] = "generic", ["basis"] = "no recognized root export class",
            ["focus_properties"] = new JArray(), ["semantics"] = "structure and serialized properties only" };
    }

    public static PropertyProjection Properties(UAsset asset, Export export, IndexResolver resolver, string? filter)
    {
        var values = new JArray();
        var references = new JArray();
        if (export is RawExport raw)
            return new(values, references, raw.Data?.LongLength ?? export.SerialSize, "unsupported");
        if (export is not NormalExport normal)
            return new(values, references, export.SerialSize, "unsupported");
        bool unsupported = normal.Data == null;
        JArray? rows = export is DataTableExport && filter == null ? new JArray() : null;
        if (rows != null && ((DataTableExport)export).Table?.Data == null) unsupported = true;
        var fields = (normal.Data ?? []).Select(p => (Property: p, Container: "properties"));
        if (rows != null && ((DataTableExport)export).Table?.Data is { } rowData)
            fields = fields.Concat(rowData.Select(p => (Property: (PropertyData)p, Container: "rows")));
        foreach (var (property, container) in fields)
        {
            string name = property.Name.ToString();
            if (filter != null && filter != name) continue;
            // Use only the library's outbound serializer. Never activate $type through JSON input.
            var data = JObject.Parse(asset.SerializeJsonObject(property));
            var tokens = data.DescendantsAndSelf().OfType<JObject>().ToArray();
            bool known = !tokens.Any(x => BackendType(x).Contains("Unknown", StringComparison.Ordinal) ||
                                         BackendType(x).Contains("RawProperty", StringComparison.Ordinal) ||
                                         BackendType(x).Contains("RawStruct", StringComparison.Ordinal));
            unsupported |= !known;
            var destination = container == "rows" ? rows! : values;
            destination.Add(new JObject { ["name"] = name, ["array_index"] = property.ArrayIndex,
                ["status"] = known ? "decoded" : "unsupported", ["data"] = data });
            foreach (var token in tokens)
            {
                var type = BackendType(token);
                var locator = container + "/" + name + ":" + token.Path;
                if (type is "ObjectPropertyData" or "ClassPropertyData" or "WeakObjectPropertyData" or "InterfacePropertyData")
                {
                    if (token["Value"]?.Type != JTokenType.Integer) continue;
                    int index = token.Value<int>("Value");
                    references.Add(new JObject { ["kind"] = "object_index", ["index"] = index,
                        ["target"] = resolver.Resolve(index), ["locator"] = locator });
                }
                else if (type == "FDelegate" && token["Object"]?.Type == JTokenType.Integer)
                {
                    int index = token.Value<int>("Object");
                    references.Add(new JObject { ["kind"] = "delegate", ["index"] = index,
                        ["target"] = resolver.Resolve(index), ["function"] = token["Delegate"]?.DeepClone(),
                        ["locator"] = locator });
                }
                else if (type is "AssetObjectPropertyData" or "AssetClassPropertyData")
                    references.Add(new JObject { ["kind"] = "soft_object", ["value"] = token["Value"]?.DeepClone(),
                        ["locator"] = locator, ["resolution"] = "not_followed" });
                else if (type == "FSoftObjectPath")
                    // Use the typed payload once, covering SoftClassPath/legacy subclasses too.
                    references.Add(new JObject { ["kind"] = "soft_object", ["value"] = token.DeepClone(),
                        ["locator"] = locator, ["resolution"] = "not_followed" });
            }
        }
        long opaque = export.Extras?.LongLength ?? 0;
        return new(values, references, opaque, unsupported || opaque > 0 ? "partial" : "decoded", rows);
    }

    private static string BackendType(JObject value) =>
        (value.Value<string>("$type") ?? "").Split(',')[0].Split('.').Last();
}
