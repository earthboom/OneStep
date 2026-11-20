#pragma once

#include "GameFramework/HUD.h"
#include "PulseArenaHUD.generated.h"

UCLASS()
class APulseArenaHUD : public AHUD
{
    GENERATED_BODY()

protected:
    virtual void DrawHUD() override;
};
