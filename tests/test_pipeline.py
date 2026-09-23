"""Pipeline tests over REAL recorded upstream payloads (tests/fixtures/raw).

The fixtures are the actual bytes fetched on 2026-09-22, trimmed to the rows
the allowlist uses. Each test guards a promise the repo makes publicly:
no invented numbers, no Artificial Analysis data, fail loudly on renames,
deterministic output.
"""

from __future__ import annotations

import copy
import csv
import io
import json
import shutil
import zipfile
from pathlib import Path

import pytest

from pipeline import build, diff, parse, render

FIX = Path(__file__).parent / "fixtures" / "raw"


@pytest.fixture(scope="module")
def allow():
    return build.load_allowlist()


@pytest.fixture(scope="module")
def snap(allow):
    return build.build(FIX, allow)


def test_builds_from_real_payloads(snap, allow):
    assert set(snap["models"]) == {m["id"] for m in allow}
    assert {s["source"] for s in snap["scores"]} >= {"epoch", "lmarena", "tau2", "steel"}
    # Every score belongs to an allowlisted model and carries its config label.
    assert all(s["model"] in snap["models"] and s["variant"] for s in snap["scores"])


def test_effort_variants_are_kept_separate(snap):
    astra = {s["variant"] for s in snap["scores"] if s["model"] == "gpt-6-astra" and s["board"] == "epoch.deepswe"}
    assert len(astra) > 1, "effort variants must not be collapsed into one number"


def test_lmarena_does_not_merge_neighbouring_models():
    assert parse.lmarena_match("claude-opus-5-high", ["claude-opus-5"])
    assert parse.lmarena_match("Claude Opus 5 (Max)", ["claude-opus-5"])
    assert not parse.lmarena_match("claude-opus-5-5-max", ["claude-opus-5"])
    assert not parse.lmarena_match("claude-opus-5-high", ["claude-opus-5.5", "claude-opus-5-5"])
    assert parse.lmarena_match("qwen3.8-max", ["qwen3.8-max"])  # "max" is part of the name here
    assert not parse.lmarena_match("qwen3.8-flash-next", ["qwen3.8-max"])
    assert parse.lmarena_match("DeepSeek V4 Pro (High) (0813)", ["deepseek-v4-pro-0813"])
    assert not parse.lmarena_match("DeepSeek V4 Pro", ["deepseek-v4-pro-0813"])


def test_steel_prefix_does_not_merge_point_releases():
    assert parse.steel_match("Claude Opus 5 (Snorkel run)", ["Claude Opus 5"])
    assert not parse.steel_match("Claude Opus 5.5", ["Claude Opus 5"])


def _rezip(src: Path, dst: Path, mutate) -> None:
    with zipfile.ZipFile(src) as z, zipfile.ZipFile(dst, "w") as w:
        for info in z.infolist():
            data = z.read(info)
            name = info.filename.rsplit("/", 1)[-1]
            w.writestr(info, mutate(name, data.decode()).encode() if name.endswith(".csv") else data)


def test_artificial_analysis_rows_never_render(tmp_path, allow):
    # Inject an AA-sourced row for an allowlisted model into an external file
    # we DO read. It must be dropped, and the rest must still build.
    raw = tmp_path / "raw"
    shutil.copytree(FIX, raw)
    zp = raw / "epoch" / "benchmark_data.zip"
    orig = tmp_path / "orig.zip"
    shutil.move(zp, orig)

    def mutate(name, text):
        if name != "cursorbench_external.csv":
            return text
        rows = list(csv.DictReader(io.StringIO(text)))
        bad = dict(rows[0])
        bad["Score"] = "0.99"
        bad["Source"] = "https://artificialanalysis.ai/models"
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows + [bad])
        return buf.getvalue()

    _rezip(orig, zp, mutate)
    snap = build.build(raw, allow)
    assert not any(s["value"] == 99.0 and s["board"] == "epoch.cursorbench" for s in snap["scores"])
    rendered = "\n".join(render.render_all(snap).values()) + build.dumps(snap)
    assert "artificialanalysis" not in rendered.lower()


def test_missing_expected_model_fails_loudly(tmp_path, allow):
    raw = tmp_path / "raw"
    shutil.copytree(FIX, raw)
    api = json.loads((raw / "models_dev" / "api.json").read_text())
    del api["xai"]["models"]["grok-4.7"]
    (raw / "models_dev" / "api.json").write_text(json.dumps(api))
    with pytest.raises(build.ValidationError, match="grok-4.7: expected in models_dev"):
        build.build(raw, allow)


def test_empty_upstream_fails_instead_of_publishing_empty_tables(tmp_path, allow):
    raw = tmp_path / "raw"
    shutil.copytree(FIX, raw)
    for c in ("text", "webdev", "agent"):
        (raw / "lmarena" / f"{c}.json").write_text("[]")
    with pytest.raises(build.ValidationError, match="lmarena"):
        build.build(raw, allow)


def test_failed_source_reuses_previous_rows_and_is_marked_stale(snap, allow):
    again = build.build(FIX, allow, prev=snap, failed={"lmarena"})
    assert again["sources"]["lmarena"]["stale"] is True
    assert [s for s in again["scores"] if s["source"] == "lmarena"] == [s for s in snap["scores"] if s["source"] == "lmarena"]
    assert "STALE" in render.render_meta(again)


def test_output_is_deterministic(allow):
    a = build.build(FIX, allow)
    b = build.build(FIX, allow)
    assert build.dumps(a) == build.dumps(b)
    assert render.render_all(a) == render.render_all(b)
    assert json.loads(build.dumps(a)) == a  # the one-record-per-line format is still valid JSON


def test_tables_say_not_measured_instead_of_guessing(snap):
    tables = render.render_all(snap)
    # Opus 5.5 launched on the fixture date: priced, but no scores yet.
    assert "Claude Opus 5.5" in tables["price-context.md"]
    assert "Not yet measured here:" in tables["coding.md"]
    assert "Claude Opus 5.5 | frontier | n/a | n/a" in tables["overall.md"]


def test_diff_reports_moves_and_first_scores(snap):
    prev = copy.deepcopy(snap)
    prev["scores"] = [s for s in prev["scores"] if s["model"] != "kimi-k3"]
    moved = next(s for s in prev["scores"] if s["board"] == "epoch.eci")
    moved["value"] -= 5
    lines, notices = diff.diff(prev, snap)
    assert any("Kimi K3" in n for n in notices)
    assert any("->" in l and "epoch.eci" in l for l in lines)
    assert diff.diff(snap, snap) == ([], [])


def test_changelog_keeps_one_section_per_day():
    a = diff.update_changelog("", "2026-09-22", ["- x"])
    b = diff.update_changelog(a, "2026-09-22", ["- y"])
    assert b.count("## 2026-09-22") == 1 and "- y" in b and "- x" not in b
