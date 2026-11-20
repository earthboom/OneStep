#pragma once

#include "CoreMinimal.h"
#include "GameFramework/PlayerController.h"
#include "TimerManager.h"
#include "PulseArenaController.generated.h"

UCLASS()
class APulseArenaController : public APlayerController
{
    GENERATED_BODY()

protected:
    virtual void SetupInputComponent() override;
    virtual void BeginPlay() override;
    virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;

private:
    friend class APulseArenaHUD;

    struct FEncounter
    {
        FString Id;
        FString Title;
        double Cooldown;
        int32 TargetCount;
        double ReadyAt = 0.0;
        int32 Score = 0;
    };

    void LoadEncounters();
    void AdvanceEncounter();
    void Pulse();
    void SendProbeKey(FKey Key);
    void RunProbeStep();

    TArray<FEncounter> Encounters;
    int32 Selected = 0;
    FTimerHandle ProbeTimer;
    int32 ProbeEncounter = 0;
    int32 ProbeStep = 0;
};
