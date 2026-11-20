// TEST ONLY: derived routing fixtures, not engine-authored animation/widget fidelity evidence.
using UAssetAPI;
using UAssetAPI.ExportTypes;
using UAssetAPI.PropertyTypes.Objects;
using UAssetAPI.PropertyTypes.Structs;
using UAssetAPI.UnrealTypes;

var input = args[0];
var output = args[1];
Directory.CreateDirectory(output);
foreach (var (kind, type) in new[] { ("animation", "AnimSequence"), ("montage", "AnimMontage"),
    ("data", "DataAsset"), ("widget", "WidgetBlueprint"), ("table", "DataTable"), ("spoof", "DataAsset"), ("ambiguous", "DataAsset") })
{
    var asset = new UAsset(input, EngineVersion.VER_UE4_27,
        customSerializationFlags: CustomSerializationFlags.SkipPreloadDependencyLoading);
    asset.Imports.Single(x => x.ObjectName.ToString() == "SoundClass").ObjectName = new FName(asset, type);
    if (kind is "widget" or "spoof")
        asset.Imports.Single(x => x.ObjectName.ToString() == "/Script/Engine").ObjectName =
            new FName(asset, kind == "widget" ? "/Script/UMGEditor" : "/Game/NotAnEngineClass");
    var target = asset.Exports.OfType<NormalExport>().Single(x => x.ObjectName.ToString() == "TestSoundClass");
    target.Data.Add(new TextPropertyData(new FName(asset, "FixtureText"))
        { Namespace = new FString("Legacy"), Value = new FString("Key37"), CultureInvariantString = new FString("Legacy text 37") });
    target.Data.Add(new IntPropertyData(new FName(asset, "FixtureValue")) { Value = 37 });
    target.Data.Add(new InterfacePropertyData(new FName(asset, "FixtureInterface"))
        { Value = new FPackageIndex(asset.Exports.IndexOf(target) + 1) });
    target.Data.Add(new DelegatePropertyData(new FName(asset, "FixtureDelegate"))
        { Value = new FDelegate(new FPackageIndex(asset.Exports.IndexOf(target) + 1), new FName(asset, "FixtureCallback")) });
    foreach (var structName in new[] { "SoftClassPath", "SoftAssetPath", "StringAssetReference", "StringClassReference" })
    {
        var propertyType = typeof(UAsset).Assembly.GetType("UAssetAPI.PropertyTypes.Structs." + structName + "PropertyData")!;
        var value = (SoftObjectPathPropertyData)Activator.CreateInstance(propertyType, new FName(asset, "Fixture" + structName))!;
        value.Value = new FSoftObjectPath(null, new FName(asset, "/Game/Example.Example_C"), new FString(""));
        target.Data.Add(new StructPropertyData(new FName(asset, "Fixture" + structName))
            { StructType = new FName(asset, structName), Value = [value] });
    }
    asset.AddNameReference(new FString("StructProperty"));
    foreach (var propertyType in new[] { "TextProperty", "IntProperty", "InterfaceProperty", "DelegateProperty" })
        asset.AddNameReference(new FString(propertyType));
    if (kind == "table")
    {
        var row = new StructPropertyData(new FName(asset, "Alpha"))
        {
            StructType = FName.DefineDummy(asset, "Generic"),
            Value = new List<PropertyData> { new IntPropertyData(new FName(asset, "Damage")) { Value = 42 } }
        };
        var table = target.ConvertToChildExport<DataTableExport>();
        table.Data = target.Data;
        table.Table = new UDataTable([row]);
        asset.Exports[asset.Exports.IndexOf(target)] = table;
    }
    if (kind == "ambiguous")
    {
        foreach (int outer in new[] { 0, asset.Exports.IndexOf(target) + 1 })
        {
            var duplicate = target.ConvertToChildExport<NormalExport>();
            duplicate.Data = target.Data;
            duplicate.ObjectName = new FName(asset, "Duplicate");
            duplicate.OuterIndex = new FPackageIndex(outer);
            duplicate.bIsAsset = false;
            asset.Exports.Add(duplicate);
        }
    }
    asset.Write(Path.Combine(output, kind + ".uasset"));
}
