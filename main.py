import bpy
import os
import sys
import importlib

# ── path bootstrap ────────────────────────────────────────────────────────────
_dir = os.path.dirname(bpy.context.space_data.text.filepath)
print(f"[metaflock] root: {_dir}")
if _dir not in sys.path:
    sys.path.append(_dir)

# ── module reloads (dev loop — edit any file, re-run main.py) ─────────────────
import config
import scene
import materials
import metaballs
import flock
import camera
import reference
import behaviors
import behaviors.boids
import behaviors.lavalamp

for _mod in (
    config, scene, materials, metaballs,
    flock, camera, reference,
    behaviors, behaviors.boids, behaviors.lavalamp,
):
    importlib.reload(_mod)

# ── imports ───────────────────────────────────────────────────────────────────
from scene      import clear_scene, setup_camera, setup_light, setup_render_settings, setup_world_background
from materials  import create_flat_green_material, apply_material
from metaballs  import create_metaball_object, add_metaball_element, sync_metaballs_to_flock, keyframe_flock
from flock      import init_flock, step_flock
from camera     import lazy_track_camera, reset_camera_target
from reference  import setup_reference_objects
from behaviors.boids    import boids
from behaviors.lavalamp import LavaLamp


# ── swap behavior here ────────────────────────────────────────────────────────
BEHAVIOR = boids          # boids  or  LavaLamp()


def run(behavior=None):
    behavior = behavior or BEHAVIOR

    # scene
    clear_scene()
    setup_render_settings()
    setup_world_background()
    cam = setup_camera()
    setup_light()
    setup_reference_objects()

    # metaballs
    mb_obj, mb_data = create_metaball_object("MetaFlock")
    mat = create_flat_green_material()
    apply_material(mb_obj, mat)

    # flock
    fl = init_flock(config.N_AGENTS, behavior)

    # seed one metaball element per agent
    for agent in fl.agents:
        add_metaball_element(mb_data, agent.position, agent.radius, agent.stiffness)

    # bake
    reset_camera_target()
    _bake(cam, mb_data, fl)

    print("[metaflock] done.")


def _bake(cam, mb_data, fl):
    scene_ref = bpy.context.scene
    for frame in range(config.FRAME_START, config.FRAME_END + 1):
        scene_ref.frame_set(frame)
        step_flock(fl)
        sync_metaballs_to_flock(mb_data, fl)
        keyframe_flock(mb_data, frame)
        lazy_track_camera(cam, fl, frame)

    scene_ref.frame_set(config.FRAME_START)
    print(f"[metaflock] baked {config.FRAME_END - config.FRAME_START + 1} frames.")


# ── entry point ───────────────────────────────────────────────────────────────
run()
