#include "PulseArenaController.h"

#include "Components/InputComponent.h"
#include "Dom/JsonObject.h"
#include "Engine/World.h"
#include "HAL/FileManager.h"
#include "HAL/PlatformMisc.h"
#include "InputKeyEventArgs.h"
#include "Misc/CommandLine.h"
#include "Misc/FileHelper.h"
#include "Misc/Parse.h"
#include "Misc/Paths.h"
#include "Serialization/JsonReader.h"
#include "Serialization/JsonSerializer.h"

DEFINE_LOG_CATEGORY_STATIC(LogPulseArena, Log, All);

void APulseArenaController::SetupInputComponent()
{
    Super::SetupInputComponent();
    InputComponent->BindKey(EKeys::SpaceBar, IE_Pressed, this, &APulseArenaController::Pulse);
    InputComponent->BindKey(EKeys::Tab, IE_Pressed, this, &APulseArenaController::AdvanceEncounter);
}

void APulseArenaController::BeginPlay()
{
    Super::BeginPlay();
    if (!IsLocalController())
    {
        return;
    }

    UE_LOG(LogPulseArena, Display, TEXT("Session game=%d local=%d net=%d map=%s"),
        GetWorld()->WorldType == EWorldType::Game, IsLocalController(), GetNetMode(), *GetWorld()->GetMapName());
    LoadEncounters();
    if (FParse::Param(FCommandLine::Get(), TEXT("PulseSmoke")))
    {
        GetWorldTimerManager().SetTimer(ProbeTimer, this, &APulseArenaController::RunProbeStep, 0.25f);
    }
}

void APulseArenaController::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
    GetWorldTimerManager().ClearTimer(ProbeTimer);
    UE_LOG(LogPulseArena, Display, TEXT("EndPlay encounters=%d pending=%d"),
        Encounters.Num(), GetWorldTimerManager().TimerExists(ProbeTimer));
    Super::EndPlay(EndPlayReason);
}

void APulseArenaController::LoadEncounters()
{
    Encounters.Add({TEXT("practice"), TEXT("Practice Range"), 0.5, 2});
    UE_LOG(LogPulseArena, Display, TEXT("Registered id=practice cooldown=0.500 targets=2 source=builtin"));

    const FString Directory = FPaths::ConvertRelativePathToFull(
        FPaths::Combine(FPaths::ProjectContentDir(), TEXT("Encounters")));
    UE_LOG(LogPulseArena, Display, TEXT("Catalog path=%s"), *Directory);
    TArray<FString> Files;
    IFileManager::Get().FindFiles(Files, *FPaths::Combine(Directory, TEXT("*.json")), true, false);
    Files.Sort();

    for (const FString& File : Files)
    {
        const FString Id = FPaths::GetBaseFilename(File);
        FString Source;
        TSharedPtr<FJsonObject> Object;
        FEncounter Encounter{Id, FString(), 0.0, 0};
        double Targets = 0.0;
        if (Id.Equals(TEXT("practice"), ESearchCase::IgnoreCase)
            || !FFileHelper::LoadFileToString(Source, *FPaths::Combine(Directory, File))
            || !FJsonSerializer::Deserialize(TJsonReaderFactory<>::Create(Source), Object)
            || !Object.IsValid()
            || !Object->TryGetStringField(TEXT("title"), Encounter.Title)
            || Encounter.Title.TrimStartAndEnd().IsEmpty() || Encounter.Title.Len() > 48
            || !Object->TryGetNumberField(TEXT("cooldownSeconds"), Encounter.Cooldown)
            || !FMath::IsFinite(Encounter.Cooldown)
            || Encounter.Cooldown < 0.25 || Encounter.Cooldown > 10.0
            || !Object->TryGetNumberField(TEXT("targets"), Targets)
            || !FMath::IsFinite(Targets) || Targets < 1 || Targets > 12
            || Targets != FMath::FloorToDouble(Targets))
        {
            UE_LOG(LogPulseArena, Warning, TEXT("Skipped invalid encounter file=%s"), *File);
            continue;
        }

        Encounter.TargetCount = static_cast<int32>(Targets);
        UE_LOG(LogPulseArena, Display, TEXT("Registered id=%s cooldown=%.3f targets=%d source=%s"),
            *Encounter.Id, Encounter.Cooldown, Encounter.TargetCount, *File);
        Encounters.Add(MoveTemp(Encounter));
    }
}

void APulseArenaController::AdvanceEncounter()
{
    if (!Encounters.IsEmpty())
    {
        Selected = (Selected + 1) % Encounters.Num();
        UE_LOG(LogPulseArena, Display, TEXT("Selected id=%s"), *Encounters[Selected].Id);
    }
}

void APulseArenaController::Pulse()
{
    if (Encounters.IsEmpty())
    {
        return;
    }

    FEncounter& Encounter = Encounters[Selected];
    const double Now = GetWorld()->GetTimeSeconds();
    const bool bAccepted = Now >= Encounter.ReadyAt;
    if (bAccepted)
    {
        Encounter.ReadyAt = Now + Encounter.Cooldown;
        Encounter.Score += Encounter.TargetCount;
    }

    UE_LOG(LogPulseArena, Display, TEXT("Pulse id=%s accepted=%d time=%.6f ready=%.6f score=%d"),
        *Encounter.Id, bAccepted, Now, Encounter.ReadyAt, Encounter.Score);
}

void APulseArenaController::SendProbeKey(FKey Key)
{
    InputKey(FInputKeyEventArgs::CreateSimulated(Key, IE_Pressed, 1.0f));
    InputKey(FInputKeyEventArgs::CreateSimulated(Key, IE_Released, 0.0f));
}

void APulseArenaController::RunProbeStep()
{
    // Route the scripted presses through PlayerInput and the normal key bindings.
    float Delay = 0.2f;
    switch (ProbeStep)
    {
        case 0:
            SendProbeKey(EKeys::SpaceBar);
            Delay = 0.125f;
            break;
        case 1:
            SendProbeKey(EKeys::SpaceBar);
            Delay = 1.0f;
            break;
        case 2:
            SendProbeKey(EKeys::SpaceBar);
            break;
        case 3:
            ++ProbeEncounter;
            if (ProbeEncounter == Encounters.Num())
            {
                UE_LOG(LogPulseArena, Display, TEXT("Probe complete"));
                FPlatformMisc::RequestExitWithStatus(false, 0, TEXT("Pulse arena scripted inputs finished"));
                return;
            }
            SendProbeKey(EKeys::Tab);
            ProbeStep = -1;
            break;
    }
    ++ProbeStep;
    GetWorldTimerManager().SetTimer(ProbeTimer, this, &APulseArenaController::RunProbeStep, Delay);
}
