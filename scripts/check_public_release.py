"""Check the candidate Lean repository for private release artifacts."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_SUFFIXES = {".log", ".zip", ".bak", ".tmp"}
PATTERNS = {
    "workstation path": re.compile(r"(?i)(?:E:[\\/]|[\\/]Users[\\/][^\\/]+|[\\/]home[\\/][^\\/]+)"),
    "internal work item": re.compile(r"\b" + "NEX" + r"[-_]?\d+\b", re.IGNORECASE),
    "internal role": re.compile(r"\b(?:" + "CEO" + "|" + "CRO" + r")\b|算法" + "研究员|审核专员|研究助理"),
    "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
}


def main() -> int:
    problems: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in {".git", ".lake"} for part in path.parts):
            continue
        relative = path.relative_to(ROOT)
        if relative == Path("scripts/check_public_release.py"):
            continue
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            problems.append(f"forbidden artifact: {relative}")
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for label, pattern in PATTERNS.items():
            for match in pattern.finditer(content):
                line = content.count("\n", 0, match.start()) + 1
                problems.append(f"{label}: {relative}:{line}")

    if problems:
        print("Public release scan failed:")
        for problem in sorted(set(problems)):
            print(f"  - {problem}")
        return 1
    print("Public release scan passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
