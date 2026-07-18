#!/usr/bin/env python3
"""Validate the CUC repository's formal and publication scaffolding."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

import yaml


ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def load_text(relative_path: str) -> str:
    path = ROOT / relative_path
    if not path.is_file():
        fail(f"Missing required file: {relative_path}")
        return ""
    return path.read_text(encoding="utf-8")


def load_yaml(relative_path: str):
    text = load_text(relative_path)
    if not text:
        return None
    try:
        return yaml.safe_load(text)
    except yaml.YAMLError as exc:
        fail(f"Invalid YAML in {relative_path}: {exc}")
        return None


def validate_required_files() -> None:
    required = [
        "README.md",
        "CHARTER.md",
        "CHANGELOG.md",
        "VERSION.md",
        "CITATION.cff",
        "CONTRIBUTING.md",
        "CODE_OF_CONDUCT.md",
        "LICENSE",
        "canon/README.md",
        "canon/symbols.yml",
        "canon/claims.yml",
        "experiments/README.md",
        "docs/faq.md",
        "docs/reddit-release.md",
        "requirements.txt",
        "requirements-dev.txt",
        ".github/PULL_REQUEST_TEMPLATE.md",
        ".github/ISSUE_TEMPLATE/claim.yml",
        ".github/ISSUE_TEMPLATE/experiment.yml",
        ".github/workflows/validate.yml",
    ]
    for relative_path in required:
        if not (ROOT / relative_path).is_file():
            fail(f"Missing required file: {relative_path}")


def extract_latex_blocks(text: str, source: str) -> list[str]:
    blocks: list[str] = []
    current: list[str] = []
    in_latex = False
    start_line = 0

    for line_number, line in enumerate(text.splitlines(), start=1):
        if line == "```latex":
            if in_latex:
                fail(f"Nested LaTeX fence in {source}:{line_number}")
            in_latex = True
            current = []
            start_line = line_number
            continue
        if line == "```" and in_latex:
            blocks.append("\n".join(current))
            in_latex = False
            current = []
            continue
        if in_latex:
            current.append(line)

    if in_latex:
        fail(f"Unclosed LaTeX fence in {source}:{start_line}")
    return blocks


def validate_charter_equations() -> set[str]:
    charter = load_text("CHARTER.md")
    if not charter:
        return set()

    blocks = extract_latex_blocks(charter, "CHARTER.md")
    if len(blocks) < 80:
        fail(f"Expected at least 80 copy-safe LaTeX blocks; found {len(blocks)}")

    tags: list[str] = []
    for index, block in enumerate(blocks, start=1):
        if block.count(r"\[") != block.count(r"\]"):
            fail(f"Unbalanced display delimiters in Charter LaTeX block {index}")
        tags.extend(re.findall(r"\\tag\{([^}]+)\}", block))

    duplicate_tags = sorted({tag for tag in tags if tags.count(tag) > 1})
    if duplicate_tags:
        fail(f"Duplicate equation tags: {', '.join(duplicate_tags)}")

    if len(tags) < 80:
        fail(f"Expected at least 80 tagged Charter equations; found {len(tags)}")

    if r"\left{" in charter or r"\right}" in charter:
        fail("Malformed scalable brace delimiter found in CHARTER.md")

    if "$" in charter:
        fail("Dollar-delimited math found in CHARTER.md; use fenced raw LaTeX")

    return set(tags)


def validate_symbols() -> None:
    data = load_yaml("canon/symbols.yml")
    if not isinstance(data, dict):
        return
    symbols = data.get("symbols")
    if not isinstance(symbols, list) or not symbols:
        fail("canon/symbols.yml must contain a nonempty symbols list")
        return

    ids: list[str] = []
    for index, symbol in enumerate(symbols, start=1):
        if not isinstance(symbol, dict):
            fail(f"Symbol record {index} is not a mapping")
            continue
        for field in ("id", "latex", "meaning", "type", "range"):
            if not symbol.get(field):
                fail(f"Symbol record {index} is missing {field}")
        if symbol.get("id"):
            ids.append(str(symbol["id"]))

    duplicates = sorted({symbol_id for symbol_id in ids if ids.count(symbol_id) > 1})
    if duplicates:
        fail(f"Duplicate symbol ids: {', '.join(duplicates)}")


def validate_claims(equation_tags: set[str]) -> None:
    data = load_yaml("canon/claims.yml")
    if not isinstance(data, dict):
        return
    claims = data.get("claims")
    if not isinstance(claims, list):
        fail("canon/claims.yml must contain a claims list")
        return
    if len(claims) != 10:
        fail(f"Expected 10 registered v0.2 hypotheses; found {len(claims)}")

    ids: list[str] = []
    required = {
        "claim_id",
        "title",
        "status",
        "scope",
        "claim",
        "prediction",
        "null_model",
        "falsifier",
        "equations",
        "evidence_level",
    }
    valid_evidence = set((data.get("evidence_scale") or {}).keys())

    for index, claim in enumerate(claims, start=1):
        if not isinstance(claim, dict):
            fail(f"Claim record {index} is not a mapping")
            continue
        missing = sorted(field for field in required if not claim.get(field))
        if missing:
            fail(f"Claim record {index} is missing: {', '.join(missing)}")
        claim_id = claim.get("claim_id")
        if claim_id:
            ids.append(str(claim_id))
        evidence = claim.get("evidence_level")
        if evidence not in valid_evidence:
            fail(f"Claim {claim_id or index} has invalid evidence level: {evidence}")
        for equation_id in claim.get("equations") or []:
            if equation_id not in equation_tags:
                fail(f"Claim {claim_id or index} references unknown equation: {equation_id}")

    duplicates = sorted({claim_id for claim_id in ids if ids.count(claim_id) > 1})
    if duplicates:
        fail(f"Duplicate claim ids: {', '.join(duplicates)}")


def validate_citation() -> None:
    data = load_yaml("CITATION.cff")
    if not isinstance(data, dict):
        return
    expected = {
        "cff-version": "1.2.0",
        "version": "0.2.0-draft.1",
        "license": "MIT",
    }
    for field, value in expected.items():
        if str(data.get(field)) != value:
            fail(f"CITATION.cff field {field!r} must equal {value!r}")
    if not data.get("authors"):
        fail("CITATION.cff must include at least one author")


def validate_yaml_files() -> None:
    for path in sorted(ROOT.rglob("*.yml")):
        relative = path.relative_to(ROOT).as_posix()
        load_yaml(relative)
    for path in sorted(ROOT.rglob("*.yaml")):
        relative = path.relative_to(ROOT).as_posix()
        load_yaml(relative)


def validate_relative_links() -> None:
    link_pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
    for path in sorted(ROOT.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        for raw_target in link_pattern.findall(text):
            target = raw_target.strip().split()[0].strip("<>")
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                fail(f"Link escapes repository in {path.relative_to(ROOT)}: {raw_target}")
                continue
            if not resolved.exists():
                fail(f"Broken relative link in {path.relative_to(ROOT)}: {raw_target}")


def validate_public_status() -> None:
    readme = load_text("README.md")
    required_phrases = [
        "not yet empirically validated",
        "not yet completed",
        "not offered as a universal physical law",
        "toy computational prototypes",
    ]
    lowered = readme.lower()
    for phrase in required_phrases:
        if phrase not in lowered:
            fail(f"README.md is missing public claim boundary: {phrase!r}")


def main() -> int:
    validate_required_files()
    validate_yaml_files()
    tags = validate_charter_equations()
    validate_symbols()
    validate_claims(tags)
    validate_citation()
    validate_relative_links()
    validate_public_status()

    if ERRORS:
        print("CUC repository validation failed:")
        for error in ERRORS:
            print(f"- {error}")
        return 1

    print("CUC repository validation passed.")
    print(f"- Charter equation tags: {len(tags)}")
    print("- Registered hypotheses: 10")
    print("- YAML, links, citation metadata, and public claim boundaries: valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())

