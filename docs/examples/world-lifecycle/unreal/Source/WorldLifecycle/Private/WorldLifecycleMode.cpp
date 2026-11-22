#include "WorldLifecycleMode.h"

#include "Engine/Level.h"
#include "Engine/LevelStreamingDynamic.h"
#include "Engine/World.h"
#include "EngineUtils.h"
#include "HAL/FileManager.h"
#include "HAL/PlatformMisc.h"
#include "HAL/PlatformTime.h"
#include "Misc/CommandLine.h"
#include "Misc/Parse.h"
#include "Misc/Paths.h"
#include "WolfPresentationComponent.h"
#include "WorldLifecyclePlayer.h"
#include "WorldScaleRun.h"

DEFINE_LOG_CATEGORY(LogWorldLifecycle);

namespace
{
constexpr const TCHAR* ForestPackage = TEXT("/Game/Maps/Forest");
constexpr double PatrolInterval = 0.25;
}

AWorldLifecycleMode::AWorldLifecycleMode()
{
    PrimaryActorTick.bCanEverTick = true;
    PlayerControllerClass = AWorldLifecyclePlayer::StaticClass();
    HUDClass = AWorldLifecycleHUD::StaticClass();
    DefaultPawnClass = nullptr;
    bStartPlayersAsSpectators = true;
    SpectatorClass = nullptr;
}

void AWorldLifecycleMode::BeginPlay()
{
    Super::BeginPlay();
    UE_LOG(LogWorldLifecycle, Display, TEXT("session game=%d standalone=%d map=%s"),
        GetWorld()->WorldType == EWorldType::Game, GetNetMode() == NM_Standalone, *GetWorld()->GetOutermost()->GetName());

    const TCHAR* Command = FCommandLine::Get();
    if (!FParse::Value(Command, TEXT("WorldSave="), SlotPath))
    {
        SlotPath = FPaths::Combine(FPaths::ProjectSavedDir(), TEXT("WorldLifecycle/Slot.json"));
    }
    FString LegacyPath;
    if (!FParse::Value(Command, TEXT("LegacyFixture="), LegacyPath))
    {
        LegacyPath = FPaths::Combine(FPaths::ProjectDir(), TEXT("../fixtures/legacy-v1.json"));
    }
    FString ScaleMode;
    if (FParse::Value(Command, TEXT("WorldScale="), ScaleMode))
    {
        FString Output;
        FString Save;
        FParse::Value(Command, TEXT("ScaleOutput="), Output);
        FParse::Value(Command, TEXT("ScaleSave="), Save);
        AWorldScaleRun* Scale = GetWorld()->SpawnActor<AWorldScaleRun>();
        if (!Scale || !Scale->Start(ScaleMode, LegacyPath, Output, Save))
        {
            FPlatformMisc::RequestExitWithStatus(false, 1, TEXT("World scale setup failed"));
        }
        return;
    }
    FString Error;
    const FString& Source = IFileManager::Get().FileExists(*SlotPath) ? SlotPath : LegacyPath;
    bReady = RestoreFrom(Source, Error);
    Status = bReady ? TEXT("Take the road into the forest.") : FString::Printf(TEXT("Could not read save (%s)."), *Error);
    if (!bReady)
    {
        UE_LOG(LogWorldLifecycle, Error, TEXT("Initial load failed path=%s reason=%s"), *Source, *Error);
    }
    UpdateCamera();
}

bool AWorldLifecycleMode::RestoreFrom(const FString& Path, FString& Error)
{
    int32 Schema = 0;
    if (!ReadWorldNpc(Path, State, Schema, Error))
    {
        UE_LOG(LogWorldLifecycle, Display, TEXT("rejected reason=%s npc=%s hp=%d quest=%d patrol=%d"),
            *Error, FWorldNpcState::Id, State.Hp, State.QuestStage, State.PatrolSteps);
        return false;
    }
    if (UWolfPresentationComponent* Projection = WolfView.Get(); IsPresentationActive())
    {
        Projection->Project(State);
    }
    UE_LOG(LogWorldLifecycle, Display, TEXT("restore schema=%d npc=%s hp=%d quest=%d patrol=%d"),
        Schema, FWorldNpcState::Id, State.Hp, State.QuestStage, State.PatrolSteps);
    return true;
}

