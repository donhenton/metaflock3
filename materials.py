# ── materials.py ──────────────────────────────────────────────────────────────
import bpy


def create_flat_green_material():
    """Flat green — no specular, no variation. Pops against the dark background."""
    mat = bpy.data.materials.new("FlatGreen")
    mat.use_nodes = True

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    out  = nodes.new("ShaderNodeOutputMaterial")
    bsdf = nodes.new("ShaderNodeBsdfDiffuse")
    bsdf.inputs["Color"].default_value     = (0.05, 0.6, 0.15, 1.0)
    bsdf.inputs["Roughness"].default_value = 1.0
    links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])

    print("[materials] flat green created.")
    return mat


def apply_material(obj, material):
    """Apply material to object, replacing any existing slot."""
    if obj.data.materials:
        obj.data.materials[0] = material
    else:
        obj.data.materials.append(material)
    print(f"[materials] '{material.name}' → '{obj.name}'")
