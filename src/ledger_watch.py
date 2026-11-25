"""The staleness guard: what has changed in other people's public work since this record last looked.

This record is frozen (release v1.0-pause-2026-11-01).  Its measurements do not age, but every statement about what another
lab has or has not run does.  results/ledger_snapshots.json pins each such statement to a date and a commit; this script
compares those pins with the live repositories and writes a report.  It reads public files as data (JSON is parsed, text is
searched), executes nothing it fetches, commits nothing, and starts no lane.

    .venv/bin/python -I src/ledger_watch.py                      report to stdout
    .venv/bin/python -I src/ledger_watch.py --out REPORT.md --state DIR
                                                                 also keep the fetched files in DIR, so the next run can
                                                                 show which lines are new since this one
    .venv/bin/python -I src/ledger_watch.py --render             rewrite results/ledger_snapshots.md from the JSON (offline)
    .venv/bin/python -I src/ledger_watch.py --accept             after a human has read the report: move every 'seen' pin
                                                                 to today (the 'compared' pins never move by script)

Network: api.github.com through `gh api` when the gh CLI is installed (so the search calls are authenticated), otherwise
anonymous HTTPS; raw.githubusercontent.com for file contents.  A fetch that fails is reported as unknown, never as unchanged.
"""
import argparse, datetime, hashlib, json, re, shutil, subprocess, sys, urllib.error, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAP = ROOT / "results" / "ledger_snapshots.json"
RENDERED = ROOT / "results" / "ledger_snapshots.md"
UA = {"User-Agent": "ledger-watch", "Accept": "application/vnd.github+json"}
SELF = "RiskAverseTech/cicada-ioc"   # the name searched for; snap["own"] lists every repository of this record
MAXLINES = 12                      # keyword lines shown per lab and category; the count is always given in full


class FetchError(Exception):
    pass


def api(path):
    """GET https://api.github.com/<path> as parsed JSON."""
    if shutil.which("gh"):
        r = subprocess.run(["gh", "api", path], capture_output=True, text=True)
        if r.returncode != 0: raise FetchError(f"gh api {path}: {r.stderr.strip()[:120]}")
        return json.loads(r.stdout)
    try:
        with urllib.request.urlopen(urllib.request.Request("https://api.github.com/" + path, headers=UA), timeout=30) as f:
            return json.loads(f.read().decode("utf-8"))
    except (urllib.error.URLError, ValueError) as e:
        raise FetchError(f"api {path}: {e}")


def raw(repo, ref, path):
    """The text of one public file."""
    url = f"https://raw.githubusercontent.com/{repo}/{ref}/{urllib.parse.quote(path)}"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "ledger-watch"}), timeout=60) as f:
            return f.read().decode("utf-8", errors="replace")
    except urllib.error.URLError as e:
        raise FetchError(f"raw {repo}/{path}: {e}")


