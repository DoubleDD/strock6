import math

import FreeCAD as App
import Part
import Sketcher

DOC_NAME = "LowerRingClampPrototype"
OUTPUT_PATH = "/Volumes/code/com.github/Telescope_Project/strock6/cad/02_PrimarySupport/Parts/LowerRingClampPrototype.FCStd"
BOARD_THICK = 16.0
HOLE_DIAMETER = 12.2
HOLE_DEPTH = 25.0
OLD_VERTEX_DIAMETER = 259.06814756944357
CLAMP_LENGTH = 25.0
CLAMP_WIDTH = 20.0
OLD_APOTHEM = OLD_VERTEX_DIAMETER / 2 * math.cos(math.radians(22.5))
NEW_CIRCUMRADIUS = OLD_VERTEX_DIAMETER / 2 + CLAMP_WIDTH / math.cos(math.radians(22.5))


def add_block(sketch, geometry_index):
    sketch.addConstraint(Sketcher.Constraint("Block", geometry_index))


def add_rectangle(sketch, x, y, width, height):
    points = [
        App.Vector(x, y, 0),
        App.Vector(x + width, y, 0),
        App.Vector(x + width, y + height, 0),
        App.Vector(x, y + height, 0),
    ]
    for index in range(4):
        geometry_index = sketch.addGeometry(
            Part.LineSegment(points[index], points[(index + 1) % 4]), False
        )
        add_block(sketch, geometry_index)


def make_top_sketch(body, name, label):
    sketch = body.newObject("Sketcher::SketchObject", name)
    sketch.Label = label
    sketch.Placement = App.Placement(
        App.Vector(0, 0, BOARD_THICK), App.Rotation()
    )
    return sketch


def set_tip(body, feature, base_feature=None):
    if base_feature is not None:
        feature.BaseFeature = base_feature
    body.Tip = feature


def assert_recompute(doc, feature=None):
    doc.recompute()
    invalid = [
        obj.Name
        for obj in doc.Objects
        if "Invalid" in obj.State or "Error" in obj.State
    ]
    if invalid:
        raise RuntimeError("重算失败: " + ", ".join(invalid))
    if feature is not None:
        if feature.Shape.isNull() or not feature.Shape.isValid():
            raise RuntimeError("无效实体: " + feature.Name)


def make_pad(doc, body, sketch, name, label):
    pad = body.newObject("PartDesign::Pad", name)
    pad.Label = label
    pad.Profile = sketch
    pad.Length = BOARD_THICK
    pad.Reversed = True
    pad.setExpression("Length", "Params.board_thick")
    set_tip(body, pad)
    assert_recompute(doc, pad)
    return pad


def make_angled_hole(doc, body, name, label, center, upward, previous_volume):
    sketch = body.newObject("Sketcher::SketchObject", name)
    sketch.Label = label + "草图"
    rotation = App.Rotation(App.Vector(0, 0, 1), upward)
    sketch.Placement = App.Placement(center, rotation)
    geometry_index = sketch.addGeometry(
        Part.Circle(App.Vector(0, 0, 0), App.Vector(0, 0, 1), HOLE_DIAMETER / 2),
        False,
    )
    add_block(sketch, geometry_index)
    base_feature = body.Tip
    pocket = body.newObject("PartDesign::Pocket", name + "Pocket")
    pocket.Label = label + "（向边中点收拢）"
    pocket.Profile = sketch
    pocket.Length = HOLE_DEPTH
    pocket.Type = "Length"
    pocket.UseCustomVector = True
    pocket.Direction = upward.negative()
    pocket.setExpression("Length", "Params.rod_hole_depth")
    set_tip(body, pocket, base_feature)
    assert_recompute(doc, pocket)
    removed = previous_volume - pocket.Shape.Volume
    if removed <= 1e-6:
        raise RuntimeError("斜孔未实际去料: " + pocket.Name)
    return removed


