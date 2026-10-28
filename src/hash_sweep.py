"""Every archived Cicada artefact against the page-73 hash (2026-10-28).

Page 73 ("An End") gives the SHA-512 of a deep-web page and tells the pilgrim to find it.  The
page was never found; the Tor v2 network that served it is gone.  What can still be checked is the
archives: wazar did whole-file SHA-512 of every blob it held (null).  This sweep does the same over the
scream314 archive (every non-image file: onion mirrors, HTML, text, binaries, decoded outputs), wazar's
primary artefacts (signed messages, payloads, mirrors) and this repository's own objects (the 75 page
images, the 256-byte payload, the signed messages, the transcription), under enumerated READINGS of
"the page": raw bytes; LF-normalised; trailing whitespace stripped; with and without a final newline;
HTML stripped to text; lower-cased; the hex and base64 of the bytes; and for the payload its raw bytes,
hex, decimal list and token list.  Any match is reported with the reading that produced it.
Usage: python -I src/hash_sweep.py
"""
import base64, hashlib, html, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lp import RESULTS, PROCESSED, RAW

TARGET = "36367763ab73783c7af284446c59466b4cd653239a311cb7116d4618dee09a8425893dc7500b464fdaf1672d7bef5e891c6e2274568926a49fb4f45132c2a8b4"
ROOT = Path(__file__).resolve().parent.parent
sources = [ROOT / "data" / "archives", ROOT / "data" / "images" / "raw", ROOT / "data" / "raw" / "pgp", ROOT / "data" / "raw"]


def readings(b):
    yield "raw", b
    yield "hex", b.hex().encode(); yield "HEX", b.hex().upper().encode(); yield "base64", base64.b64encode(b)
    try: t = b.decode("utf-8")
    except UnicodeDecodeError: return
    lf = t.replace("\r\n", "\n").replace("\r", "\n")
    yield "lf", lf.encode()
    yield "lf-no-final-newline", lf.rstrip("\n").encode(); yield "lf-final-newline", (lf.rstrip("\n") + "\n").encode()
    stripped = "\n".join(l.rstrip() for l in lf.split("\n")); yield "trailing-ws-stripped", stripped.encode()
    yield "stripped-no-final-newline", stripped.rstrip("\n").encode()
    if "<" in t and ">" in t:
        txt = html.unescape(re.sub(r"<[^>]+>", "", re.sub(r"<script.*?</script>|<style.*?</style>", "", lf, flags=re.S | re.I)))
        yield "html-text", txt.encode(); yield "html-text-collapsed", re.sub(r"\s+", " ", txt).strip().encode()
    yield "lower", lf.lower().encode()


n_files = n_read = 0; hits = []; seen = set()
for src in sources:
    for p in sorted(src.rglob("*")):
        if not p.is_file() or p.suffix == ".pyc": continue
        b = p.read_bytes(); key = hashlib.sha256(b).hexdigest()
        if key in seen: continue
        seen.add(key); n_files += 1
        for name, data in readings(b):
            n_read += 1
            if hashlib.sha512(data).hexdigest() == TARGET: hits.append((str(p.relative_to(ROOT)), name))
# this repository's own derived objects
pl = json.loads((PROCESSED / "payload.json").read_text())
B = bytes(sum((pl["pages"][k]["bytes_archive"] for k in pl["order"]), [])); Bt = bytes(sum((pl["pages"][k]["bytes_token_reading"] for k in pl["order"]), []))
toks = " ".join(sum((pl["pages"][k]["tokens"] for k in pl["order"]), []))
extra = {"payload bytes (archive reading)": B, "payload bytes (token reading)": Bt, "payload bytes reversed": B[::-1], "payload hex": B.hex().encode(), "payload decimal list": " ".join(str(x) for x in B).encode(), "payload tokens": toks.encode(), "payload tokens no spaces": toks.replace(" ", "").encode()}
for name, data in extra.items():
    n_read += 1
    if hashlib.sha512(data).hexdigest() == TARGET: hits.append(("derived", name))
out = ["# Every archived artefact against the page-73 hash", "", f"Target SHA-512 `{TARGET[:16]}…{TARGET[-8:]}`. {n_files:,} distinct files from the scream314 archive, wazar's primary artefacts, the 75 page images, the signed messages and the transcription, under {n_read:,} readings in all (raw, hex, base64, newline and whitespace normalisations, HTML stripped to text, lower-cased), plus the payload in seven forms.", "",
       ("**Matches:** " + "; ".join(f"{p} ({r})" for p, r in hits)) if hits else "**No reading of any held artefact hashes to the target.** The page, if it still exists anywhere, is not in the public archives in any form enumerated here; wazar's whole-file sweep over its own holdings reached the same result.", ""]
(RESULTS / "hash_sweep.md").write_text("\n".join(out) + "\n"); print("\n".join(out))