def sha256(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def entry_ids(kind, text):
    """The row identifiers of a watched file, in file order; [] for plain text.  The file is data: parsed or matched, never run."""
    if kind == "json-entries":
        d = json.loads(text); rows = d.get("entries", []) if isinstance(d, dict) else d
        return [str(r.get("id", i)) for i, r in enumerate(rows) if isinstance(r, dict)]
    if kind == "toml-tables":       # one [[table]] per row; the id is the first id = "..." after it (no TOML parser needed, or wanted)
        out = []
        for block in re.split(r"(?m)^\[\[", text)[1:]:
            m = re.search(r'(?m)^id\s*=\s*"([^"]*)"', block); out.append(m.group(1) if m else block.split("]]")[0])
        return out
    if kind == "md-rows":           # markdown table rows whose first cell is a number
        return re.findall(r"(?m)^\|\s*#?(\d+)\s*\|", text)
    return []


def new_lines(old, new):
    """Lines of `new` that do not occur in `old` (order kept, blank lines dropped)."""
    seen = set(old.splitlines()) if old else set()
    return [l for l in new.splitlines() if l.strip() and l not in seen]


def scan(lines, keywords):
    """{category: [matching lines]} by case-insensitive substring."""
    out = {}
    for cat, words in keywords.items():
        ws = [w.lower() for w in words]; hits = [l for l in lines if any(w in l.lower() for w in ws)]
        if hits: out[cat] = hits
    return out


def check_lab(lab, keywords, state=None, api=api, raw=raw):
    """One lab against its 'seen' pin.  Returns a dict; 'error' is set when the answer is unknown."""
    r = dict(key=lab["key"], repo=lab["repo"], tier=lab["tier"], seen=lab["seen"], files=[], hits={}, error=None)
    try:
        head = api(f"repos/{lab['repo']}/commits/{lab['branch']}")
        r["head"] = head["sha"]; r["head_date"] = head["commit"]["committer"]["date"][:10]; r["moved"] = head["sha"] != lab["seen"]["commit"]
        if r["moved"]:
            try: r["ahead"] = api(f"repos/{lab['repo']}/compare/{lab['seen']['commit']}...{head['sha']}").get("ahead_by")
            except FetchError: r["ahead"] = None            # history rewritten or too long to compare
    except (FetchError, KeyError) as e:
        r["error"] = str(e); return r
    fresh = []
    for w in lab.get("watch", []):
        f = dict(path=w["path"], kind=w["kind"])
        try: text = raw(lab["repo"], r["head"], w["path"])
        except FetchError as e:
            f["error"] = str(e); r["files"].append(f); continue
        f["sha256"] = sha256(text); f["ids"] = entry_ids(w["kind"], text); f["lines"] = len(text.splitlines())
        prev = None
        if state is not None:
            p = state / lab["key"] / w["path"].replace("/", "__")
            if p.exists(): prev = p.read_text(encoding="utf-8")
            p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text, encoding="utf-8")
        f["first_read"] = prev is None
        added = new_lines(prev, text); f["added"] = len(added) if prev is not None else None
        if prev is not None and f["ids"]:
            old = set(entry_ids(w["kind"], prev)); f["new_ids"] = [i for i in f["ids"] if i not in old]
        fresh += added if prev is not None else text.splitlines()
        f["cites_us"] = any(k.lower() in text.lower() for k in keywords.get("cites this record", []))
        r["files"].append(f)
    r["hits"] = scan(fresh, keywords)
    return r


def check_source(src, raw=raw, api=api):
    r = dict(key=src["key"], repo=src["repo"], pinned=src["sha256"], error=None)
    try:
        r["head"] = api(f"repos/{src['repo']}/commits/{src['branch']}")["sha"]; r["moved"] = r["head"] != src["seen"]["commit"]
        r["now"] = sha256(raw(src["repo"], r["head"], src["path"])); r["same"] = r["now"] == src["sha256"]
    except (FetchError, KeyError) as e:
        r["error"] = str(e)
    return r


def field(since, own=(SELF,), api=api):
    """Two GitHub-wide looks: who cites this record, and which Liber Primus repositories were created since the last re-read."""
    out = dict(citing=None, created=None, errors=[])
    try:
        d = api("search/code?q=" + urllib.parse.quote(f'"{SELF}"') + "&per_page=50")
        out["citing"] = sorted({i["repository"]["full_name"] for i in d.get("items", [])} - set(own))
    except (FetchError, KeyError) as e: out["errors"].append("citation search: " + str(e))
    try:
        seen = {}
        for q in ("liber primus", "cicada 3301 runes"):
            d = api("search/repositories?q=" + urllib.parse.quote(f"{q} created:>={since}") + "&sort=updated&per_page=30")
            for i in d.get("items", []): seen[i["full_name"]] = (i["created_at"][:10], (i.get("description") or "")[:90])
        out["created"] = seen
    except (FetchError, KeyError) as e: out["errors"].append("new-repository search: " + str(e))
    return out


