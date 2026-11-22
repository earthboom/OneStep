#pragma once

#include "GameFramework/GameModeBase.h"
#include "WorldNpcState.h"
#include "WorldLifecycleMode.generated.h"

class ULevelStreamingDynamic;
class UWolfPresentationComponent;

DECLARE_LOG_CATEGORY_EXTERN(LogWorldLifecycle, Log, All);

enum class EForestPhase : uint8 { Town, Loading, Forest, Unloading };

UCLASS()
class AWorldLifecycleMode : public AGameModeBase
{
    GENERATED_BODY()

public:
    AWorldLifecycleMode();
    void StartVisit();
    void HitWolf();
    void ReturnToTown();
    void SaveSlot();
    bool RestoreFrom(const FString& Path, FString& Error);
    void ApplyCamera(APlayerController& Player) const;

    bool IsReady() const { return bReady; }
    EForestPhase GetPhase() const { return Phase; }
    const FWorldNpcState& GetState() const { return State; }
    int32 GetVisit() const { return Visit; }
    bool HasSaved() const { return bSaved; }
    const FString& GetStatus() const { return Status; }

protected:
    void BeginPlay() override;
    void Tick(float DeltaSeconds) override;

private:
    UWolfPresentationComponent* CreateProjection();
    bool IsPresentationActive() const;
    void MarkRequest();
    void SampleTransition();
    void UpdateCamera() const;

    FWorldNpcState State;
    EForestPhase Phase = EForestPhase::Town;
    FString Status;
    FString SlotPath;
    bool bReady = false;
    bool bSaved = false;
    int32 Visit = 0;
    double NextPatrolAt = 0.0;
    double RequestedAt = 0.0;
    double PreviousSample = 0.0;
    double MaxTickGap = 0.0;
    int32 TickGaps = 0;

    UPROPERTY(Transient)
    TObjectPtr<ULevelStreamingDynamic> ForestStream;
    TWeakObjectPtr<UWolfPresentationComponent> WolfView;
};
