"""The staleness guard (src/ledger_watch.py).  Offline: every network call is replaced by a fake, so CI never reaches GitHub."""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import ledger_watch as W

SNAP = json.loads((ROOT / "results" / "ledger_snapshots.json").read_text(encoding="utf-8"))


def test_snapshot_file_is_complete():
    keys = [l["key"] for l in SNAP["labs"]]; assert len(keys) == len(set(keys))
    for l in SNAP["labs"]:
        assert l["tier"] in ("compared", "not-compared", "archive")
        assert len(l["seen"]["commit"]) == 40 and l["seen"]["date"] <= SNAP["last_reread"]
        if l["tier"] == "compared":                    # a lab our claims rest on must say when it was read and where the claim is
            assert len(l["compared"]["commit"]) == 40 and l["compared"]["date"] <= l["seen"]["date"] and l["compared"]["where"]
        else: assert "compared" not in l
    for c in SNAP["claims"]:                           # every indexed claim rests on labs that were actually compared
        assert c["as_of"] and all(SNAP["labs"][keys.index(k)]["tier"] == "compared" for k in c["rests_on"])
    assert SNAP["sources"][0]["sha256"] == "e21743ccd9a07f3845d52a329c61b9fa69e9ca6a44ee3ba0db8f28a0d7065004"   # docs/replicate.md


def test_the_pinned_transcription_is_the_file_in_the_repository():
    p = ROOT / "data" / "raw" / "iddqd__liber-primus__transcription--master.txt"
    assert W.sha256(p.read_text(encoding="utf-8")) == SNAP["sources"][0]["sha256"]


def test_rendered_page_is_current():
    assert (ROOT / "results" / "ledger_snapshots.md").read_text(encoding="utf-8") == W.render(SNAP)


def test_entry_ids():
    assert W.entry_ids("json-entries", json.dumps({"entries": [{"id": "R1-A"}, {"id": "R2-B"}]})) == ["R1-A", "R2-B"]
    assert W.entry_ids("toml-tables", '[[row]]\nid = "obs-lag6"\nstatus = "observed"\n\n[[row]]\nid = "p60"\n') == ["obs-lag6", "p60"]
    assert W.entry_ids("md-rows", "| # | date |\n|---|---|\n| 1 | x |\n| 22 | y |\n| note | z |\n") == ["1", "22"]
    assert W.entry_ids("text", "anything") == []


def test_new_lines_and_scan():
    old = "a\nb\n"; new = "a\nb\n\nlag-5 equality at z 4\ncites RiskAverseTech/cicada-ioc §38\n"
    added = W.new_lines(old, new); assert added == ["lag-5 equality at z 4", "cites RiskAverseTech/cicada-ioc §38"]
    hits = W.scan(added, SNAP["keywords"]); assert hits["the two laws"] == [added[0]] and hits["cites this record"] == [added[1]]
    assert W.scan(["prime_echo binary"], SNAP["keywords"]) == {}      # a bare 'echo' is not a hit


def fake(head, files):
    def api(path):
        if "/commits/" in path: return {"sha": head, "commit": {"committer": {"date": "2026-12-01T00:00:00Z"}}}
        if "/compare/" in path: return {"ahead_by": 3}
        raise W.FetchError("unexpected " + path)
    def raw(repo, ref, path):
        if path not in files: raise W.FetchError("404 " + path)
        return files[path]
    return api, raw


def test_unchanged_changed_and_unreadable(tmp_path):
    lab = dict(key="x", repo="o/r", branch="main", tier="compared", seen=dict(date="2026-11-25", commit="a" * 40, state="s"), watch=[dict(path="L.json", kind="json-entries")])
    v1 = json.dumps({"entries": [{"id": "A"}]}); v2 = json.dumps({"entries": [{"id": "A"}, {"id": "B", "note": "within-word lag-6"}]}, indent=1)
    api, raw = fake("a" * 40, {"L.json": v1}); r = W.check_lab(lab, SNAP["keywords"], tmp_path, api, raw)
    assert not r["moved"] and r["files"][0]["first_read"] and r["files"][0]["ids"] == ["A"]
    api, raw = fake("b" * 40, {"L.json": v2}); r = W.check_lab(lab, SNAP["keywords"], tmp_path, api, raw)
    assert r["moved"] and r["ahead"] == 3 and r["files"][0]["new_ids"] == ["B"] and "the two laws" in r["hits"]
    def dead(path): raise W.FetchError("offline")
    r = W.check_lab(lab, SNAP["keywords"], tmp_path, dead, raw); assert r["error"]          # unknown, and the report must say so
    text = W.report(dict(SNAP, labs=[lab], sources=[]), [r], [], dict(citing=None, created=None, errors=[]), "2026-12-01")
    assert "1 could not be read" in text and "not readable" in text and "0 unchanged" in text


def test_a_changed_transcription_is_flagged():
    src = SNAP["sources"][0]; api, raw = fake(src["seen"]["commit"], {src["path"]: "different"})
    r = W.check_source(src, raw, api); assert not r["same"]
    text = W.report(SNAP, [], [r], dict(citing=["Dukotah/cicada3301", "new/lab"], created={}, errors=[]), "2026-12-01")   # Dukotah is in the snapshot file, new/lab is not
    assert "no longer matches its pin" in text and "not in the snapshot file: new/lab" in text
