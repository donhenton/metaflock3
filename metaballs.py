# ── metaballs.py ──────────────────────────────────────────────────────────────
import bpy
import config
from mathutils import Vector


def create_metaball_object(name="MetaFlock"):
    """
    Create a MetaBall datablock and parent object.
    Returns (object, metaball_data).
    """
    mb_data            = bpy.data.metaballs.new(name)
    mb_data.threshold  = config.MB_THRESHOLD
    mb_data.resolution = config.MB_RESOLUTION

    mb_obj = bpy.data.objects.new(name, mb_data)
    bpy.context.scene.collection.objects.link(mb_obj)

    print(f"[metaballs] '{name}' — threshold={config.MB_THRESHOLD}, resolution={config.MB_RESOLUTION}")
    return mb_obj, mb_data


def add_metaball_element(mb_data, location=(0, 0, 0), radius=None, stiffness=None):
    """Add a single element to an existing metaball datablock."""
    radius    = radius    or config.AGENT_RADIUS
    stiffness = stiffness or config.AGENT_STIFFNESS

    el           = mb_data.elements.new()
    el.co        = Vector(location)
    el.radius    = radius
    el.stiffness = stiffness
    return el


def sync_metaballs_to_flock(mb_data, flock):
    """Write agent state into metaball elements."""
    for el, agent in zip(mb_data.elements, flock.agents):
        el.co        = Vector(agent.position)
        el.radius    = agent.radius
        el.stiffness = agent.stiffness


def keyframe_flock(mb_data, frame):
    """Insert keyframes on all metaball elements at given frame."""
    for el in mb_data.elements:
        el.keyframe_insert(data_path="co",        frame=frame)
        el.keyframe_insert(data_path="radius",    frame=frame)
        el.keyframe_insert(data_path="stiffness", frame=frame)
