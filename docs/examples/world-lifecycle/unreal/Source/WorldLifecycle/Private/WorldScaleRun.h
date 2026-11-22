#pragma once

#include "GameFramework/Actor.h"
#include "WorldNpcState.h"
#include "WorldScaleRun.generated.h"

class ACameraActor;
class AStaticMeshActor;
class FJsonValue;
class ULevelStreamingDynamic;
class UWolfPresentationComponent;

UCLASS()
class AWorldScaleRun : public AActor
{
    GENERATED_BODY()

public:
    AWorldScaleRun();
    bool Start(const FString& Mode, const FString& LegacyPath, const FString& Output, const FString& Save);

protected:
    void Tick(float DeltaSeconds) override;
    void EndPlay(const EEndPlayReason::Type Reason) override;

private:
    static constexpr int32 ChunkCount = 8;
    static constexpr int32 NpcsPerChunk = 256;
    static constexpr int32 Population = ChunkCount * NpcsPerChunk;
    static constexpr int32 WolfIndex = 5 * NpcsPerChunk;

    enum class EPhase : uint8 { Setup, Transition, Warmup, Steady, Cleanup, Done };

    struct FPose
    {
        FVector Position;
        float Facing = 0.0f;
        int32 Patrol = 0;
        bool bNearObserver = false;
    };

    struct FFrameSample
    {
        const TCHAR* Group;
        const TCHAR* Route;
        double WallMs;
        uint64 Work;
    };

    void CaptureFrame();
    bool SetUpViews();
    void SetViews(int32 Chunk);
    void RequestTransition(int32 Step);
    void TickTransition();
    void TickSteady();
    void TickCleanup();
    ULevelStreamingDynamic* RequestChunk(int32 Chunk);
    void SampleAgents(int32 Tick);
    FPose EvaluateAgent(int32 Id, int32 Tick) const;
    void RecordCheckpoint(const TCHAR* Name);
    void Finish(const TCHAR* Failure);

    UPROPERTY(Transient)
    TArray<TObjectPtr<ULevelStreamingDynamic>> Chunks;
    UPROPERTY(Transient)
    TArray<TObjectPtr<AStaticMeshActor>> Views;
    UPROPERTY(Transient)
    TObjectPtr<ACameraActor> ForestCamera;
    UPROPERTY(Transient)
    TObjectPtr<AActor> TownCamera;
    UPROPERTY(Transient)
    TObjectPtr<UWolfPresentationComponent> WolfProjection;

    TArray<FPose> Poses;
    TArray<FFrameSample> Frames;
    TArray<TSharedPtr<FJsonValue>> Checkpoints;
    TArray<TSharedPtr<FJsonValue>> Transitions;
    FWorldNpcState Wolf;
    FString ModeName;
    FString OutputPath;
    FString SavePath;
    FDelegateHandle FrameHandle;
    EPhase Phase = EPhase::Setup;
    const TCHAR* FrameGroup = TEXT("startup");
    const TCHAR* FrameRoute = TEXT("preload");
    int32 SourceSchema = 0;
    int32 RouteStep = -1;
    int32 VisibleChunk = INDEX_NONE;
    int32 ScheduleTick = 0;
    int32 SegmentStartTick = 0;
    int32 PatrolBase = 0;
    int32 LastPeakLevelCount = 0;
    uint64 WorkEvaluations = 0;
    uint64 LastFrameWork = 0;
    uint64 WorkFrames = 0;
    uint64 Observations = 0;
    double LastFrameAt = 0;
    double RequestedAt = 0;
    double StageStartedAt = 0;
    double Deadline = 0;
    bool bStreamed = false;
    bool bScheduled = false;
    bool bRestoreOnly = false;
};
