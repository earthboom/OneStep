#include "PulseArenaHUD.h"

#include "Engine/Canvas.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "PulseArenaController.h"

void APulseArenaHUD::DrawHUD()
{
    Super::DrawHUD();
    const APulseArenaController* Player = Cast<APulseArenaController>(PlayerOwner);
    if (!Canvas || !Player || Player->Encounters.IsEmpty())
    {
        return;
    }

    const auto& Encounter = Player->Encounters[Player->Selected];
    const double Remaining = FMath::Max(0.0, Encounter.ReadyAt - GetWorld()->GetTimeSeconds());
    const FLinearColor Aqua(0.21f, 0.85f, 0.71f, 1.0f);
    const bool bReady = Remaining <= 0.0;
    const FLinearColor TargetColor = bReady ? Aqua : FLinearColor(0.23f, 0.32f, 0.34f);
    const FLinearColor Backdrop(0.016f, 0.033f, 0.049f, 1.0f);
    DrawRect(Backdrop, 0, 0, Canvas->ClipX, Canvas->ClipY);
    const float X = Canvas->ClipX * 0.11f;
    const float Y = Canvas->ClipY * 0.22f;
    const float TargetWidth = FMath::Min(40.0f, Canvas->ClipX * 0.05f);
    DrawText(TEXT("PULSE ARENA"), Aqua, X, Y, GEngine->GetMediumFont(), 1.0f);
    DrawText(Encounter.Title, FLinearColor::White, X, Y + 39.0f, GEngine->GetLargeFont(), 1.25f);
    DrawText(FString::Printf(TEXT("Targets cleared  %d"), Encounter.Score),
        FLinearColor::White, X, Y + 87.0f, GEngine->GetMediumFont(), 1.0f);

    for (int32 Target = 0; Target < Encounter.TargetCount; ++Target)
    {
        DrawRect(TargetColor, X + Target * (TargetWidth + 8.0f), Y + 130.0f, TargetWidth, TargetWidth);
    }

    const FString Status = bReady ? TEXT("Ready") : FString::Printf(TEXT("Recharging %.1fs"), Remaining);
    DrawText(Status, TargetColor, X, Y + 188.0f, GEngine->GetMediumFont(), 1.0f);
    const TCHAR* Controls = Player->Encounters.Num() > 1 ? TEXT("SPACE  Pulse       TAB  Next encounter") : TEXT("SPACE  Pulse");
    DrawText(Controls, FLinearColor::White, X, Y + 231.0f, GEngine->GetMediumFont(), 1.0f);
}
