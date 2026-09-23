"""The skill must stay loadable by every runtime (agentskills.io spec limits)
and the prose layer must stay complete and well-formed."""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

import yaml

from pipeline import build, prose

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "model-field-guide"
ALLOWED_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}


def _frontmatter(p: Path) -> dict:
    return yaml.safe_load(p.read_text().split("---\n", 2)[1])


def test_skill_frontmatter_meets_spec():
    fm = _frontmatter(SKILL_DIR / "SKILL.md")
    assert set(fm) <= ALLOWED_FIELDS, f"non-spec fields break OpenCode/skills-ref: {set(fm) - ALLOWED_FIELDS}"
    assert fm["name"] == SKILL_DIR.name, "name must equal the folder name (OpenCode, Cursor, skills-ref enforce this)"
    assert re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", fm["name"]) and len(fm["name"]) <= 64
    assert 0 < len(fm["description"]) <= 1024, "Codex hard-limits descriptions at 1024 chars"
    assert len(fm.get("compatibility", "")) <= 500
    assert "claude" not in fm["name"] and "anthropic" not in fm["name"]


def test_skill_body_is_short():
    assert len((SKILL_DIR / "SKILL.md").read_text().splitlines()) < 200


def test_only_one_skill_md_in_the_repo():
    # Codex scans six levels deep and would load any stray SKILL.md as a skill.
    found = [p for p in ROOT.rglob("SKILL.md") if ".venv" not in p.parts and ".cache" not in p.parts]
    assert found == [SKILL_DIR / "SKILL.md"]


def test_every_allowlisted_model_has_valid_prose():
    ids = [m["id"] for m in build.load_allowlist()]
    notes, problems = prose.load_all(SKILL_DIR / "references" / "models", ids)
    assert not problems, problems
    for mid, fm in notes.items():
        assert fm["review_by"] > fm["reviewed"], mid
        if fm["status"] == "legacy":
            assert fm["superseded_by"] in ids, f"{mid}: legacy models must name an allowlisted successor"


def test_referenced_paths_exist():
    body = (SKILL_DIR / "SKILL.md").read_text()
    for rel in set(re.findall(r"`((?:tables|references)/[\w./-]+\.md)`", body)):
        assert (SKILL_DIR / rel).exists(), f"SKILL.md points at missing {rel}"


def test_prose_has_no_em_dash_numbers_without_source():
    # Cheap guard for the most damaging failure: a percentage in prose with no
    # evidence section to back it.
    for p in (SKILL_DIR / "references" / "models").glob("*.md"):
        if p.name.startswith("_"):
            continue
        text = p.read_text()
        if re.search(r"\d+(\.\d+)?%", text):
            assert "**Evidence:**" in text, f"{p.name} quotes numbers but has no Evidence section"


def test_stale_detection():
    notes = {"a": {"review_by": date(2026, 9, 1)}, "b": {"review_by": date(2026, 12, 1)}}
    assert prose.stale(notes, date(2026, 9, 22)) == ["a"]
