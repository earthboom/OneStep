#include "WorldScaleRun.h"

#include "Camera/CameraActor.h"
#include "Components/StaticMeshComponent.h"
#include "Dom/JsonObject.h"
#include "Engine/GameViewportClient.h"
#include "Engine/Level.h"
#include "Engine/LevelStreamingDynamic.h"
#include "Engine/StaticMesh.h"
#include "Engine/StaticMeshActor.h"
#include "Engine/World.h"
#include "EngineUtils.h"
#include "GameFramework/HUD.h"
#include "GameFramework/PlayerController.h"
#include "HAL/IConsoleManager.h"
#include "HAL/PlatformMemory.h"
#include "HAL/PlatformMisc.h"
#include "HAL/PlatformTime.h"
#include "Materials/MaterialInterface.h"
#include "Misc/CoreDelegates.h"
#include "Misc/FileHelper.h"
#include "Serialization/JsonSerializer.h"
#include "Slate/SceneViewport.h"
#include "UObject/UObjectGlobals.h"
#include "WolfPresentationComponent.h"
#include "WorldLifecycleMode.h"

namespace
{
constexpr int32 RouteChunks[] = {INDEX_NONE, 0, 2, 5, INDEX_NONE, 5};
const TCHAR* RouteNames[] = {TEXT("preload"), TEXT("enter0"), TEXT("travel2"), TEXT("travel5"), TEXT("returnTown"), TEXT("reenter5")};
const TCHAR* SettleNames[] = {TEXT("town"), TEXT("chunk0"), TEXT("chunk2"), TEXT("combat"), TEXT("offscreen"), TEXT("revisit")};
constexpr double GameHz = 30.0;
constexpr int32 SegmentTicks = 24;
constexpr int32 PatrolPeriod = 8;

double CenterOf(int32 Chunk) { return 12000.0 + 6500.0 * Chunk; }

void Mix(uint64& Hash, int64 Value)
{
    Hash ^= static_cast<uint64>(Value);
    Hash *= 1099511628211ull;
}

FString Hex(uint64 Hash) { return FString::Printf(TEXT("%016llx"), static_cast<unsigned long long>(Hash)); }
}

AWorldScaleRun::AWorldScaleRun()
{
    PrimaryActorTick.bCanEverTick = true;
    PrimaryActorTick.TickGroup = TG_PostUpdateWork;
    Chunks.SetNum(ChunkCount);
    Poses.SetNum(Population);
}

bool AWorldScaleRun::Start(const FString& Mode, const FString& LegacyPath, const FString& Output, const FString& Save)
{
    ModeName = Mode;
    bStreamed = Mode.StartsWith(TEXT("streamed-"));
    bScheduled = Mode.EndsWith(TEXT("-scheduled"));
    bRestoreOnly = Mode == TEXT("restore");
    OutputPath = Output;
    SavePath = Save;
    FString Error;
    if ((Mode != TEXT("resident-full") && Mode != TEXT("streamed-full")
        && Mode != TEXT("resident-scheduled") && Mode != TEXT("streamed-scheduled") && !bRestoreOnly)
        || Output.IsEmpty() || (!bRestoreOnly && Save.IsEmpty()) || GetWorld()->WorldType != EWorldType::Game
        || !ReadWorldNpc(LegacyPath, Wolf, SourceSchema, Error))
    {
        UE_LOG(LogWorldLifecycle, Error, TEXT("Scale startup failed mode=%s fixture=%s reason=%s"), *Mode, *LegacyPath, *Error);
        return false;
    }
    Deadline = FPlatformTime::Seconds() + 40.0;
    if (!bRestoreOnly)
    {
        Frames.Reserve(4096);
        FrameHandle = FCoreDelegates::OnBeginFrame.AddUObject(this, &AWorldScaleRun::CaptureFrame);
    }
    return true;
}

void AWorldScaleRun::CaptureFrame()
{
    const double Now = FPlatformTime::Seconds();
    if (LastFrameAt > 0)
    {
        Frames.Add({FrameGroup, FrameRoute, (Now - LastFrameAt) * 1000.0, WorkEvaluations - LastFrameWork});
    }
    LastFrameAt = Now;
    LastFrameWork = WorkEvaluations;
}

