# ── scene.py ──────────────────────────────────────────────────────────────────
import bpy
import config


def clear_scene():
    """Remove everything from the scene."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=True)

    for collection in (
        bpy.data.meshes,
        bpy.data.metaballs,
        bpy.data.cameras,
        bpy.data.lights,
        bpy.data.materials,
    ):
        for block in list(collection):
            collection.remove(block)

    print("[scene] cleared.")


def setup_camera(location=None):
    """Create camera at location. Pointing handled per-frame by camera.py."""
    location = location or config.CAM_LOCATION
    cam_data = bpy.data.cameras.new("Camera")
    cam_obj  = bpy.data.objects.new("Camera", cam_data)
    bpy.context.scene.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj
    cam_obj.location = location
    print(f"[scene] camera at {location}")
    return cam_obj


def setup_light(light_type=None, location=None, energy=None):
    """Add a light."""
    light_type = light_type or config.LIGHT_TYPE
    location   = location   or config.LIGHT_LOCATION
    energy     = energy     or config.LIGHT_ENERGY

    light_data        = bpy.data.lights.new("Light", type=light_type)
    light_data.energy = energy
    light_obj         = bpy.data.objects.new("Light", light_data)
    bpy.context.scene.collection.objects.link(light_obj)
    light_obj.location = location
    print(f"[scene] {light_type} light at {location}, energy={energy}")
    return light_obj


def setup_render_settings(fps=None, frame_start=None, frame_end=None):
    """Configure render engine, FPS, frame range, resolution."""
    fps         = fps         or config.FPS
    frame_start = frame_start or config.FRAME_START
    frame_end   = frame_end   or config.FRAME_END

    scene                   = bpy.context.scene
    scene.render.engine     = 'BLENDER_EEVEE_NEXT'
    scene.render.fps        = fps
    scene.frame_start       = frame_start
    scene.frame_end         = frame_end
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    print(f"[scene] EEVEE | {fps}fps | frames {frame_start}–{frame_end}")


def setup_world_background(
    noise_scale=None,
    wave_distortion=None,
    darkness=None,
):
    """
    Weird muted world background.
    Noise-distorted wave pattern through a dark teal-to-black colour ramp.
    Works in EEVEE — no sky texture dependency.
    """
    noise_scale     = noise_scale     or config.WORLD_NOISE_SCALE
    wave_distortion = wave_distortion or config.WORLD_WAVE_DISTORTION
    darkness        = darkness        or config.WORLD_DARKNESS

    world = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
    bpy.context.scene.world = world
    world.use_nodes = True

    nt = world.node_tree
    nt.nodes.clear()

    # nodes
    out     = nt.nodes.new("ShaderNodeOutputWorld")
    bg      = nt.nodes.new("ShaderNodeBackground")
    ramp    = nt.nodes.new("ShaderNodeValToRGB")
    wave    = nt.nodes.new("ShaderNodeTexWave")
    noise   = nt.nodes.new("ShaderNodeTexNoise")
    coord   = nt.nodes.new("ShaderNodeTexCoord")
    mix     = nt.nodes.new("ShaderNodeMixRGB")

    # layout
    coord.location   = (-800, 0)
    noise.location   = (-600, 0)
    wave.location    = (-400, 0)
    ramp.location    = (-180, 0)
    mix.location     = (20,   0)
    bg.location      = (220,  0)
    out.location     = (420,  0)

    # noise — distorts the wave
    noise.inputs["Scale"].default_value      = noise_scale
    noise.inputs["Detail"].default_value     = 8.0
    noise.inputs["Roughness"].default_value  = 0.65
    noise.inputs["Distortion"].default_value = 1.2

    # wave — organic banding
    wave.wave_type                           = 'BANDS'
    wave.inputs["Scale"].default_value       = 3.0
    wave.inputs["Distortion"].default_value  = wave_distortion
    wave.inputs["Detail"].default_value      = 6.0
    wave.inputs["Detail Scale"].default_value = 2.5

    # colour ramp — dark teal to near-black
    ramp.color_ramp.interpolation = 'B_SPLINE'
    ramp.color_ramp.elements[0].position = 0.0
    ramp.color_ramp.elements[0].color    = (0.04, 0.05, 0.07, 1.0)   # near black
    ramp.color_ramp.elements[1].position = 1.0
    ramp.color_ramp.elements[1].color    = (0.11, 0.18, 0.20, 1.0)   # muted teal

    # mix darkness — keep it brooding
    mix.blend_type                    = 'MULTIPLY'
    mix.inputs["Fac"].default_value   = 1.0
    mix.inputs["Color2"].default_value = (darkness, darkness, darkness, 1.0)

    # wire it up
    links = nt.links
    links.new(coord.outputs["Generated"],  noise.inputs["Vector"])
    links.new(coord.outputs["Generated"],  wave.inputs["Vector"])
    links.new(noise.outputs["Fac"],        wave.inputs["Distortion"])
    links.new(wave.outputs["Fac"],         ramp.inputs["Fac"])
    links.new(ramp.outputs["Color"],       mix.inputs["Color1"])
    links.new(mix.outputs["Color"],        bg.inputs["Color"])
    links.new(bg.outputs["Background"],    out.inputs["Surface"])

    bg.inputs["Strength"].default_value = 1.0

    print(f"[scene] world background set — noise={noise_scale}, distortion={wave_distortion}, darkness={darkness}")
