using Newtonsoft.Json;
using UAssetAPI;
using UAssetAPI.CustomVersions;
using UAssetAPI.PropertyTypes.Objects;
using UAssetAPI.UnrealTypes;

namespace OneStep.UnrealAssets;

// UAssetAPI discovers property subclasses in dependent assemblies and registers this
// TextProperty override after its built-in reader. Keep the upstream decoder for
// every existing history; only consume the versioned editor-only extension it lacks.
public sealed class ReadOnlyTextPropertyData : TextPropertyData
{
    [JsonProperty] public FString? DevNotes;

    public ReadOnlyTextPropertyData() { }
    public ReadOnlyTextPropertyData(FName name) : base(name) { }

    public override void Read(AssetBinaryReader reader, bool includeHeader, long leng1, long leng2 = 0,
        PropertySerializationContext serializationContext = PropertySerializationContext.Normal)
    {
        base.Read(reader, includeHeader, leng1, leng2, serializationContext);
        // Engine TextHistory.cpp: FTextHistory_Base::Serialize, AddDevNotesToFText = 260.
        // Gate on the serialized custom version, never the package's marketing version.
        if (HistoryType == TextHistoryType.Base && !reader.Asset.IsFilterEditorOnly &&
            (int)reader.Asset.GetCustomVersion<FFortniteMainBranchObjectVersion>() >= 260)
            DevNotes = reader.ReadFString();
    }
}
