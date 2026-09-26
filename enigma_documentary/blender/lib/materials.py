"""Procedural materials (no image textures, so nothing to download and little RAM).

Palette follows design/H_visual_design_system.md: black crinkle paint, bakelite,
brass, steel, ivory, oak, copper; one warm emission colour for current.
"""
from __future__ import annotations

import bpy

SIGNAL = (1.0, 0.42, 0.08, 1.0)       # warm amber: electricity (saturated so AgX keeps the hue)
SIGNAL_RETURN = (1.0, 0.22, 0.04, 1.0)
LAMP_GLOW = (1.0, 0.50, 0.12, 1.0)      # saturated so AgX keeps it amber, not white
CORRECT = (0.30, 0.85, 0.45, 1.0)
REJECT = (0.95, 0.25, 0.22, 1.0)


def _new(name):
    m = bpy.data.materials.get(name)
    if m:
        return m, None
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    return m, m.node_tree


def _bsdf(nt):
    return nt.nodes["Principled BSDF"]


def _set(b, name, value):
    if name in b.inputs:
        b.inputs[name].default_value = value


def _noise_bump(nt, scale, strength, detail=8.0):
    tex = nt.nodes.new("ShaderNodeTexNoise")
    tex.inputs["Scale"].default_value = scale
    tex.inputs["Detail"].default_value = detail
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = strength
    bump.inputs["Distance"].default_value = 0.0005
    nt.links.new(tex.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], _bsdf(nt).inputs["Normal"])
    return tex


def _rough_variation(nt, lo, hi, scale):
    tex = nt.nodes.new("ShaderNodeTexNoise")
    tex.inputs["Scale"].default_value = scale
    ramp = nt.nodes.new("ShaderNodeMapRange")
    ramp.inputs["To Min"].default_value = lo
    ramp.inputs["To Max"].default_value = hi
    nt.links.new(tex.outputs["Fac"], ramp.inputs["Value"])
    nt.links.new(ramp.outputs["Result"], _bsdf(nt).inputs["Roughness"])


def crinkle_paint():
    m, nt = _new("MAT_crinkle_black")
    if nt:
        b = _bsdf(nt)
        _set(b, "Base Color", (0.008, 0.008, 0.009, 1))
        _set(b, "Specular IOR Level", 0.3)
        _noise_bump(nt, 900.0, 0.45)
        _rough_variation(nt, 0.62, 0.85, 40.0)
    return m


def bakelite():
    m, nt = _new("MAT_bakelite")
    if nt:
        b = _bsdf(nt)
        _set(b, "Base Color", (0.02, 0.014, 0.01, 1))
        _set(b, "Roughness", 0.28)
        _set(b, "Coat Weight", 0.3)
        _rough_variation(nt, 0.22, 0.4, 25.0)
    return m


def brass():
    m, nt = _new("MAT_brass")
    if nt:
        b = _bsdf(nt)
        _set(b, "Base Color", (0.78, 0.56, 0.26, 1))
        _set(b, "Metallic", 1.0)
        _rough_variation(nt, 0.22, 0.42, 60.0)
        _noise_bump(nt, 300.0, 0.08)
    return m


def steel():
    m, nt = _new("MAT_steel")
    if nt:
        b = _bsdf(nt)
        _set(b, "Base Color", (0.62, 0.62, 0.64, 1))
        _set(b, "Metallic", 1.0)
        _rough_variation(nt, 0.18, 0.35, 80.0)
    return m


def copper():
    m, nt = _new("MAT_copper")
    if nt:
        b = _bsdf(nt)
        _set(b, "Base Color", (0.85, 0.45, 0.28, 1))
        _set(b, "Metallic", 1.0)
        _set(b, "Roughness", 0.3)
    return m


def ivory():
    m, nt = _new("MAT_ivory")
    if nt:
        b = _bsdf(nt)
        _set(b, "Base Color", (0.86, 0.82, 0.70, 1))
        _set(b, "Roughness", 0.32)
        _set(b, "Subsurface Weight", 0.08)
        _set(b, "Coat Weight", 0.4)
        _rough_variation(nt, 0.25, 0.45, 30.0)
    return m


def ink():
    m, nt = _new("MAT_ink")
    if nt:
        b = _bsdf(nt)
        _set(b, "Base Color", (0.015, 0.015, 0.015, 1))
        _set(b, "Roughness", 0.6)
    return m


def engraved_white():
    """Painted letters. Invisible from behind: ring letters on the far side of a
    glass rotor would otherwise show through mirrored."""
    m, nt = _new("MAT_engraved_white")
    if nt:
        b = _bsdf(nt)
        _set(b, "Base Color", (0.82, 0.8, 0.74, 1))
        _set(b, "Roughness", 0.5)
        geo = nt.nodes.new("ShaderNodeNewGeometry")
        clear = nt.nodes.new("ShaderNodeBsdfTransparent")
        mix = nt.nodes.new("ShaderNodeMixShader")
        out = nt.nodes["Material Output"]
        nt.links.new(geo.outputs["Backfacing"], mix.inputs["Fac"])
        nt.links.new(b.outputs["BSDF"], mix.inputs[1])
        nt.links.new(clear.outputs["BSDF"], mix.inputs[2])
        nt.links.new(mix.outputs["Shader"], out.inputs["Surface"])
    return m


