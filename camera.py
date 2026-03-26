# ── camera.py ─────────────────────────────────────────────────────────────────
import bpy
import config
from mathutils import Vector


# internal state — persists across frames during bake
_current_target = None


def lazy_track_camera(cam_obj, flock, frame):
    """
    Lerp camera aim toward flock centroid rather than snapping.
    CAM_LERP controls lag — 0.0 = never moves, 1.0 = instant snap.
    Low values (0.03–0.06) give a heavy, drifting feel that reads motion.
    """
    global _current_target

    centroid = flock.centroid

    if _current_target is None:
        _current_target = Vector(centroid)

    # lerp toward centroid
    _current_target = _current_target.lerp(centroid, config.CAM_LERP)

    direction = _current_target - Vector(cam_obj.location)
    if direction.length > 0:
        rot_quat = direction.to_track_quat('-Z', 'Y')
        cam_obj.rotation_euler = rot_quat.to_euler()
        cam_obj.keyframe_insert(data_path="rotation_euler", frame=frame)


def reset_camera_target():
    """Call before each bake to clear stale state."""
    global _current_target
    _current_target = None
