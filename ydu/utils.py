import os
import string
from pathlib import Path
from typing import List


def discover_roots() -> List[Path]:
    roots = []
    if os.name == "nt":
        for letter in string.ascii_uppercase:
            drive = Path(f"{letter}:/")
            if drive.exists():
                roots.append(drive)
    else:
        roots.append(Path("/"))
        home = Path.home()
        if home not in roots:
            roots.append(home)
    return roots


def print_plan(plan: List[str]) -> None:
    print("PLAN")
    for i, step in enumerate(plan, 1):
        print(f"{i}. {step}")


def confirm(prompt: str = "Proceed? [y/N] ") -> bool:
    try:
        return input(prompt).strip().lower() == "y"
    except EOFError:
        return False