void AWorldScaleRun::Tick(float DeltaSeconds)
{
    Super::Tick(DeltaSeconds);
    if (Phase == EPhase::Done)
    {
        return;
    }
    if (FPlatformTime::Seconds() > Deadline)
    {
        Finish(TEXT("route-timeout"));
        return;
    }
    switch (Phase)
    {
    case EPhase::Setup:
        if (bRestoreOnly)
        {
            RecordCheckpoint(TEXT("reopened"));
            Finish(nullptr);
            return;
        }
        if (!SetUpViews())
        {
            Finish(TEXT("missing-camera-or-npc-asset"));
            return;
        }
        RequestTransition(0);
        break;
    case EPhase::Transition:
        TickTransition();
        break;
    case EPhase::Warmup:
        FrameGroup = TEXT("warmup");
        SampleAgents(ScheduleTick);
        if (GetWorld()->GetTimeSeconds() - StageStartedAt >= 0.15)
        {
            StageStartedAt = GetWorld()->GetTimeSeconds();
            SegmentStartTick = ScheduleTick;
            Phase = EPhase::Steady;
        }
        break;
    case EPhase::Steady:
        TickSteady();
        break;
    case EPhase::Cleanup:
        TickCleanup();
        break;
    case EPhase::Done:
        break;
    }
}

bool AWorldScaleRun::SetUpViews()
{
    if (APlayerController* Player = GetWorld()->GetFirstPlayerController())
    {
        if (AHUD* Hud = Player->GetHUD())
        {
            Hud->bShowHUD = false;
        }
    }
    for (TActorIterator<ACameraActor> It(GetWorld()); It; ++It)
    {
        if (It->ActorHasTag(TEXT("TownCamera")))
        {
            TownCamera = *It;
            break;
        }
    }
    ForestCamera = GetWorld()->SpawnActor<ACameraActor>();
    UStaticMesh* Mesh = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Sphere.Sphere"));
    UMaterialInterface* Finish = LoadObject<UMaterialInterface>(nullptr, TEXT("/Game/Materials/Wolf.Wolf"));
    if (!TownCamera || !ForestCamera || !Mesh || !Finish)
    {
        return false;
    }
    Views.Reserve(NpcsPerChunk);
    for (int32 Index = 0; Index < NpcsPerChunk; ++Index)
    {
        AStaticMeshActor* View = GetWorld()->SpawnActor<AStaticMeshActor>();
        if (!View)
        {
            return false;
        }
        UStaticMeshComponent* Component = View->GetStaticMeshComponent();
        Component->SetMobility(EComponentMobility::Movable);
        Component->SetStaticMesh(Mesh);
        Component->SetMaterial(0, Finish);
        Component->SetCollisionEnabled(ECollisionEnabled::NoCollision);
        View->SetActorScale3D(FVector(0.23, 0.16, 0.33));
        View->SetActorHiddenInGame(true);
        Views.Add(View);
    }
    WolfProjection = NewObject<UWolfPresentationComponent>(Views[0].Get());
    Views[0]->AddInstanceComponent(WolfProjection);
    WolfProjection->RegisterComponent();
    return true;
}

void AWorldScaleRun::SetViews(int32 Chunk)
{
    VisibleChunk = Chunk;
    for (AStaticMeshActor* View : Views)
    {
        View->SetActorHiddenInGame(Chunk == INDEX_NONE);
        View->Tags.Reset();
    }
    APlayerController* Player = GetWorld()->GetFirstPlayerController();
    if (Chunk == INDEX_NONE)
    {
        Player->SetViewTarget(TownCamera);
        return;
    }
    const FVector Eye(CenterOf(Chunk) - 970.0, -1280.0, 925.0);
    const FVector Target(CenterOf(Chunk), 0.0, 60.0);
    ForestCamera->SetActorLocationAndRotation(Eye, (Target - Eye).Rotation());
    Player->SetViewTarget(ForestCamera);
    for (int32 Index = 0; Index < Views.Num(); ++Index)
    {
        const int32 Id = Chunk * NpcsPerChunk + Index;
        const FString Tag = Id == WolfIndex ? FWorldNpcState::Id : FString::Printf(TEXT("patrol-%04d"), Id);
        Views[Index]->Tags.Add(FName(*Tag));
    }
    SampleAgents(ScheduleTick);
    if (Chunk == WolfIndex / NpcsPerChunk)
    {
        WolfProjection->ProjectAt(Wolf, Poses[WolfIndex].Position);
    }
}

