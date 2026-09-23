"""Pipeline tests over the REAL coding-agents page recorded on 2026-09-22.

Each test guards a promise: never publish a broken or empty table, keep
effort levels in labels, byte-deterministic output, and a changelog that
says what moved.
"""

from __future__ import annotations

import copy
import gzip
from pathlib import Path

import pytest

from pipeline import aa, diff, nightly, render

FIXTURE = Path(__file__).parent / "fixtures" / "coding-agents-2026-09-22.html.gz"


@pytest.fixture(scope="module")
def html() -> str:
    return gzip.decompress(FIXTURE.read_bytes()).decode("utf-8")


@pytest.fixture(scope="module")
def data(html):
    return aa.parse(html)


def test_parses_every_row_from_the_real_page(data):
    assert len(data["rows"]) == 19
    assert data["index_version"] == "v1.5"
    assert data["as_of"] == "2026-09-23"
    top = data["rows"][0]
    assert (top["agent"], top["index"]) == ("Claude Code", 62.2)
    assert set(top["evals"]) == set(aa.EVALS)


def test_labels_keep_effort_and_drop_raw_config_dicts(data):
    labels = {r["label"] for r in data["rows"]}
    assert "Opencode - GLM-5.3 (max)" in labels
    assert "Codex - GPT-6 Sol (max)" in labels
    assert not any("reasoning_effort" in label for label in labels)
    glm = next(r for r in data["rows"] if r["agent"] == "Opencode")
    assert glm["model"] == "GLM-5.3 (max)", "effort must survive even when display.model drops it"


def test_rows_sorted_by_index(data):
    idx = [r["index"] for r in data["rows"]]
    assert idx == sorted(idx, reverse=True)


def test_changed_page_format_fails_instead_of_publishing_empty_table():
    with pytest.raises(aa.ParseError, match="flight payload"):
        aa.parse("<html><body>redesigned page</body></html>")


def test_too_few_rows_fails(html):
    # Keep the payload but break all but a few row objects.
    broken = html.replace('\\"isDefault\\"', '\\"isDefaultX\\"', 15)
    with pytest.raises(aa.ParseError, match="rows parsed"):
        aa.parse(broken)


def test_output_is_deterministic(html):
    a, b = aa.parse(html), aa.parse(html)
    assert nightly.dumps(a) == nightly.dumps(b)
    assert render.render_table(a) == render.render_table(b)


def test_snapshot_format_is_valid_json(data):
    import json
    assert json.loads(nightly.dumps(data)) == data


def test_table_credits_the_source_and_shows_the_date(data):
    t = render.render_table(data)
    assert "Artificial Analysis" in t and "Data as of:** 2026-09-23" in t
    assert "| 1 | Claude Code |" in t
    assert "## Best score for the money" in t and "## Fastest" in t


def test_diff_reports_new_rows_and_moves(data):
    prev = copy.deepcopy(data)
    prev["rows"] = [r for r in prev["rows"] if r["agent"] != "Grok Build"]
    prev["rows"][0]["index"] -= 3
    lines, notices = diff.diff(prev, data)
    assert any("New: **Grok Build" in line for line in lines)
    assert any("->" in line for line in lines)
    assert notices
    assert diff.diff(data, data) == ([], [])


def test_index_version_change_is_flagged(data):
    prev = copy.deepcopy(data)
    prev["index_version"] = "v1.4"
    lines, _ = diff.diff(prev, data)
    assert "methodology changed" in lines[0]


def test_changelog_keeps_one_section_per_day():
    a = diff.update_changelog("", "2026-09-22", ["- x"])
    b = diff.update_changelog(a, "2026-09-22", ["- y"])
    assert b.count("## 2026-09-22") == 1 and "- y" in b and "- x" not in b


def test_live_page_with_undefined_sentinels_parses():
    # Recorded 2026-09-23: Next.js wrote "$undefined" for display.creator on
    # the Devin Fusion rows, which crashed the first live run.
    html = gzip.decompress((FIXTURE.parent / "coding-agents-2026-09-23.html.gz").read_bytes()).decode("utf-8")
    data = aa.parse(html)
    devin = [r for r in data["rows"] if r["agent"] == "Devin Fusion CLI"]
    assert devin and all(r["agent_maker"] == "" for r in devin)
