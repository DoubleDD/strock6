#!/usr/bin/env python3
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET

import FreeCAD as App
import FreeCADGui as Gui


def saved_visibility(path):
    with ZipFile(path) as archive:
        root = ET.fromstring(archive.read("Document.xml"))
    object_data = root.find("ObjectData")
    if object_data is None:
        raise RuntimeError(f"Document.xml 缺少 ObjectData：{path}")
    result = {}
    for obj in object_data.findall("Object"):
        value = obj.find("./Properties/Property[@name='Visibility']/Bool")
        if value is not None:
            result[obj.attrib["name"]] = value.attrib.get("value") == "true"
    return result


def has_assembly_links(path):
    with ZipFile(path) as archive:
        root = ET.fromstring(archive.read("Document.xml"))
    objects = root.find("Objects")
    if objects is None:
        raise RuntimeError(f"Document.xml 缺少 Objects：{path}")
    return any(
        obj.attrib.get("type") == "App::Link"
        for obj in objects.findall("Object")
    )


def geometry_signature(obj):
    if obj.TypeId in ("App::DocumentObjectGroup", "Assembly::AssemblyObject", "App::Link"):
        return None
    if not hasattr(obj, "Shape"):
        return None
    shape = obj.Shape
    if shape.isNull():
        return ("null",)
    return (
        shape.ShapeType,
        len(shape.Solids),
        len(shape.Faces),
        len(shape.Edges),
        round(shape.Volume, 5),
        round(shape.Area, 5),
        tuple(round(value, 5) for value in shape.CenterOfMass)
        if hasattr(shape, "CenterOfMass")
        else None,
    )


def document_signature(doc):
    return {
        obj.Name: (obj.TypeId, obj.Label, geometry_signature(obj))
        for obj in doc.Objects
    }


def error_states(doc):
    return {
        obj.Name: tuple(obj.State)
        for obj in doc.Objects
        if any(state in ("Invalid", "Error") for state in obj.State)
    }


def set_visibility(obj, desired):
    obj.Visibility = desired
    if obj.ViewObject:
        obj.ViewObject.Visibility = desired


def expected_visibility(doc, initial):
    expected = {obj.Name: initial.get(obj.Name, obj.Visibility) for obj in doc.Objects}
    for obj in doc.Objects:
        if obj.TypeId == "App::Link":
            expected[obj.Name] = True
        elif obj.TypeId == "PartDesign::Body":
            expected[obj.Name] = True
            tip = obj.Tip
            for child in obj.Group:
                expected[child.Name] = child == tip
        elif obj.TypeId == "App::Origin":
            expected[obj.Name] = False
            for child in obj.OriginFeatures:
                expected[child.Name] = False
    return expected


def apply_visibility(doc, expected):
    for obj in doc.Objects:
        if obj.TypeId not in ("App::Link", "PartDesign::Body") and obj.Name in expected:
            set_visibility(obj, expected[obj.Name])
    for obj in doc.Objects:
        if obj.TypeId == "PartDesign::Body":
            set_visibility(obj, True)
            for child in obj.Group:
                set_visibility(child, child == obj.Tip)
    for obj in doc.Objects:
        if obj.TypeId == "App::Link":
            set_visibility(obj, True)
    for obj in doc.Objects:
        if obj.TypeId == "App::Origin":
            set_visibility(obj, False)
            for child in obj.OriginFeatures:
                set_visibility(child, False)


def visibility_problems(doc, expected):
    problems = []
    for obj in doc.Objects:
        if obj.Name not in expected:
            continue
        view_value = obj.ViewObject.Visibility if obj.ViewObject else obj.Visibility
        if obj.Visibility != expected[obj.Name] or view_value != expected[obj.Name]:
            problems.append(
                f"{obj.Name}: 期望={expected[obj.Name]}, "
                f"App={obj.Visibility}, View={view_value}"
            )
    return problems


def model_problems(doc, expected):
    problems = visibility_problems(doc, expected)
    for obj in doc.Objects:
        if obj.TypeId == "App::Link" and obj.LinkedObject is None:
            problems.append(f"断链:{obj.Name}")
        if obj.TypeId == "PartDesign::Body" and not obj.Shape.isNull():
            if not obj.Shape.isValid():
                problems.append(f"无效 Body:{obj.Name}")
        if obj.TypeId == "Sketcher::SketchObject":
            if obj.ConflictingConstraints:
                problems.append(f"草图冲突:{obj.Name}")
            if obj.RedundantConstraints:
                problems.append(f"草图冗余:{obj.Name}")
    return problems