ULevelStreamingDynamic* AWorldScaleRun::RequestChunk(int32 Chunk)
{
    const FString Name = FString::Printf(TEXT("/Game/Maps/Scale/Chunk%d"), Chunk);
    ULevelStreamingDynamic::FLoadLevelInstanceParams Params(GetWorld(), Name, FTransform::Identity);
    Params.LevelStreamingCreatedCallback = [](ULevelStreaming* Level) { Level->bShouldBlockOnLoad = false; };
    bool bAccepted = false;
    ULevelStreamingDynamic* Level = ULevelStreamingDynamic::LoadLevelInstance(Params, bAccepted);
    return bAccepted ? Level : nullptr;
}

void AWorldScaleRun::RequestTransition(int32 Step)
{
    RequestedAt = FPlatformTime::Seconds();
    RouteStep = Step;
    FrameRoute = RouteNames[Step];
    FrameGroup = Step == 0 ? TEXT("startup") : TEXT("transition");
    const int32 Target = RouteChunks[Step];
    LastPeakLevelCount = 0;

    if (bStreamed)
    {
        for (int32 Index = 0; Index < Chunks.Num(); ++Index)
        {
            if (Chunks[Index] && Index != Target)
            {
                Chunks[Index]->SetShouldBeVisible(false);
                Chunks[Index]->SetShouldBeLoaded(false);
                Chunks[Index]->SetIsRequestingUnloadAndRemoval(true);
            }
        }
        if (Target != INDEX_NONE && !Chunks[Target])
        {
            Chunks[Target] = RequestChunk(Target);
            if (!Chunks[Target])
            {
                Finish(TEXT("chunk-request-failed"));
                return;
            }
        }
    }
    else if (Step == 0)
    {
        for (int32 Index = 0; Index < Chunks.Num(); ++Index)
        {
            Chunks[Index] = RequestChunk(Index);
            if (!Chunks[Index])
            {
                Finish(TEXT("resident-preload-failed"));
                return;
            }
        }
    }
    SetViews(INDEX_NONE);
    Phase = EPhase::Transition;
}

void AWorldScaleRun::TickTransition()
{
    const int32 Target = RouteChunks[RouteStep];
    int32 Loaded = 0;
    bool bReady = true;
    for (int32 Index = 0; Index < Chunks.Num(); ++Index)
    {
        const bool bRetain = !bStreamed || Index == Target;
        ULevelStreamingDynamic* Level = Chunks[Index];
        if (!Level)
        {
            bReady &= !bRetain;
            continue;
        }
        if (Level->GetLevelStreamingState() == ELevelStreamingState::FailedToLoad)
        {
            Finish(TEXT("chunk-load-failed"));
            return;
        }
        const bool bLoaded = Level->IsLevelLoaded();
        Loaded += bLoaded ? 1 : 0;
        if (bRetain)
        {
            bReady &= bLoaded && Level->IsLevelVisible();
        }
        else if (bLoaded || GetWorld()->GetStreamingLevels().Contains(Level))
        {
            bReady = false;
        }
        else
        {
            Chunks[Index] = nullptr;
        }
    }
    LastPeakLevelCount = FMath::Max(LastPeakLevelCount, Loaded);
    if (!bReady)
    {
        SampleAgents(ScheduleTick);
        return;
    }

    SetViews(Target);
    const TSharedRef<FJsonObject> Transition = MakeShared<FJsonObject>();
    Transition->SetStringField(TEXT("name"), RouteNames[RouteStep]);
    Transition->SetNumberField(TEXT("targetChunk"), Target);
    Transition->SetNumberField(TEXT("ms"), (FPlatformTime::Seconds() - RequestedAt) * 1000.0);
    Transition->SetNumberField(TEXT("peakObservedLoadedChunks"), LastPeakLevelCount);
    Transitions.Add(MakeShared<FJsonValueObject>(Transition));

    if (RouteStep == 4)
    {
        PatrolBase = Wolf.PatrolSteps;
        RecordCheckpoint(TEXT("detached"));
        Phase = EPhase::Cleanup;
        return;
    }
    StageStartedAt = GetWorld()->GetTimeSeconds();
    Phase = EPhase::Warmup;
}

void AWorldScaleRun::TickCleanup()
{
    FrameGroup = TEXT("cleanup");
    CollectGarbage(RF_NoFlags, true);
    RecordCheckpoint(TEXT("afterGc"));
    StageStartedAt = GetWorld()->GetTimeSeconds();
    Phase = EPhase::Warmup;
}

