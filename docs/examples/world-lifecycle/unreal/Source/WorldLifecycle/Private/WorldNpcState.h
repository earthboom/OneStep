#pragma once

#include "CoreMinimal.h"

struct FWorldNpcState
{
    static constexpr const TCHAR* Id = TEXT("forest-wolf-v2");
    int32 Hp = 100;
    int32 QuestStage = 0;
    int32 PatrolSteps = 0;
};

bool ReadWorldNpc(const FString& Path, FWorldNpcState& State, int32& Schema, FString& Error);
bool WriteWorldNpc(const FString& Path, const FWorldNpcState& State);
