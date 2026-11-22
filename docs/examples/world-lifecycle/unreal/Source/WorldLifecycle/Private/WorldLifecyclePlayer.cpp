#include "WorldLifecyclePlayer.h"

#include "Components/InputComponent.h"
#include "Engine/Canvas.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "HAL/PlatformMisc.h"
#include "HAL/PlatformTime.h"
#include "InputKeyEventArgs.h"
#include "Misc/CommandLine.h"
#include "Misc/Parse.h"
#include "WorldLifecycleMode.h"

AWorldLifecyclePlayer::AWorldLifecyclePlayer()
{
    bAutoManageActiveCameraTarget = false;
}

void AWorldLifecyclePlayer::BeginPlay()
{
    Super::BeginPlay();
    if (const AWorldLifecycleMode* Game = Mode())
    {
        Game->ApplyCamera(*this);
    }
    if (IsLocalController() && FParse::Value(FCommandLine::Get(), TEXT("WorldProbe="), Probe))
    {
        FirstPressAt = GetWorld()->GetTimeSeconds() + 0.5;
        ProbeDeadline = FPlatformTime::Seconds() + 30;
    }
}

void AWorldLifecyclePlayer::EndPlay(const EEndPlayReason::Type Reason)
{
    if (!Probe.IsEmpty())
    {
        UE_LOG(LogWorldLifecycle, Display, TEXT("end"));
    }
    Super::EndPlay(Reason);
}

void AWorldLifecyclePlayer::SetupInputComponent()
{
    Super::SetupInputComponent();
    InputComponent->BindKey(EKeys::E, IE_Pressed, this, &AWorldLifecyclePlayer::Enter);
    InputComponent->BindKey(EKeys::SpaceBar, IE_Pressed, this, &AWorldLifecyclePlayer::Hit);
    InputComponent->BindKey(EKeys::R, IE_Pressed, this, &AWorldLifecyclePlayer::Return);
    InputComponent->BindKey(EKeys::S, IE_Pressed, this, &AWorldLifecyclePlayer::Save);
}

AWorldLifecycleMode* AWorldLifecyclePlayer::Mode() const
{
    return GetWorld()->GetAuthGameMode<AWorldLifecycleMode>();
}

void AWorldLifecyclePlayer::Enter()
{
    if (AWorldLifecycleMode* Game = Mode()) { Game->StartVisit(); }
}

void AWorldLifecyclePlayer::Hit()
{
    if (AWorldLifecycleMode* Game = Mode()) { Game->HitWolf(); }
}

void AWorldLifecyclePlayer::Return()
{
    if (AWorldLifecycleMode* Game = Mode()) { Game->ReturnToTown(); }
}

void AWorldLifecyclePlayer::Save()
{
    if (AWorldLifecycleMode* Game = Mode()) { Game->SaveSlot(); }
}

void AWorldLifecyclePlayer::PlayerTick(float DeltaSeconds)
{
    Super::PlayerTick(DeltaSeconds);
    if (!Probe.IsEmpty() && ProbeStep != EProbeStep::Done)
    {
        TickProbe();
    }
}

void AWorldLifecyclePlayer::Press(FKey Key)
{
    InputKey(FInputKeyEventArgs::CreateSimulated(Key, IE_Pressed, 1.0f));
    InputKey(FInputKeyEventArgs::CreateSimulated(Key, IE_Released, 0.0f));
}

void AWorldLifecyclePlayer::TickProbe()
{
    AWorldLifecycleMode* Game = Mode();
    if (!Game || !Game->IsReady() || FPlatformTime::Seconds() > ProbeDeadline)
    {
        FinishProbe(false);
        return;
    }

    switch (ProbeStep)
    {
    case EProbeStep::Start:
        if (GetWorld()->GetTimeSeconds() >= FirstPressAt)
        {
            Press(EKeys::E);
            ProbeStep = EProbeStep::Entered;
        }
        break;
    case EProbeStep::Entered:
        if (Game->GetPhase() == EForestPhase::Forest)
        {
            if (Probe == TEXT("restore"))
            {
                FinishProbe(true);
                break;
            }
            Press(EKeys::SpaceBar);
            ProbeStep = EProbeStep::Hit;
        }
        break;
    case EProbeStep::Hit:
        if (Game->GetState().Hp == 60)
        {
            Press(EKeys::R);
            ProbeStep = EProbeStep::Patrol;
        }
        break;
    case EProbeStep::Patrol:
        if (Game->GetPhase() == EForestPhase::Town && Game->GetState().PatrolSteps > 0)
        {
            Press(EKeys::E);
            ProbeStep = EProbeStep::Reentered;
        }
        break;
    case EProbeStep::Reentered:
        if (Game->GetPhase() == EForestPhase::Forest && Game->GetVisit() == 2)
        {
            Press(EKeys::S);
            ProbeStep = EProbeStep::Saved;
        }
        break;
    case EProbeStep::Saved:
        if (Game->HasSaved())
        {
            FString Path;
            FString Error;
            const bool bHasCandidate = FParse::Value(FCommandLine::Get(), TEXT("RejectedFixture="), Path);
            const bool bRejected = bHasCandidate && !Game->RestoreFrom(Path, Error);
            FinishProbe(bRejected && Error == TEXT("unsupported-schema"));
        }
        break;
    case EProbeStep::Done:
        break;
    }
}

void AWorldLifecyclePlayer::FinishProbe(bool bPassed)
{
    if (bPassed)
    {
        UE_LOG(LogWorldLifecycle, Display, TEXT("complete"));
    }
    else
    {
        UE_LOG(LogWorldLifecycle, Error, TEXT("Probe failed at step %d"), static_cast<int32>(ProbeStep));
    }
    ProbeStep = EProbeStep::Done;
    FPlatformMisc::RequestExitWithStatus(false, bPassed ? 0 : 1, TEXT("World lifecycle probe finished"));
}

void AWorldLifecycleHUD::DrawHUD()
{
    Super::DrawHUD();
    const AWorldLifecycleMode* Game = GetWorld()->GetAuthGameMode<AWorldLifecycleMode>();
    if (!Canvas || !Game)
    {
        return;
    }
    const bool bForest = Game->GetPhase() == EForestPhase::Forest;
    const FLinearColor Panel(0.025f, 0.043f, 0.034f, 0.92f);
    const FLinearColor PaleGreen(0.67f, 0.90f, 0.68f);
    const float Left = 22.0f;
    DrawRect(Panel, Left, 22, 350, 118);
    DrawText(bForest ? TEXT("Forest") : TEXT("Town"), PaleGreen, Left + 14, 29, GEngine->GetLargeFont(), 1.3f);
    DrawText(Game->GetStatus(), FLinearColor::White, Left + 14, 60, GEngine->GetMediumFont());
    const FWorldNpcState& Npc = Game->GetState();
    DrawText(FString::Printf(TEXT("Wolf HP %d     Quest %d     Patrol %d"), Npc.Hp, Npc.QuestStage, Npc.PatrolSteps),
        PaleGreen, Left + 14, 90, GEngine->GetMediumFont());
    DrawText(bForest ? TEXT("Space  Strike       R  Town       S  Save") : TEXT("E  Forest       S  Save"),
        FLinearColor::White, Left + 14, 113, GEngine->GetMediumFont());
}