void AWorldScaleRun::TickSteady()
{
    FrameGroup = TEXT("steady");
    const double Elapsed = GetWorld()->GetTimeSeconds() - StageStartedAt;
    const int32 Taken = FMath::Clamp(FMath::FloorToInt(Elapsed * GameHz), 0, SegmentTicks);
    ScheduleTick = SegmentStartTick + Taken;
    if (RouteStep == 4 && Wolf.Hp > 0)
    {
        Wolf.PatrolSteps = static_cast<int32>(FMath::Min<int64>(MAX_int32, int64(PatrolBase) + Taken / PatrolPeriod));
    }
    SampleAgents(ScheduleTick);
    if (Taken != SegmentTicks)
    {
        return;
    }
    if (RouteStep == 3)
    {
        RecordCheckpoint(TEXT("beforeCombat"));
        Wolf.Hp = FMath::Max(0, Wolf.Hp - 40);
        Wolf.QuestStage = 1;
        SampleAgents(ScheduleTick);
        WolfProjection->ProjectAt(Wolf, Poses[WolfIndex].Position);
    }
    RecordCheckpoint(SettleNames[RouteStep]);
    if (RouteStep + 1 < UE_ARRAY_COUNT(RouteChunks))
    {
        RequestTransition(RouteStep + 1);
        return;
    }
    if (!WriteWorldNpc(SavePath, Wolf))
    {
        Finish(TEXT("write-failed"));
        return;
    }
    Finish(nullptr);
}

AWorldScaleRun::FPose AWorldScaleRun::EvaluateAgent(int32 Id, int32 Tick) const
{
    const int32 Chunk = Id / NpcsPerChunk;
    const int32 Index = Id % NpcsPerChunk;
    const int32 Offset = Id == WolfIndex ? (Wolf.PatrolSteps % 6) * 8 : (Index * 23 + Chunk * 7) % 48;
    const int32 PhaseTick = (Tick + Offset) % 48;
    const double Along = PhaseTick < 24 ? PhaseTick : 48 - PhaseTick;
    const double Across = PhaseTick < 24 ? PhaseTick / 2.0 : (PhaseTick - 24) / 2.0;
    FPose Pose;
    Pose.Position = FVector(CenterOf(Chunk) + (Index % 16 - 8) * 76.0 + Along * 2.0,
        (Index / 16 - 8) * 37.0 + Across, Id == WolfIndex ? 30.0 : 17.0);
    Pose.Facing = PhaseTick < 24 ? 6.0f : 174.0f;
    Pose.Patrol = Id == WolfIndex ? Wolf.PatrolSteps : (Tick + Offset) / PatrolPeriod;
    Pose.bNearObserver = VisibleChunk != INDEX_NONE &&
        FVector::DistSquared(Pose.Position, FVector(CenterOf(VisibleChunk), 0, 0)) <= FMath::Square(480.0);
    return Pose;
}

void AWorldScaleRun::SampleAgents(int32 Tick)
{
    ++WorkFrames;
    const int32 Begin = bScheduled ? (VisibleChunk == INDEX_NONE ? Population : VisibleChunk * NpcsPerChunk) : 0;
    const int32 End = bScheduled ? FMath::Min(Population, Begin + NpcsPerChunk) : Population;
    WorkEvaluations += End - Begin;
    for (int32 Id = Begin; Id < End; ++Id)
    {
        const FPose Pose = EvaluateAgent(Id, Tick);
        Poses[Id] = Pose;
        Observations += Pose.bNearObserver ? 1 : 0;
        if (VisibleChunk == Id / NpcsPerChunk)
        {
            AStaticMeshActor* View = Views[Id % NpcsPerChunk];
            View->SetActorLocationAndRotation(Pose.Position, FRotator(0, Pose.Facing, 0));
            View->SetActorHiddenInGame(Id == WolfIndex && Wolf.Hp == 0);
        }
    }
}

