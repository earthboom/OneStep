using UnrealBuildTool;

public class PulseArenaTarget : TargetRules
{
    public PulseArenaTarget(TargetInfo target) : base(target)
    {
        Type = TargetType.Game;
        DefaultBuildSettings = BuildSettingsVersion.V7;
        IncludeOrderVersion = EngineIncludeOrderVersion.Unreal5_8;
        ExtraModuleNames.Add("PulseArena");
    }
}
