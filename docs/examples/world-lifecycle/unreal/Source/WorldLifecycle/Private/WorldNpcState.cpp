#include "WorldNpcState.h"

#include "Dom/JsonObject.h"
#include "HAL/FileManager.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "Serialization/JsonReader.h"
#include "Serialization/JsonSerializer.h"

namespace
{
bool ReadInt(const FJsonObject& Object, const TCHAR* Name, int32 Min, int32 Max, int32& Value)
{
    const TSharedPtr<FJsonValue> Field = Object.TryGetField(Name);
    double Number = 0;
    if (!Field || Field->Type != EJson::Number || !Field->TryGetNumber(Number)
        || !FMath::IsFinite(Number) || Number < Min || Number > Max || Number != FMath::FloorToDouble(Number))
    {
        return false;
    }
    Value = static_cast<int32>(Number);
    return true;
}
}

bool ReadWorldNpc(const FString& Path, FWorldNpcState& State, int32& Schema, FString& Error)
{
    FString Text;
    if (!FFileHelper::LoadFileToString(Text, *Path))
    {
        Error = TEXT("unreadable-file");
        return false;
    }
    TSharedPtr<FJsonObject> Object;
    if (!FJsonSerializer::Deserialize(TJsonReaderFactory<>::Create(Text), Object) || !Object)
    {
        Error = TEXT("invalid-json");
        return false;
    }
    int32 ReadSchema = 0;
    if (!ReadInt(*Object, TEXT("schemaVersion"), 1, MAX_int32, ReadSchema)
        || (ReadSchema != 1 && ReadSchema != 2))
    {
        Error = TEXT("unsupported-schema");
        return false;
    }

    // The v1 authored ID aliases the same logical NPC under the current canonical ID.
    const TCHAR* ExpectedId = ReadSchema == 1 ? TEXT("forest-wolf") : FWorldNpcState::Id;
    FString Id;
    FWorldNpcState Candidate;
    if (!Object->TryGetStringField(TEXT("npcId"), Id) || !Id.Equals(ExpectedId, ESearchCase::CaseSensitive)
        || !ReadInt(*Object, TEXT("hp"), 0, 100, Candidate.Hp)
        || !ReadInt(*Object, TEXT("questStage"), 0, 1, Candidate.QuestStage)
        || !ReadInt(*Object, TEXT("patrolSteps"), 0, MAX_int32, Candidate.PatrolSteps))
    {
        Error = TEXT("invalid-npc-state");
        return false;
    }

    State = Candidate;
    Schema = ReadSchema;
    return true;
}

bool WriteWorldNpc(const FString& Path, const FWorldNpcState& State)
{
    const TSharedRef<FJsonObject> Object = MakeShared<FJsonObject>();
    Object->SetNumberField(TEXT("schemaVersion"), 2);
    Object->SetStringField(TEXT("npcId"), FWorldNpcState::Id);
    Object->SetNumberField(TEXT("hp"), State.Hp);
    Object->SetNumberField(TEXT("questStage"), State.QuestStage);
    Object->SetNumberField(TEXT("patrolSteps"), State.PatrolSteps);
    FString Text;
    FJsonSerializer::Serialize(Object, TJsonWriterFactory<>::Create(&Text));

    IFileManager& Files = IFileManager::Get();
    Files.MakeDirectory(*FPaths::GetPath(Path), true);
    const FString PendingPath = Path + TEXT(".pending");
    return FFileHelper::SaveStringToFile(Text, *PendingPath, FFileHelper::EEncodingOptions::ForceUTF8WithoutBOM)
        && Files.Move(*Path, *PendingPath, true, false);
}