void AWorldScaleRun::RecordCheckpoint(const TCHAR* Name)
{
    const TSharedRef<FJsonObject> Entry = MakeShared<FJsonObject>();
    int32 Resident = 0;
    int32 Visible = 0;
    int32 Registered = 0;
    int32 ActorEntries = 0;
    for (const ULevelStreamingDynamic* Level : Chunks)
    {
        if (Level)
        {
            Registered += GetWorld()->GetStreamingLevels().Contains(Level) ? 1 : 0;
            Visible += Level->IsLevelVisible() ? 1 : 0;
            if (const ULevel* Loaded = Level->GetLoadedLevel())
            {
                ++Resident;
                ActorEntries += Loaded->Actors.Num();
            }
        }
    }

    uint64 StateHash = 14695981039346656037ull;
    for (int32 Id = 0; Id < Population; ++Id)
    {
        const FPose Pose = EvaluateAgent(Id, ScheduleTick);
        Mix(StateHash, Id);
        Mix(StateHash, Pose.Patrol);
        Mix(StateHash, Id == WolfIndex ? Wolf.Hp : 100);
        Mix(StateHash, Id == WolfIndex ? Wolf.QuestStage : 0);
        Mix(StateHash, FMath::RoundToInt64(Pose.Position.X * 10.0));
        Mix(StateHash, FMath::RoundToInt64(Pose.Position.Y * 10.0));
    }
    int32 ActiveViews = 0;
    int32 RecentlyRendered = 0;
    uint64 ViewHash = 14695981039346656037ull;
    for (const AStaticMeshActor* View : Views)
    {
        if (!View->IsHidden() && View->Tags.Num() == 1)
        {
            ++ActiveViews;
            const float LastOnScreen = View->GetStaticMeshComponent()->GetLastRenderTimeOnScreen();
            RecentlyRendered += LastOnScreen > 0.0f && GetWorld()->GetTimeSeconds() - LastOnScreen < 0.35 ? 1 : 0;
            const FVector Position = View->GetActorLocation();
            for (TCHAR Character : View->Tags[0].ToString())
            {
                Mix(ViewHash, Character);
            }
            Mix(ViewHash, FMath::RoundToInt64(Position.X * 10.0));
            Mix(ViewHash, FMath::RoundToInt64(Position.Y * 10.0));
        }
    }

    const FPlatformMemoryStats Memory = FPlatformMemory::GetStats();
    Entry->SetStringField(TEXT("name"), Name);
    Entry->SetNumberField(TEXT("chunk"), VisibleChunk);
    Entry->SetNumberField(TEXT("scheduleTick"), ScheduleTick);
    Entry->SetNumberField(TEXT("worldSeconds"), GetWorld()->GetTimeSeconds());
    Entry->SetNumberField(TEXT("logicalNpcs"), Population);
    Entry->SetNumberField(TEXT("activeViews"), ActiveViews);
    Entry->SetNumberField(TEXT("recentlyRenderedViews"), RecentlyRendered);
    Entry->SetNumberField(TEXT("residentChunks"), Resident);
    Entry->SetNumberField(TEXT("visibleChunks"), Visible);
    Entry->SetNumberField(TEXT("registeredChunks"), Registered);
    Entry->SetNumberField(TEXT("geometryActors"), ActorEntries);
    Entry->SetNumberField(TEXT("workEvaluations"), WorkEvaluations);
    Entry->SetNumberField(TEXT("workFrames"), WorkFrames);
    Entry->SetStringField(TEXT("populationHash"), Hex(StateHash));
    Entry->SetStringField(TEXT("viewHash"), Hex(ViewHash));
    Entry->SetNumberField(TEXT("hp"), Wolf.Hp);
    Entry->SetNumberField(TEXT("quest"), Wolf.QuestStage);
    Entry->SetNumberField(TEXT("patrol"), Wolf.PatrolSteps);
    const bool bWolfBound = WolfProjection && VisibleChunk == WolfIndex / NpcsPerChunk &&
        WolfProjection->GetOwner()->ActorHasTag(FWorldNpcState::Id);
    Entry->SetBoolField(TEXT("wolfViewBound"), bWolfBound);
    if (bWolfBound)
    {
        const FWorldNpcState& ViewState = WolfProjection->GetProjection();
        Entry->SetNumberField(TEXT("viewHp"), ViewState.Hp);
        Entry->SetNumberField(TEXT("viewQuest"), ViewState.QuestStage);
        Entry->SetNumberField(TEXT("viewPatrol"), ViewState.PatrolSteps);
    }
    Entry->SetNumberField(TEXT("privateBytes"), Memory.UsedVirtual);
    Entry->SetNumberField(TEXT("workingBytes"), Memory.UsedPhysical);
    Entry->SetNumberField(TEXT("peakWorkingBytes"), Memory.PeakUsedPhysical);
    Entry->SetNumberField(TEXT("peakPrivateBytes"), Memory.PeakUsedVirtual);
    Entry->SetStringField(TEXT("instance"), VisibleChunk == INDEX_NONE ? TEXT("") :
        Chunks[VisibleChunk]->GetWorldAssetPackageFName().ToString());
    Checkpoints.Add(MakeShared<FJsonValueObject>(Entry));
    UE_LOG(LogWorldLifecycle, Display, TEXT("Scale checkpoint=%s resident=%d views=%d tick=%d hp=%d quest=%d patrol=%d"),
        Name, Resident, ActiveViews, ScheduleTick, Wolf.Hp, Wolf.QuestStage, Wolf.PatrolSteps);
}

