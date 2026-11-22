#include "WolfPresentationComponent.h"

#include "GameFramework/Actor.h"

void UWolfPresentationComponent::Project(const FWorldNpcState& State)
{
    Projection = State;
    GetOwner()->SetActorHiddenInGame(State.Hp == 0);
    GetOwner()->SetActorLocation(FVector(2200.0 + (State.PatrolSteps % 5) * 85.0, 20.0, 42.0));
}
