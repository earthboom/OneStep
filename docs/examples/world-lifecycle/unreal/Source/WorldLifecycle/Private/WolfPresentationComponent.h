#pragma once

#include "Components/ActorComponent.h"
#include "WorldNpcState.h"
#include "WolfPresentationComponent.generated.h"

UCLASS()
class UWolfPresentationComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    void Project(const FWorldNpcState& State);
    const FWorldNpcState& GetProjection() const { return Projection; }

private:
    FWorldNpcState Projection;
};