def make_params(doc):
    sheet = doc.addObject("Spreadsheet::Sheet", "Params")
    sheet.Label = "下环夹块试验参数表"
    sheet.set("A1", "别名")
    sheet.set("B1", "值")
    sheet.set("C1", "说明")
    rows = [
        ("board_thick", "16 mm", "板厚 M-01"),
        ("rod_hole_d", "12.2 mm", "桁架杆孔径 T-01"),
        ("rod_hole_depth", "25 mm", "沿杆轴孔深"),
        ("inner_bore_d", "197.5 mm", "主镜座套合孔当前三档值"),
        ("old_oct_vertex_d", "259.06814756944357 mm", "原八角环实际外接圆直径"),
        ("clamp_length", "25 mm", "用户指定夹块长"),
        ("clamp_width", "20 mm", "用户指定夹块宽"),
        ("lower_hole_spacing", "=clamp_length", "两孔圆心位于长边两端"),
        ("old_apothem", "=old_oct_vertex_d / 2 * cos(22.5 deg)", "原实际外边内切半径"),
        ("new_oct_vertex_d", "=old_oct_vertex_d + 2 * clamp_width / cos(22.5 deg)", "外置缺口后的外接圆直径"),
        ("upper_rod_center_r", "108.75 mm", "当前 M 杆上端基准半径"),
        ("joint_radial_inset", "4.5 mm", "当前上接头径向内缩"),
        ("upper_tangent_offset", "9 mm", "当前上接头切向错位"),
        ("lower_tangent_offset", "=clamp_length / 2", "下端孔切向偏移"),
        ("rod_length", "1250 mm", "铝杆成品长度"),
        ("radial_inward", "39.594036563135 mm", "向上径向内收分量"),
        ("tangent_to_center", "79.851920908019 mm", "向上向边中点分量"),
        ("transverse_offset", "89.129215210633 mm", "完整横向偏移"),
        ("axial_span", "=sqrt(rod_length^2 - transverse_offset^2)", "杆端竖向跨度"),
        ("rod_tilt_total", "=atan(transverse_offset / axial_span)", "总倾角 4.088852°"),
        ("rod_tilt_radial", "=atan(radial_inward / axial_span)", "径向分量 1.818877°"),
        ("rod_tilt_tangent", "=atan(tangent_to_center / axial_span)", "向边中点切向分量 3.664478°"),
    ]
    for row, (alias, value, note) in enumerate(rows, 2):
        sheet.set(f"A{row}", alias)
        sheet.set(f"B{row}", value)
        sheet.set(f"C{row}", note)
        sheet.setAlias(f"B{row}", alias)
    return sheet


