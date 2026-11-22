"""Author the eight distinct forest chunks in a disposable Unreal Python project."""

import random

import unreal


CHUNK_COUNT = 8
TREES_PER_CHUNK = 384
LEVELS = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
ACTORS = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
MESHES = {name: unreal.load_asset(f"/Engine/BasicShapes/{name}") for name in ("Cube", "Cone")}
MATERIALS = {name: unreal.load_asset(f"/Game/Materials/{name}")
             for name in ("ForestFloor", "Track", "Trunk", "Pine", "TownRoof", "TownWall")}


def mesh(shape, finish, x, y, z, scale, yaw=0):
    actor = ACTORS.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(x, y, z), unreal.Rotator(0, 0, yaw))
    component = actor.static_mesh_component
    component.set_static_mesh(MESHES[shape])
    component.set_material(0, MATERIALS[finish])
    component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
    actor.set_actor_scale3d(unreal.Vector(*scale))


def main():
    if not all(MESHES.values()) or not all(MATERIALS.values()):
        raise RuntimeError("Copy the small example Content/Materials directory into this project first.")
    for index in range(CHUNK_COUNT):
        name = f"/Game/Maps/Scale/Chunk{index}"
        if not LEVELS.new_level(name):
            raise RuntimeError(f"Could not create {name} in the disposable project.")
        center = 12000 + 6500 * index
        mesh("Cube", "ForestFloor", center, 0, -27, (64, 50, 0.5))
        mesh("Cube", "Track", center, 0, -3, (64, 7, 0.10))
        mesh("Cube", "TownWall", center + 310, 405, 80, (0.6, 0.6, 1.6))
        mesh("Cone", "TownRoof", center + 310, 405, 195, (1.8 + index * 0.1, 1.8, 1.4), index * 13)
        layout = random.Random(40007 + index * 101)
        for tree in range(TREES_PER_CHUNK):
            side = -1 if tree % 2 else 1
            x = center + layout.randrange(-3090, 3091)
            y = side * layout.randrange(450, 2420)
            height = layout.uniform(0.62, 1.55)
            width = layout.uniform(0.75, 1.30)
            mesh("Cube", "Trunk", x, y, 77 * height, (0.22, 0.22, 1.54 * height), tree % 90)
            mesh("Cone", "Pine", x, y, 188 * height, (1.5 * width, 1.5 * width, 2.65 * height), tree % 90)
        if not LEVELS.save_current_level():
            raise RuntimeError(f"Could not save {name}")
        unreal.log(f"SCALE_MAP_GENERATED {name} trees={TREES_PER_CHUNK} geometryActors={4 + 2 * TREES_PER_CHUNK}")


main()