void AWorldLifecycleMode::SaveSlot()
{
    if (!bReady)
    {
        return;
    }
    bSaved = WriteWorldNpc(SlotPath, State);
    Status = bSaved ? TEXT("Journey saved.") : TEXT("Could not save the journey.");
    if (bSaved)
    {
        UE_LOG(LogWorldLifecycle, Display, TEXT("save schema=2 npc=%s hp=%d quest=%d patrol=%d"),
            FWorldNpcState::Id, State.Hp, State.QuestStage, State.PatrolSteps);
    }
}

void AWorldLifecycleMode::StartVisit()
{
    if (!bReady || Phase != EForestPhase::Town)
    {
        return;
    }
    MarkRequest();
    ULevelStreamingDynamic::FLoadLevelInstanceParams Params(GetWorld(), ForestPackage, FTransform::Identity);
    Params.LevelStreamingCreatedCallback = [](ULevelStreaming* Stream) { Stream->bShouldBlockOnLoad = false; };
    bool bAccepted = false;
    ForestStream = ULevelStreamingDynamic::LoadLevelInstance(Params, bAccepted);
    if (!bAccepted || !ForestStream)
    {
        Status = TEXT("Could not request the forest level.");
        return;
    }
    ++Visit;
    Phase = EForestPhase::Loading;
    Status = TEXT("Streaming the forest...");
    UE_LOG(LogWorldLifecycle, Display, TEXT("request visit=%d package=%s blocking=%d"),
        Visit, ForestPackage, ForestStream->bShouldBlockOnLoad);
}

void AWorldLifecycleMode::HitWolf()
{
    if (Phase != EForestPhase::Forest || State.Hp == 0 || !IsPresentationActive())
    {
        return;
    }
    State.Hp = FMath::Max(0, State.Hp - 40);
    State.QuestStage = 1;
    WolfView->Project(State);
    Status = State.Hp == 0 ? TEXT("The wolf is defeated.") : TEXT("You hit the wolf for 40.");
    UE_LOG(LogWorldLifecycle, Display, TEXT("hit npc=%s hp=%d quest=%d patrol=%d"),
        FWorldNpcState::Id, State.Hp, State.QuestStage, State.PatrolSteps);
}

void AWorldLifecycleMode::ReturnToTown()
{
    if (Phase != EForestPhase::Forest)
    {
        return;
    }
    MarkRequest();
    Phase = EForestPhase::Unloading;
    Status = TEXT("Returning to town...");
    UpdateCamera();
    ForestStream->SetShouldBeVisible(false);
    ForestStream->SetShouldBeLoaded(false);
    ForestStream->SetIsRequestingUnloadAndRemoval(true);
    UE_LOG(LogWorldLifecycle, Display, TEXT("request-out visit=%d"), Visit);
}