def report(snap, labs, sources, fld, today, ignore=()):
    known = {l["repo"] for l in snap["labs"]} | {s["repo"] for s in snap["sources"]} | set(snap.get("own", [])) | set(ignore)
    moved = [l for l in labs if not l["error"] and l["moved"]]; failed = [l for l in labs if l["error"]] + [s for s in sources if s["error"]]
    cite = [l for l in labs if any(f.get("cites_us") for f in l["files"])]; trig = [l for l in labs if l["hits"]]
    o = [f"# Ledger watch, {today}", "",
         f"Pins last moved {snap['last_reread']}. {len(labs)} repositories checked: {len(moved)} have new commits, {len(labs) - len(moved) - sum(1 for l in labs if l['error'])} unchanged, {len(failed)} could not be read (unknown, not unchanged).", "",
         "## What needs a human", ""]
    for s in sources:
        if s["error"]: o.append(f"- **Transcription source {s['repo']}: not readable** ({s['error']}).")
        elif not s["same"]: o.append(f"- **Transcription source {s['repo']} no longer matches its pin** (pinned {s['pinned'][:12]}…, now {s['now'][:12]}…). A corrected transcription is a reopen trigger (README §81): rerun the five counts of `docs/replicate.md` on it.")
        else: o.append(f"- Transcription source {s['repo']}: file matches its pin ({s['pinned'][:12]}…).")
    if fld.get("citing") is not None:
        citing = [c for c in fld["citing"] if c not in ignore]; new = [c for c in citing if c not in known]
        o.append(f"- Repositories whose code or text names this record: {', '.join(citing) or 'none found'}" + (f" (**not in the snapshot file: {', '.join(new)}**)" if new else "") + ".")
    if fld.get("created") is not None:
        new = {k: v for k, v in fld["created"].items() if k not in known}
        o.append(f"- Repositories created since {snap['last_reread']} that match the search and are not in the snapshot file: " + ("; ".join(f"{k} ({v[0]}; {v[1]})" for k, v in sorted(new.items())) if new else "none") + ".")
    for e in fld.get("errors", []): o.append(f"- Search not run: {e}.")
    for l in failed: o.append(f"- **{l['repo']}: not readable** ({l['error']}).")
    if not trig: o.append("- No keyword hit in new lines of any watched file.")
    o += ["", "## Repositories", "", "| repository | tier | pinned look | head now | commits since | watched files |", "|---|---|---|---|---|---|"]
    for l in labs:
        if l["error"]: o.append(f"| {l['repo']} | {l['tier']} | {l['seen']['date']} {l['seen']['commit'][:10]} | unknown | unknown | |"); continue
        fs = []
        for f in l["files"]:
            if "error" in f: fs.append(f"{f['path']}: not readable"); continue
            s = f"{f['path']}: " + (f"{len(f['ids'])} rows" if f["ids"] else f"{f['lines']} lines")
            if f["first_read"]: s += " (no earlier copy kept; nothing to diff)"
            else: s += f", {f['added']} new lines" + (f", {len(f['new_ids'])} new rows" if f.get("new_ids") else "")
            fs.append(s)
        since = "0" if not l["moved"] else (str(l["ahead"]) if l.get("ahead") is not None else "history not comparable")
        o.append(f"| {l['repo']} | {l['tier']} | {l['seen']['date']} {l['seen']['commit'][:10]} | {l['head_date']} {l['head'][:10]} | {since} | {'; '.join(fs) or '(commits only)'} |")
    for l in labs:
        news = [(f["path"], f["new_ids"]) for f in l["files"] if f.get("new_ids")]
        if not (l["hits"] or news): continue
        first = any(f.get("first_read") for f in l["files"])
        o += ["", f"### {l['repo']}" + (" (whole files scanned: no earlier copy to diff against)" if first else " (new lines only)"), ""]
        for path, ids in news: o.append(f"- New rows in {path} ({len(ids)}): " + ", ".join(ids[:40]) + (" …" if len(ids) > 40 else ""))
        for cat, hits in l["hits"].items():
            o.append(f"- **{cat}**: {len(hits)} lines" + (f", first {MAXLINES} shown" if len(hits) > MAXLINES else ""))
            o += [f"  - `{h.strip()[:260].replace('`', chr(39))}`" for h in hits[:MAXLINES]]
    o += ["", "## What this report is and is not", "",
          "Text matched by keyword in files fetched as data. A hit is a pointer to read, not a finding; no hit is not evidence that nothing changed. "
          "Nothing was committed. The record's comparative claims still hold only as of the 'compared' dates in `results/ledger_snapshots.md`. "
          "After reading, `--accept` moves the 'seen' pins to today; a new comparison is a separate, deliberate piece of work.", ""]
    return "\n".join(o)


