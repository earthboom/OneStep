"""Generate the two small Unreal maps from engine primitives in the Unreal Python editor."""

import random

import unreal


LEVELS = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
ACTORS = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
ASSETS = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
MESHES = {shape: unreal.load_asset(f"/Engine/BasicShapes/{shape}")
          for shape in ("Cube", "Cone", "Sphere")}
MATERIALS = {
    "TownFloor": (0.29, 0.24, 0.17), "TownWall": (0.48, 0.31, 0.16),
    "TownRoof": (0.47, 0.12, 0.06), "Track": (0.48, 0.38, 0.22),
    "ForestFloor": (0.10, 0.19, 0.08), "Trunk": (0.20, 0.09, 0.04),
    "Pine": (0.05, 0.22, 0.09), "Wolf": (0.27, 0.28, 0.32),
}


def begin(name):
    package = f"/Game/Maps/{name}"
    if not LEVELS.new_level(package):
        raise RuntimeError(f"Could not create {package}. Remove that map from a disposable copy before rebuilding it.")


def material(name, rgb):
    path = f"/Game/Materials/{name}"
    if ASSETS.does_asset_exist(path):
        return ASSETS.load_asset(path)
    tools = unreal.AssetToolsHelpers.get_asset_tools()
    asset = tools.create_asset(name, "/Game/Materials", unreal.Material, unreal.MaterialFactoryNew())
    editing = unreal.MaterialEditingLibrary
    color = editing.create_material_expression(asset, unreal.MaterialExpressionConstant3Vector, -250, 0)
    color.set_editor_property("constant", unreal.LinearColor(*rgb, 1.0))
    editing.connect_material_property(color, "", unreal.MaterialProperty.MP_BASE_COLOR)
    editing.recompile_material(asset)
    if not ASSETS.save_loaded_asset(asset):
        raise RuntimeError(f"Could not save {path}")
    return asset


def spawn(actor_type, label, position, rotation=(0, 0, 0)):
    actor = ACTORS.spawn_actor_from_class(actor_type, unreal.Vector(*position), unreal.Rotator(*rotation))
    actor.set_actor_label(label)
    return actor


def mesh(label, shape, position, scale, finish, tags=()):
    actor = spawn(unreal.StaticMeshActor, label, position)
    component = actor.static_mesh_component
    if tags:
        component.set_mobility(unreal.ComponentMobility.MOVABLE)
    component.set_static_mesh(MESHES[shape])
    component.set_material(0, finish)
    actor.set_actor_scale3d(unreal.Vector(*scale))
    actor.set_editor_property("tags", [unreal.Name(tag) for tag in tags])


def camera(tag, offset_x):
    position = unreal.Vector(offset_x - 720, -1020, 710)
    focus = unreal.Vector(offset_x, 0, 85)
    facing = unreal.MathLibrary.find_look_at_rotation(position, focus)
    actor = ACTORS.spawn_actor_from_class(unreal.CameraActor, position, facing)
    actor.set_actor_label(tag)
    actor.set_editor_property("tags", [unreal.Name(tag)])


def save(name):
    if not LEVELS.save_current_level():
        raise RuntimeError(f"Could not save {name}")
    unreal.log(f"WORLD_MAP_GENERATED {name}")


def main():
    finishes = {name: material(name, rgb) for name, rgb in MATERIALS.items()}
    begin("Town")
    camera("TownCamera", 0)
    camera("ForestCamera", 2200)
    sun = spawn(unreal.DirectionalLight, "Sun", (0, 0, 450))
    sun.set_actor_rotation(unreal.MathLibrary.find_look_at_rotation(
        unreal.Vector(0, -360, 450), unreal.Vector(0, 0, 0)), False)
    sun.get_component_by_class(unreal.DirectionalLightComponent).set_mobility(unreal.ComponentMobility.MOVABLE)
    mesh("Town ground", "Cube", (0, 0, -30), (15, 12, 0.5), finishes["TownFloor"])
    mesh("Town road", "Cube", (0, 20, -2), (13, 2.7, 0.1), finishes["Track"])
    for index, (x, y, width) in enumerate(((-240, 290, 2.6), (70, 300, 2.1), (350, 235, 2.7))):
        mesh(f"House {index}", "Cube", (x, y, 115), (width, 2.5, 2.4), finishes["TownWall"])
        mesh(f"Roof {index}", "Cone", (x, y, 265), (width * 1.3, 3.8, 1.9), finishes["TownRoof"])
    save("Town")

    begin("Forest")
    mesh("Forest ground", "Cube", (2200, 0, -30), (15, 12, 0.5), finishes["ForestFloor"])
    mesh("Forest track", "Cube", (2200, 20, -2), (13, 2.7, 0.1), finishes["Track"])
    layout = random.Random(73)
    for index in range(48):
        x = 2200 + layout.randint(-680, 680)
        y = layout.randint(175, 550) if index % 4 else layout.randint(-535, -200)
        height = layout.uniform(0.75, 1.25)
        mesh(f"Trunk {index}", "Cube", (x, y, 75 * height), (0.23, 0.23, 1.5 * height), finishes["Trunk"])
        mesh(f"Pine {index}", "Cone", (x, y, 190 * height), (1.6, 1.6, 2.5 * height), finishes["Pine"])
    mesh("Wolf", "Sphere", (2200, 20, 42), (1.20, 0.62, 0.67), finishes["Wolf"], ("WolfPresentation",))
    save("Forest")


main()
