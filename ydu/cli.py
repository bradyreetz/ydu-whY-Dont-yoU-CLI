import sys
from pathlib import Path

from .executors import find_files_by_extension, move_files
from .intents import parse_intent
from .planner import build_plan
from .utils import confirm, discover_roots, print_plan


def main():
    if len(sys.argv) < 2:
        print('Usage: ydu "<free text>"')
        sys.exit(1)
    text = sys.argv[1]
    intent = parse_intent(text)
    if not intent:
        print("Could not understand request.")
        sys.exit(1)
    roots = discover_roots()
    plan = build_plan(intent, roots)
    print_plan(plan)
    if not confirm():
        print("Aborted.")
        return
    ext = intent["extension"]
    files = find_files_by_extension(ext, roots)
    if intent["type"] == "find_by_extension":
        for f in files:
            print(f)
        print(f"summary: {len(files)} found")
    else:
        dest = Path(intent["destination"]).expanduser()
        logs = move_files(files, dest)
        for src, dst, status in logs:
            print(f"{src} -> {dst} : {status}")
        moved = sum(1 for _, _, s in logs if s == "moved")
        skipped = sum(1 for _, _, s in logs if s.startswith("skip"))
        errors = sum(1 for _, _, s in logs if s == "error")
        print(f"summary: moved={moved} skipped={skipped} errors={errors}")