def render(snap):
    """results/ledger_snapshots.md from the JSON; no network."""
    by = {l["key"]: l for l in snap["labs"]}
    def pin(p): return f"{p['date']}, `{p['commit'][:10]}`: {p['state']}" if p.get("commit") else f"{p['date']}: {p['state']}"
    o = ["# Other people's work: what this record read, and when", "",
         f"*Generated by `src/ledger_watch.py --render` from `results/ledger_snapshots.json`. Pins last moved {snap['last_reread']}.*", "",
         "**The reading rule.** This record is frozen at release `v1.0-pause-2026-11-01`. Its measurements are pinned to a transcription hash and do not age. "
         "Its statements about other labs do: every sentence in the README or in `results/` of the form \"no ledger has run this\", \"nobody had\", "
         "\"every decoder in the ledgers\" is true **as of the date in the \"claims compared against\" column below**, and says nothing about what that lab did afterwards. "
         "The last column is the most recent look, which checks only whether the repository moved; it is not a new comparison.", "",
         snap["pin_note"], "",
         "## Labs whose work this record's claims are compared against", "",
         "| repository | what it is | claims compared against | later reads | last looked |", "|---|---|---|---|---|"]
    for l in snap["labs"]:
        if l["tier"] != "compared": continue
        later = "<br>".join(f"{p['date']}, `{p['commit'][:10]}`: {p['state']} ({p['where']})" for p in l.get("later_reads", [])) or "none"
        o.append(f"| {l['repo']} (`{l['branch']}`) | {l['what']} | {pin(l['compared'])} ({l['compared']['where']}) | {later} | {pin(l['seen'])} |")
    o += ["", "## Seen, not compared", "",
          "No claim in this record rests on these, and no lane here has been checked against them. The repositories created after 2026-10-28 postdate every comparison in this record.", "",
          "| repository | what it is | last looked |", "|---|---|---|"]
    for l in snap["labs"]:
        if l["tier"] != "compared": o.append(f"| {l['repo']} (`{l['branch']}`) | {l['what']} | {pin(l['seen'])} |")
    for g in snap.get("gone", []): o.append(f"| {g['repo']} | no longer reachable | {g['note']} |")
    if snap.get("search_note"): o += ["", snap["search_note"]]
    o += ["", "## The transcription", "", "| repository | role | SHA-256 of the file | last looked |", "|---|---|---|---|"]
    for s in snap["sources"]: o.append(f"| {s['repo']} (`{s['branch']}`) | {s['role']} | `{s['sha256']}` | {s['seen']['date']}, `{s['seen']['commit'][:10]}`: {s['seen']['note']} |")
    o += ["", "## Where the comparative claims are, and what each rests on", "", "| where | as of | rests on | the claim | note |", "|---|---|---|---|---|"]
    for c in snap["claims"]: o.append(f"| {c['where']} | {c['as_of']} | {', '.join(by[k]['repo'] for k in c['rests_on'])} | {c['claim']} | {c.get('note', '')} |")
    o += ["", "## The watch", "",
          "`src/ledger_watch.py` compares the \"last looked\" pins with the live repositories: new commits, new rows in the ledgers it can parse, "
          "whether the transcription file still matches its hash, which repositories name this record, which new repositories appeared, and lines new since the previous run that match "
          "a short keyword list (" + "; ".join(snap["keywords"]) + "). It reads public files as data, executes nothing, commits nothing and starts no lane; "
          "a repository it cannot read is reported as unknown. A hit means a person should read the source. Reopening the work is decided by README §81, not by this script.", "",
          "Reproduce: `.venv/bin/python -I src/ledger_watch.py` (network), `--render` (this page, offline).", ""]
    return "\n".join(o)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out"); ap.add_argument("--state"); ap.add_argument("--render", action="store_true"); ap.add_argument("--accept", action="store_true")
    ap.add_argument("--no-search", action="store_true", help="skip the two GitHub-wide searches")
    ap.add_argument("--ignore", default="", help="comma-separated repositories to leave out of the citation line (aggregators, your own forks)")
    a = ap.parse_args(); snap = json.loads(SNAP.read_text(encoding="utf-8")); today = datetime.date.today().isoformat()
    if a.render:
        RENDERED.write_text(render(snap), encoding="utf-8"); print(f"wrote {RENDERED.relative_to(ROOT)}"); return 0
    state = Path(a.state) if a.state else None
    labs = [check_lab(l, snap["keywords"], state) for l in snap["labs"]]; sources = [check_source(s) for s in snap["sources"]]
    fld = dict(citing=None, created=None, errors=[]) if a.no_search else field(snap["last_reread"], own=snap.get("own", [SELF]))
    text = report(snap, labs, sources, fld, today, ignore=[x.strip() for x in a.ignore.split(",") if x.strip()])
    if a.out: Path(a.out).write_text(text, encoding="utf-8"); print(f"wrote {a.out}")
    else: print(text)
    if a.accept:
        if any(l["error"] for l in labs): print("not accepting: at least one repository could not be read", file=sys.stderr); return 1
        for l, r in zip(snap["labs"], labs):
            if r["moved"]: l["seen"] = dict(date=today, commit=r["head"], state=f"head dated {r['head_date']}; moved by --accept, state not described")
            else: l["seen"]["date"] = today
        for s, r in zip(snap["sources"], sources):
            if not r["error"] and r["same"] and not r["moved"]: s["seen"]["date"] = today
        snap["last_reread"] = today; SNAP.write_text(json.dumps(snap, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        RENDERED.write_text(render(snap), encoding="utf-8"); print("pins moved; review the diff before committing")
    return 0


if __name__ == "__main__":
    sys.exit(main())