def build():
    if DOC_NAME in App.listDocuments():
        App.closeDocument(DOC_NAME)
    doc = App.newDocument(DOC_NAME)
    doc.Label = "下环夹块倾斜孔试验"
    make_params(doc)

    ring = doc.addObject("PartDesign::Body", "LowerRingBody")
    ring.Label = "八角环（带夹块缺口）"
    ring_profile = make_top_sketch(ring, "RingProfile", "八角环外形与套合孔草图")
    vertices = [
        App.Vector(
            NEW_CIRCUMRADIUS * math.cos(math.radians(22.5 + 45 * index)),
            NEW_CIRCUMRADIUS * math.sin(math.radians(22.5 + 45 * index)),
            0,
        )
        for index in range(8)
    ]
    for index in range(8):
        geometry_index = ring_profile.addGeometry(
            Part.LineSegment(vertices[index], vertices[(index + 1) % 8]), False
        )
        add_block(ring_profile, geometry_index)
    geometry_index = ring_profile.addGeometry(
        Part.Circle(App.Vector(0, 0, 0), App.Vector(0, 0, 1), 197.5 / 2), False
    )
    add_block(ring_profile, geometry_index)
    ring_pad = make_pad(doc, ring, ring_profile, "RingPad", "八角环板体拉伸")

    notches = make_top_sketch(ring, "ClampNotches", "四个夹块缺口草图（25×20）")
    new_apothem = OLD_APOTHEM + CLAMP_WIDTH
    for x, y, width, height in [
        (OLD_APOTHEM, -CLAMP_LENGTH / 2, CLAMP_WIDTH, CLAMP_LENGTH),
        (-CLAMP_LENGTH / 2, OLD_APOTHEM, CLAMP_LENGTH, CLAMP_WIDTH),
        (-new_apothem, -CLAMP_LENGTH / 2, CLAMP_WIDTH, CLAMP_LENGTH),
        (-CLAMP_LENGTH / 2, -new_apothem, CLAMP_LENGTH, CLAMP_WIDTH),
    ]:
        add_rectangle(notches, x, y, width, height)
    notch_pocket = ring.newObject("PartDesign::Pocket", "ClampNotchPocket")
    notch_pocket.Label = "四个夹块缺口切透"
    notch_pocket.Profile = notches
    notch_pocket.Type = "ThroughAll"
    notch_pocket.Length = BOARD_THICK
    set_tip(ring, notch_pocket, ring_pad)
    assert_recompute(doc, notch_pocket)

    clamp = doc.addObject("PartDesign::Body", "ClampBody")
    clamp.Label = "夹块（25×20×16）"
    clamp_profile = make_top_sketch(clamp, "ClampProfile", "夹块外形草图（25×20）")
    add_rectangle(
        clamp_profile,
        OLD_APOTHEM,
        -CLAMP_LENGTH / 2,
        CLAMP_WIDTH,
        CLAMP_LENGTH,
    )
    clamp_pad = make_pad(doc, clamp, clamp_profile, "ClampPad", "夹块板体拉伸")

    upper_radius = 108.75 - 4.5
    upper_angle = math.radians(-45)
    upper_x = upper_radius * math.cos(upper_angle) - 9 * math.sin(upper_angle)
    upper_y = upper_radius * math.sin(upper_angle) + 9 * math.cos(upper_angle)
    radial_inward = -(upper_x - OLD_APOTHEM)
    tangent_to_center = -(upper_y - CLAMP_LENGTH / 2)
    axial_span = math.sqrt(1250**2 - radial_inward**2 - tangent_to_center**2)

    removed_volumes = {}
    for side in range(4):
        side_angle = math.radians(side * 90)
        radial = App.Vector(math.cos(side_angle), math.sin(side_angle), 0)
        tangent = App.Vector(-math.sin(side_angle), math.cos(side_angle), 0)
        for pair_index, tangent_sign in enumerate((1, -1), 1):
            center = App.Vector(0, 0, BOARD_THICK).add(
                radial * OLD_APOTHEM + tangent * (tangent_sign * CLAMP_LENGTH / 2)
            )
            upward = (
                radial * (-radial_inward)
                + tangent * (-tangent_to_center * tangent_sign)
                + App.Vector(0, 0, axial_span)
            ).normalize()
            ring_name = f"RingHole{side * 2 + pair_index:02d}"
            removed_volumes[ring_name] = make_angled_hole(
                doc,
                ring,
                ring_name,
                f"八角环斜孔{side * 2 + pair_index:02d}",
                center,
                upward,
                ring.Shape.Volume,
            )
            if side == 0:
                clamp_name = f"ClampHole{pair_index:02d}"
                removed_volumes[clamp_name] = make_angled_hole(
                    doc,
                    clamp,
                    clamp_name,
                    f"夹块半圆斜槽{pair_index:02d}",
                    center,
                    upward,
                    clamp.Shape.Volume,
                )

    for obj in doc.Objects:
        if obj.TypeId == "App::Origin":
            obj.Label = "原点坐标系"
        elif obj.TypeId == "App::Line":
            obj.Label = ("X" if obj.Name.startswith("X_") else "Y" if obj.Name.startswith("Y_") else "Z") + "基准轴"
        elif obj.TypeId == "App::Plane":
            obj.Label = obj.Name.split("_")[0] + "基准面"
        elif obj.TypeId == "App::Point":
            obj.Label = "原点"
        obj.Visibility = False
    for body in (ring, clamp):
        body.Visibility = True
        body.Tip.Visibility = True
    clamp.ViewObject.ShapeColor = (0.85, 0.55, 0.20)
    doc.recompute()
    doc.saveAs(OUTPUT_PATH)
    if App.GuiUp:
        import FreeCADGui as Gui

        Gui.activeDocument().activeView().viewIsometric()
        Gui.activeDocument().activeView().fitAll()
        doc.save()
    return {
        "document": doc.Name,
        "path": doc.FileName,
        "bodies": [body.Name for body in (ring, clamp)],
        "volumes": {body.Name: body.Shape.Volume for body in (ring, clamp)},
        "solids": {body.Name: len(body.Shape.Solids) for body in (ring, clamp)},
        "removed_volumes": removed_volumes,
        "radial_inward": radial_inward,
        "tangent_to_center": tangent_to_center,
        "axial_span": axial_span,
        "total_tilt_deg": math.degrees(math.atan2(math.hypot(radial_inward, tangent_to_center), axial_span)),
        "radial_tilt_deg": math.degrees(math.atan2(radial_inward, axial_span)),
        "tangent_tilt_deg": math.degrees(math.atan2(tangent_to_center, axial_span)),
    }


_result_ = build()
