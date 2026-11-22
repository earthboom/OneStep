#pragma once

#include "GameFramework/HUD.h"
#include "GameFramework/PlayerController.h"
#include "WorldLifecyclePlayer.generated.h"

class AWorldLifecycleMode;

UCLASS()
class AWorldLifecyclePlayer : public APlayerController
{
    GENERATED_BODY()

public:
    AWorldLifecyclePlayer();

protected:
    void BeginPlay() override;
    void EndPlay(const EEndPlayReason::Type Reason) override;
    void SetupInputComponent() override;
    void PlayerTick(float DeltaSeconds) override;

private:
    enum class EProbeStep : uint8 { Start, Entered, Hit, Patrol, Reentered, Saved, Done };

    AWorldLifecycleMode* Mode() const;
    void Enter();
    void Hit();
    void Return();
    void Save();
    void Press(FKey Key);
    void TickProbe();
    void FinishProbe(bool bPassed);

    FString Probe;
    EProbeStep ProbeStep = EProbeStep::Start;
    double ProbeDeadline = 0;
    double FirstPressAt = 0;
};

UCLASS()
class AWorldLifecycleHUD : public AHUD
{
    GENERATED_BODY()

protected:
    void DrawHUD() override;
};
