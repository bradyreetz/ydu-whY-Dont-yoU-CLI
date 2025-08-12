import os
import shutil
from pathlib import Path
from typing import List, Tuple


def find_files_by_extension(ext: str, roots: List[Path]) -> List[Path]:
    ext = ext.lower().lstrip(".")
    matches: List[Path] = []
    for root in roots:
        try:
            for dirpath, _, filenames in os.walk(root):
                for name in filenames:
                    if Path(name).suffix.lower() == f".{ext}":
                        matches.append(Path(dirpath) / name)
        except Exception:
            continue
    return matches


def move_files(files: List[Path], dest: Path) -> List[Tuple[Path, Path, str]]:
    logs = []
    try:
        dest.mkdir(parents=True, exist_ok=True)
    except Exception:
        return [(src, dest / src.name, "error") for src in files]
    for src in files:
        dst = dest / src.name
        if dst.exists():
            logs.append((src, dst, "skip: exists"))
            continue
        try:
            shutil.move(str(src), str(dst))
            logs.append((src, dst, "moved"))
        except Exception:
            logs.append((src, dst, "error"))
    return logs
