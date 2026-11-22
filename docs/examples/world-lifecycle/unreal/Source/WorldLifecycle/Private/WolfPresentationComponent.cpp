#include "WolfPresentationComponent.h"

#include "GameFramework/Actor.h"

void UWolfPresentationComponent::Project(const FWorldNpcState& State)
{
    ProjectAt(State, FVector(2200.0 + (State.PatrolSteps % 5) * 85.0, 20.0, 42.0));
}

void UWolfPresentationComponent::ProjectAt(const FWorldNpcState& State, const FVector& Position)
{
    Projection = State;
    GetOwner()->SetActorHiddenInGame(State.Hp == 0);
    GetOwner()->SetActorLocation(Position);
}
