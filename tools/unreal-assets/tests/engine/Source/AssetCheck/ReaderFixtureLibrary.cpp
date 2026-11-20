#include "ReaderFixtureLibrary.h"
#include "Modules/ModuleManager.h"
#include "UObject/UnrealType.h"
#include "WidgetBlueprint.h"
#include "Blueprint/WidgetTree.h"
#include "Components/CanvasPanel.h"
#include "Components/TextBlock.h"
#include "Kismet2/KismetEditorUtilities.h"

IMPLEMENT_PRIMARY_GAME_MODULE(FDefaultGameModuleImpl, AssetCheck, "AssetCheck");

FString UReaderFixtureLibrary::PropertyText(UObject* Object, const FString& Name)
{
    check(Object);
    FProperty* Property = FindFProperty<FProperty>(Object->GetClass(), *Name);
    checkf(Property, TEXT("Missing native property %s"), *Name);
    FString Text;
    Property->ExportText_InContainer(0, Text, Object, nullptr, Object, PPF_None);
    return Text;
}

UObject* UReaderFixtureLibrary::ConfigureWidget(UObject* Blueprint)
{
    UWidgetBlueprint* BP = CastChecked<UWidgetBlueprint>(Blueprint);
    check(BP->GetOutermost()->GetName().StartsWith(TEXT("/Game/ReaderChecks/")));
    UCanvasPanel* Root = NewObject<UCanvasPanel>(BP->WidgetTree, TEXT("RootCanvas"));
    BP->WidgetTree->RootWidget = Root;
    UTextBlock* Label = NewObject<UTextBlock>(BP->WidgetTree, TEXT("StatusLabel"));
    Label->SetText(FText::FromString(TEXT("Reader verification 37")));
    Label->SetRenderOpacity(0.625f);
    Root->AddChild(Label);
    FKismetEditorUtilities::CompileBlueprint(BP);
    return Label;
}