def oak():
    m, nt = _new("MAT_oak")
    if nt:
        b = _bsdf(nt)
        # Long grain: stretch coordinates along the board, then fine bands + slight distortion.
        coord = nt.nodes.new("ShaderNodeTexCoord")
        mapping = nt.nodes.new("ShaderNodeMapping")
        mapping.inputs["Scale"].default_value = (1.0, 1.0, 12.0)
        nt.links.new(coord.outputs["Object"], mapping.inputs["Vector"])
        wave = nt.nodes.new("ShaderNodeTexWave")
        wave.bands_direction = "Z"
        wave.inputs["Scale"].default_value = 18.0
        wave.inputs["Distortion"].default_value = 3.0
        wave.inputs["Detail"].default_value = 6.0
        wave.inputs["Detail Scale"].default_value = 1.5
        nt.links.new(mapping.outputs["Vector"], wave.inputs["Vector"])
        ramp = nt.nodes.new("ShaderNodeValToRGB")
        ramp.color_ramp.elements[0].color = (0.10, 0.055, 0.028, 1)
        ramp.color_ramp.elements[1].color = (0.24, 0.14, 0.07, 1)
        nt.links.new(wave.outputs["Fac"], ramp.inputs["Fac"])
        nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
        _set(b, "Roughness", 0.45)
        _set(b, "Coat Weight", 0.25)
    return m


def glass_dark():
    m, nt = _new("MAT_lamp_window")
    if nt:
        b = _bsdf(nt)
        _set(b, "Base Color", (0.10, 0.09, 0.08, 1))
        _set(b, "Roughness", 0.12)
        _set(b, "Coat Weight", 1.0)
    return m


def driven_emission(name, base_rgba, strength=12.0, dim=(0.10, 0.09, 0.08, 1)):
    """Emission scaled by the object's colour alpha-free RGB: animate `object.color`
    to switch it on and off per object while sharing one material.

    object.color = (1,1,1,1) -> full glow, (0,0,0,1) -> off.
    """
    m, nt = _new(name)
    if nt:
        b = _bsdf(nt)
        _set(b, "Base Color", dim)
        _set(b, "Roughness", 0.4)
        info = nt.nodes.new("ShaderNodeObjectInfo")
        mix = nt.nodes.new("ShaderNodeMix")
        mix.data_type = "RGBA"
        mix.blend_type = "MULTIPLY"
        mix.inputs["Factor"].default_value = 1.0
        mix.inputs[6].default_value = base_rgba          # A
        nt.links.new(info.outputs["Color"], mix.inputs[7])  # B
        nt.links.new(mix.outputs[2], b.inputs["Emission Color"])
        _set(b, "Emission Strength", strength)
    return m


def signal_material(name="MAT_signal", color=SIGNAL, strength=7.0):
    return driven_emission(name, color, strength, dim=(0.02, 0.015, 0.01, 1))


def translucent_core():
    """Rotor core shown as smoked glass when we look inside the wiring."""
    m, nt = _new("MAT_core_glass")
    if nt:
        b = _bsdf(nt)
        _set(b, "Base Color", (0.05, 0.04, 0.035, 1))
        _set(b, "Roughness", 0.2)
        _set(b, "Alpha", 0.25)
        if hasattr(m, "blend_method"):
            m.blend_method = "BLEND"
    return m


def all_materials() -> dict:
    return {"crinkle": crinkle_paint(), "bakelite": bakelite(), "brass": brass(), "steel": steel(),
            "copper": copper(), "ivory": ivory(), "ink": ink(), "white": engraved_white(), "oak": oak(),
            "lamp_window": glass_dark(),
            "lamp": driven_emission("MAT_lamp_letter", LAMP_GLOW, 14.0, dim=(0.012, 0.011, 0.010, 1)),
            "lamp_glass": driven_emission("MAT_lamp_glass", LAMP_GLOW, 1.2, dim=(0.16, 0.15, 0.13, 1)),
            "signal": signal_material(), "signal_return": signal_material("MAT_signal_return", SIGNAL_RETURN),
            "core_glass": translucent_core(),
            "wire_glow": driven_emission("MAT_wire_glow", SIGNAL, 6.0, dim=(0.55, 0.30, 0.18, 1)),
            "contact_glow": driven_emission("MAT_contact_glow", SIGNAL, 8.0, dim=(0.60, 0.45, 0.20, 1)),
            "label_glow": driven_emission("MAT_label_glow", SIGNAL, 8.0, dim=(0.55, 0.53, 0.48, 1))}