def open_document(path, managed_names, expected_names):
    def loaded(doc):
        names = {obj.Name for obj in doc.Objects}
        return bool(names) and expected_names <= names

    existing = next(
        (
            doc
            for doc in App.listDocuments().values()
            if doc.FileName and Path(doc.FileName) == path
        ),
        None,
    )
    if existing is not None:
        if existing.Name not in managed_names:
            raise RuntimeError(f"目标文档已在 GUI 中打开，请先关闭：{path}")
        if loaded(existing):
            return existing
        App.closeDocument(existing.Name)
    for _ in range(3):
        before = set(App.listDocuments())
        doc = App.openDocument(str(path))
        managed_names.update(set(App.listDocuments()) - before)
        managed_names.add(doc.Name)
        if loaded(doc):
            return doc
        App.closeDocument(doc.Name)
    raise RuntimeError(f"文档多次打开后仍未完整载入，已停止处理：{path}")


def close_document(doc):
    if doc is None:
        return
    try:
        name = doc.Name
    except (ReferenceError, RuntimeError):
        return
    if name in App.listDocuments():
        App.closeDocument(name)


def process_document(path, root, managed_names):
    doc = None
    initial = saved_visibility(path)
    try:
        doc = open_document(path, managed_names, set(initial))
        doc.recompute(None, True, True)
        if not doc.Objects:
            raise RuntimeError("文档重算后仍为空，等待重新载入")
        baseline = document_signature(doc)
        baseline_errors = error_states(doc)
        expected = expected_visibility(doc, initial)
        apply_visibility(doc, expected)
        doc.recompute(None, True, True)
        updated = document_signature(doc)
        if updated != baseline:
            changed = [name for name in baseline if baseline[name] != updated.get(name)]
            raise RuntimeError(f"保存前文档或几何变化：{changed}")
        if error_states(doc) != baseline_errors:
            raise RuntimeError("保存前重算错误状态变化")
        problems = model_problems(doc, expected)
        if problems:
            raise RuntimeError("保存前检查：" + "；".join(problems[:12]))

        doc.save()
        Gui.getDocument(doc.Name).save()
        with ZipFile(path) as archive:
            if archive.testzip() is not None or "GuiDocument.xml" not in archive.namelist():
                raise RuntimeError("ZIP 或 GuiDocument.xml 检查失败")

        close_document(doc)
        doc = open_document(path, managed_names, set(initial))
        doc.recompute(None, True, True)
        if not doc.Objects:
            raise RuntimeError("重开后文档仍为空，等待重新载入")
        reopened = document_signature(doc)
        if reopened != baseline:
            changed = [name for name in baseline if baseline[name] != reopened.get(name)]
            added = sorted(set(reopened) - set(baseline))
            removed = sorted(set(baseline) - set(reopened))
            raise RuntimeError(
                f"重开后文档或几何变化：变化={changed}，新增={added}，删除={removed}"
            )
        if error_states(doc) != baseline_errors:
            raise RuntimeError("重开后重算错误状态变化")
        problems = model_problems(doc, expected)
        if problems:
            raise RuntimeError("重开后检查：" + "；".join(problems[:12]))
        print(f"已验证 {path.relative_to(root)}，对象 {len(doc.Objects)} 个", flush=True)
    finally:
        close_document(doc)


def main(project_root=None, relative_paths=None):
    if not App.GuiUp:
        raise RuntimeError("必须在 FreeCAD GUI 中运行，才能保存 GuiDocument.xml 视图状态")
    root = (
        Path(project_root).resolve()
        if project_root is not None
        else Path(__file__).resolve().parents[2]
    )
    if relative_paths:
        paths = [root / path for path in relative_paths]
    else:
        paths = [*root.glob("cad/**/*.FCStd"), *root.glob("tests/fixtures/cad/**/*.FCStd")]
    paths = sorted(
        paths,
        key=lambda path: (has_assembly_links(path), -len(path.parts), str(path)),
    )
    managed_names = set()
    failures = []
    try:
        for path in paths:
            for attempt in range(3):
                try:
                    process_document(path, root, managed_names)
                    break
                except Exception as exc:
                    load_error = "载入" in str(exc) or "deleted object" in str(exc)
                    if load_error and attempt < 2:
                        print(f"重新载入 {path.relative_to(root)}", flush=True)
                        continue
                    failures.append((str(path.relative_to(root)), str(exc)))
                    print(f"失败 {path.relative_to(root)}：{exc}", flush=True)
                    break
    finally:
        for name in sorted(managed_names, reverse=True):
            if name in App.listDocuments():
                App.closeDocument(name)
    print(f"批量可见性处理：{len(paths)} 份，失败 {len(failures)} 份", flush=True)
    if failures:
        raise RuntimeError(failures)
    return len(paths)


if __name__ == "__main__":
    main()
