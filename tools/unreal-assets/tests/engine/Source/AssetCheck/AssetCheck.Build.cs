using UnrealBuildTool;
public class AssetCheck : ModuleRules
{
    public AssetCheck(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
        PublicDependencyModuleNames.AddRange(new[] {"Core", "CoreUObject", "Engine"});
        PrivateDependencyModuleNames.AddRange(new[] {"UnrealEd", "UMG", "UMGEditor", "SlateCore"});
    }
}
