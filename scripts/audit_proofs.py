"""Reject Lean placeholders and unexpected theorem axioms after a Lake build."""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLACEHOLDER = re.compile(r"\b(?:sorry|admit|axiom|opaque)\b")
AXIOM_LINE = re.compile(r"depends on axioms:\s*\[(?P<axioms>[^]]*)\]")
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_AUDITS = 6


def code_only(source: str) -> str:
    """Replace comments and strings with spaces while preserving line positions."""
    result: list[str] = []
    index = 0
    comment_depth = 0
    in_string = False
    while index < len(source):
        pair = source[index : index + 2]
        char = source[index]
        if comment_depth:
            if pair == "/-":
                comment_depth += 1
                result.extend("  ")
                index += 2
            elif pair == "-/":
                comment_depth -= 1
                result.extend("  ")
                index += 2
            else:
                result.append("\n" if char == "\n" else " ")
                index += 1
        elif in_string:
            if char == "\\" and index + 1 < len(source):
                result.extend("  ")
                index += 2
            elif char == '"':
                in_string = False
                result.append(" ")
                index += 1
            else:
                result.append("\n" if char == "\n" else " ")
                index += 1
        elif pair == "/-":
            comment_depth = 1
            result.extend("  ")
            index += 2
        elif pair == "--":
            end = source.find("\n", index)
            if end == -1:
                result.extend(" " * (len(source) - index))
                break
            result.extend(" " * (end - index))
            result.append("\n")
            index = end + 1
        elif char == '"':
            in_string = True
            result.append(" ")
            index += 1
        else:
            result.append(char)
            index += 1
    return "".join(result)


def find_placeholders() -> list[str]:
    problems: list[str] = []
    for path in sorted(ROOT.rglob("*.lean")):
        if ".lake" in path.parts:
            continue
        code = code_only(path.read_text(encoding="utf-8"))
        relative = path.relative_to(ROOT)
        for match in PLACEHOLDER.finditer(code):
            line = code.count("\n", 0, match.start()) + 1
            problems.append(f"placeholder declaration: {relative}:{line}: {match.group(0)}")
    return problems


def theorem_axioms() -> tuple[list[str], str]:
    result = subprocess.run(
        ["lake", "env", "lean", "ESeries/CheckAxioms.lean"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    transcript = result.stdout + result.stderr
    if result.returncode:
        return ["axiom audit command failed", transcript], transcript
    rows = AXIOM_LINE.findall(transcript)
    problems: list[str] = []
    if len(rows) != EXPECTED_AUDITS:
        problems.append(f"expected {EXPECTED_AUDITS} theorem audit rows, found {len(rows)}")
    for axioms in rows:
        found = {item.strip() for item in axioms.split(",") if item.strip()}
        unexpected = sorted(found - ALLOWED_AXIOMS)
        if unexpected:
            problems.append(f"unexpected axioms: {', '.join(unexpected)}")
        if "sorryAx" in found:
            problems.append("sorryAx found in theorem audit")
    return problems, transcript


def write_report(path: Path, transcript: str, problems: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    manifest = ROOT / "lake-manifest.json"
    manifest_hash = hashlib.sha256(manifest.read_bytes()).hexdigest()
    lines = [
        "Lean proof audit",
        f"toolchain: {(ROOT / 'lean-toolchain').read_text(encoding='utf-8').strip()}",
        f"lake-manifest-sha256: {manifest_hash}",
        "status: " + ("failed" if problems else "passed"),
        "",
        transcript.strip(),
    ]
    if problems:
        lines.extend(["", "problems:", *problems])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    problems = find_placeholders()
    axiom_problems, transcript = theorem_axioms()
    problems.extend(axiom_problems)
    if args.report:
        write_report(args.report, transcript, problems)
    if problems:
        print("Lean proof audit failed:", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1
    print("Lean proof audit passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
