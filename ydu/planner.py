from pathlib import Path
from typing import List


def build_plan(intent, roots: List[Path]) -> List[str]:
    plan = []
    roots_str = ", ".join(str(r) for r in roots)
    plan.append(f"discover roots: {roots_str}")
    plan.append(f"search for *.{intent['extension']}")
    if intent["type"] == "move_by_extension":
        dest = intent["destination"]
        plan.append(f"ensure destination: {dest}")
        plan.append(f"move files to: {dest}")
    return plan
