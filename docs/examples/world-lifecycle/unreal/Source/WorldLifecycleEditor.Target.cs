using UnrealBuildTool;

public class WorldLifecycleEditorTarget : TargetRules
{
    public WorldLifecycleEditorTarget(TargetInfo target) : base(target)
    {
        Type = TargetType.Editor;
        DefaultBuildSettings = BuildSettingsVersion.V7;
        IncludeOrderVersion = EngineIncludeOrderVersion.Unreal5_8;
        ExtraModuleNames.Add("WorldLifecycle");
    }
}
