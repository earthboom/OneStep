#include "PulseArenaGameMode.h"

#include "PulseArenaController.h"
#include "PulseArenaHUD.h"

APulseArenaGameMode::APulseArenaGameMode()
{
    PlayerControllerClass = APulseArenaController::StaticClass();
    HUDClass = APulseArenaHUD::StaticClass();
}
