using UnrealBuildTool;

public class WorldLifecycleTarget : TargetRules
{
    public WorldLifecycleTarget(TargetInfo target) : base(target)
    {
        Type = TargetType.Game;
        DefaultBuildSettings = BuildSettingsVersion.V7;
        IncludeOrderVersion = EngineIncludeOrderVersion.Unreal5_8;
        ExtraModuleNames.Add("WorldLifecycle");
    }
}