void AWorldScaleRun::Finish(const TCHAR* Failure)
{
    Phase = EPhase::Done;
    FCoreDelegates::OnBeginFrame.Remove(FrameHandle);
    const TSharedRef<FJsonObject> Result = MakeShared<FJsonObject>();
    Result->SetStringField(TEXT("mode"), ModeName);
    Result->SetStringField(TEXT("failure"), Failure ? Failure : TEXT(""));
    Result->SetStringField(TEXT("canonicalNpc"), FWorldNpcState::Id);
    UGameViewportClient* Client = GetWorld()->GetGameViewport();
    const FSceneViewport* Viewport = Client ? Client->GetGameViewport() : nullptr;
    const FIntPoint ViewSize = Viewport ? Viewport->GetSizeXY() : FIntPoint::ZeroValue;
    Result->SetBoolField(TEXT("windowed"), Viewport && Viewport->GetWindowMode() == EWindowMode::Windowed);
    Result->SetNumberField(TEXT("viewportX"), ViewSize.X);
    Result->SetNumberField(TEXT("viewportY"), ViewSize.Y);
    IConsoleManager& Console = IConsoleManager::Get();
    const IConsoleVariable* VSync = Console.FindConsoleVariable(TEXT("r.VSync"));
    const IConsoleVariable* MaxFps = Console.FindConsoleVariable(TEXT("t.MaxFPS"));
    Result->SetNumberField(TEXT("vsync"), VSync ? VSync->GetInt() : -1);
    Result->SetNumberField(TEXT("maxFps"), MaxFps ? MaxFps->GetFloat() : -1);
    Result->SetNumberField(TEXT("sourceSchema"), SourceSchema);
    Result->SetNumberField(TEXT("observations"), Observations);
    Result->SetArrayField(TEXT("checkpoints"), MoveTemp(Checkpoints));
    Result->SetArrayField(TEXT("transitions"), MoveTemp(Transitions));
    TArray<TSharedPtr<FJsonValue>> Rows;
    Rows.Reserve(Frames.Num());
    for (const FFrameSample& Frame : Frames)
    {
        TArray<TSharedPtr<FJsonValue>> Row{
            MakeShared<FJsonValueString>(Frame.Group), MakeShared<FJsonValueString>(Frame.Route),
            MakeShared<FJsonValueNumber>(Frame.WallMs), MakeShared<FJsonValueNumber>(Frame.Work)};
        Rows.Add(MakeShared<FJsonValueArray>(MoveTemp(Row)));
    }
    Result->SetArrayField(TEXT("frames"), MoveTemp(Rows));
    FString Text;
    FJsonSerializer::Serialize(Result, TJsonWriterFactory<TCHAR, TCondensedJsonPrintPolicy<TCHAR>>::Create(&Text));
    const bool bPublished = FFileHelper::SaveStringToFile(Text, *OutputPath, FFileHelper::EEncodingOptions::ForceUTF8WithoutBOM);
    if (Failure || !bPublished)
    {
        UE_LOG(LogWorldLifecycle, Error, TEXT("Scale failed reason=%s output=%s"), Failure ? Failure : TEXT("output-write-failed"), *OutputPath);
    }
    FPlatformMisc::RequestExitWithStatus(false, (Failure || !bPublished) ? 1 : 0, TEXT("World scale experiment finished"));
}

void AWorldScaleRun::EndPlay(const EEndPlayReason::Type Reason)
{
    FCoreDelegates::OnBeginFrame.Remove(FrameHandle);
    Super::EndPlay(Reason);
}
