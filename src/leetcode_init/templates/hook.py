#!/usr/bin/env python3
import stat
import sys
from pathlib import Path

HOOK = """#!/bin/sh
set -e
cmake --preset debug >/dev/null
cmake --build --preset debug --target format-check tidy-check
"""


def main():
    hooks = Path(__file__).resolve().parent / ".git" / "hooks"
    if not hooks.is_dir():
        sys.exit("no .git/hooks found, run 'git init' first")
    hook = hooks / "pre-push"
    hook.write_text(HOOK)
    hook.chmod(hook.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    print(f"installed {hook}")


if __name__ == "__main__":
    main()