void AWorldLifecycleMode::Tick(float DeltaSeconds)
{
    Super::Tick(DeltaSeconds);
    if (Phase == EForestPhase::Loading || Phase == EForestPhase::Unloading)
    {
        SampleTransition();
    }

    if (Phase == EForestPhase::Loading && ForestStream->GetLevelStreamingState() == ELevelStreamingState::FailedToLoad)
    {
        Status = TEXT("The forest level failed to stream.");
        ForestStream->SetIsRequestingUnloadAndRemoval(true);
        WolfView.Reset();
        ForestStream = nullptr;
        Phase = EForestPhase::Town;
        return;
    }
    if (Phase == EForestPhase::Loading && ForestStream->IsLevelVisible())
    {
        UWolfPresentationComponent* Projection = CreateProjection();
        if (!Projection)
        {
            Status = TEXT("Forest map has no active wolf presentation.");
            Phase = EForestPhase::Forest;
            ReturnToTown();
            return;
        }
        WolfView = Projection;
        Phase = EForestPhase::Forest;
        Status = TEXT("The wolf waits by the track.");
        UpdateCamera();
        const double VisibleAt = FPlatformTime::Seconds();
        const FWorldNpcState& View = Projection->GetProjection();
        UE_LOG(LogWorldLifecycle, Display, TEXT("visible visit=%d instance=%s loaded=%d visible=%d presentation=%d actors=%d npc=%s hp=%d quest=%d patrol=%d viewHp=%d viewQuest=%d viewPatrol=%d latencyMs=%.3f maxTickGapMs=%.3f tickGaps=%d"),
            Visit, *ForestStream->GetWorldAssetPackageFName().ToString(), ForestStream->IsLevelLoaded(),
            ForestStream->IsLevelVisible(), IsPresentationActive(), ForestStream->GetLoadedLevel()->Actors.Num(),
            FWorldNpcState::Id, State.Hp, State.QuestStage, State.PatrolSteps, View.Hp, View.QuestStage,
            View.PatrolSteps, (VisibleAt - RequestedAt) * 1000.0, MaxTickGap * 1000.0, TickGaps);
        return;
    }
    const double WorldSeconds = GetWorld()->GetTimeSeconds();
    if (Phase == EForestPhase::Unloading && !ForestStream->IsLevelLoaded()
        && !GetWorld()->GetStreamingLevels().Contains(ForestStream.Get()) && !IsPresentationActive())
    {
        UE_LOG(LogWorldLifecycle, Display, TEXT("unloaded visit=%d registered=0 loaded=0 presentation=0 npc=%s hp=%d quest=%d patrol=%d worldSeconds=%.6f latencyMs=%.3f maxTickGapMs=%.3f tickGaps=%d"),
            Visit, FWorldNpcState::Id, State.Hp, State.QuestStage, State.PatrolSteps, WorldSeconds,
            (FPlatformTime::Seconds() - RequestedAt) * 1000.0, MaxTickGap * 1000.0, TickGaps);
        WolfView.Reset();
        ForestStream = nullptr;
        Phase = EForestPhase::Town;
        NextPatrolAt = WorldSeconds + PatrolInterval;
        Status = TEXT("Back in town. The wolf is still patrolling.");
        return;
    }
    if (Phase == EForestPhase::Town && Visit > 0 && State.Hp > 0 && State.PatrolSteps < MAX_int32
        && WorldSeconds >= NextPatrolAt)
    {
        NextPatrolAt = WorldSeconds + PatrolInterval;
        ++State.PatrolSteps;
        UE_LOG(LogWorldLifecycle, Display, TEXT("patrol npc=%s hp=%d quest=%d patrol=%d worldSeconds=%.6f loaded=0 presentation=0"),
            FWorldNpcState::Id, State.Hp, State.QuestStage, State.PatrolSteps, WorldSeconds);
    }
}

UWolfPresentationComponent* AWorldLifecycleMode::CreateProjection()
{
    for (AActor* Actor : ForestStream->GetLoadedLevel()->Actors)
    {
        if (!IsValid(Actor) || !Actor->ActorHasTag(TEXT("WolfPresentation")) || !Actor->HasActorBegunPlay())
        {
            continue;
        }
        UWolfPresentationComponent* Projection = NewObject<UWolfPresentationComponent>(Actor);
        Actor->AddInstanceComponent(Projection);
        Projection->RegisterComponent();
        Projection->Project(State);
        return Projection;
    }
    return nullptr;
}

bool AWorldLifecycleMode::IsPresentationActive() const
{
    const UWolfPresentationComponent* Projection = WolfView.Get();
    return Projection && Projection->IsRegistered() && Projection->GetOwner()->HasActorBegunPlay();
}

void AWorldLifecycleMode::MarkRequest()
{
    RequestedAt = PreviousSample = FPlatformTime::Seconds();
    MaxTickGap = 0.0;
    TickGaps = 0;
}

void AWorldLifecycleMode::SampleTransition()
{
    const double Now = FPlatformTime::Seconds();
    MaxTickGap = FMath::Max(MaxTickGap, Now - PreviousSample);
    PreviousSample = Now;
    ++TickGaps;
}

void AWorldLifecycleMode::UpdateCamera() const
{
    if (APlayerController* Player = GetWorld()->GetFirstPlayerController())
    {
        ApplyCamera(*Player);
    }
}

void AWorldLifecycleMode::ApplyCamera(APlayerController& Player) const
{
    const FName Tag = Phase == EForestPhase::Forest ? TEXT("ForestCamera") : TEXT("TownCamera");
    for (TActorIterator<AActor> It(GetWorld()); It; ++It)
    {
        if (It->ActorHasTag(Tag))
        {
            Player.SetViewTarget(*It);
            return;
        }
    }
}
