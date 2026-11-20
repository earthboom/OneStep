#pragma once
#include "Kismet/BlueprintFunctionLibrary.h"
#include "ReaderFixtureLibrary.generated.h"

UCLASS()
class UReaderFixtureLibrary : public UBlueprintFunctionLibrary
{
    GENERATED_BODY()
public:
    UFUNCTION(BlueprintCallable, Category="ReaderChecks")
    static FString PropertyText(UObject* Object, const FString& Name);

    UFUNCTION(BlueprintCallable, Category="ReaderChecks")
    static UObject* ConfigureWidget(UObject* Blueprint);
};
