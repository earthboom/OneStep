using UnrealBuildTool;
public class AssetCheckEditorTarget : TargetRules
{
    public AssetCheckEditorTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Editor;
        DefaultBuildSettings = BuildSettingsVersion.Latest;
        IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
        ExtraModuleNames.Add("AssetCheck");
    }
}
