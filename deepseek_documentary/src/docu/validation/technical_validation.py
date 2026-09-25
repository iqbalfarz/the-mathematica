"""Static checks: every scene class exists, and scene code uses exactly the script's beats."""
from __future__ import annotations

import ast
import importlib

from ..paths import ROOT
from ..script import load_script


def check():
    issues = []
    by_module = {}
    for s in load_script():
        by_module.setdefault(s.act, []).append(s)
    for act, specs in sorted(by_module.items()):
        path = ROOT / "src/docu/scenes" / f"act{act:02d}.py"
        try:
            mod = importlib.import_module(f"docu.scenes.act{act:02d}")
        except Exception as e:  # pragma: no cover
            issues.append(f"act{act:02d}: import failed: {e}")
            continue
        tree = ast.parse(path.read_text())
        classes = {n.name: n for n in tree.body if isinstance(n, ast.ClassDef)}
        for s in specs:
            if not hasattr(mod, s.cls):
                issues.append(f"{s.id}: class {s.cls} missing in {path.name}")
                continue
            if getattr(getattr(mod, s.cls), "SCENE_ID", None) != s.id:
                issues.append(f"{s.id}: {s.cls}.SCENE_ID mismatch")
            used = [c.args[0].value for c in ast.walk(classes[s.cls]) if isinstance(c, ast.Call)
                    and getattr(c.func, "attr", "") == "beat" and c.args and isinstance(c.args[0], ast.Constant)]
            has_loop = any(isinstance(c, ast.For) for c in ast.walk(classes[s.cls]))
            want = [b.id for b in s.beats]
            if not has_loop and used != want:
                issues.append(f"{s.id}: code beats {used} != script beats {want}")
    return issues
