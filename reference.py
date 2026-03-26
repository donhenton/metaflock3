# ── reference.py ──────────────────────────────────────────────────────────────
import bpy
import random
import config


def setup_reference_objects():
    """
    Add a floor plane and scattered monolith boxes to the scene.
    Gives the camera spatial anchors and gives agents something to fly past.
    """
    _add_floor()
    _add_monoliths(config.MONOLITH_COUNT)
    print(f"[reference] floor + {config.MONOLITH_COUNT} monoliths added.")


def _add_floor():
    bpy.ops.mesh.primitive_plane_add(size=config.FLOOR_SIZE, location=(0, 0, config.FLOOR_Z))
    floor = bpy.context.active_object
    floor.name = "Floor"

    mat = bpy.data.materials.new("FloorMat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()

    out  = nodes.new("ShaderNodeOutputMaterial")
    bsdf = nodes.new("ShaderNodeBsdfDiffuse")
    bsdf.inputs["Color"].default_value     = (0.08, 0.08, 0.10, 1.0)  # near-black cool grey
    bsdf.inputs["Roughness"].default_value = 1.0
    mat.node_tree.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])

    floor.data.materials.append(mat)
    return floor


def _add_monoliths(count):
    """Scatter dark upright boxes at random positions around the floor."""
    mat = bpy.data.materials.new("MonolithMat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    out  = nodes.new("ShaderNodeOutputMaterial")
    bsdf = nodes.new("ShaderNodeBsdfDiffuse")
    bsdf.inputs["Color"].default_value     = (0.05, 0.07, 0.09, 1.0)
    bsdf.inputs["Roughness"].default_value = 1.0
    mat.node_tree.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])

    spread = config.FLOOR_SIZE * 0.38
    for i in range(count):
        x = random.uniform(-spread, spread)
        y = random.uniform(-spread, spread)
        h = random.uniform(1.5, 4.0)
        w = random.uniform(0.3, 0.7)

        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, y, config.FLOOR_Z + h * 0.5))
        m = bpy.context.active_object
        m.name = f"Monolith_{i}"
        m.scale = (w, w, h)
        bpy.ops.object.transform_apply(scale=True)
        m.data.materials.append(mat)
