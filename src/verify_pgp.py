"""Verify Cicada 3301's signed messages against the group's public key by FULL fingerprint (2026-10-27).

A Discord post of 2026-10-27 claimed the April 2017 "Beware false paths" message was a hoax that
"exploited weaknesses in PGP".  The signature is RSA-4096 over SHA-512 with the key created on
2012-01-05 whose fingerprint is 6D85 4CD7 9333 22A6 01C3 286D 181F 01E5 7A35 090F; it verifies,
as do the 2012 denial about "Necrome" and the 2016 message pointing at Liber Primus.  Note on
transcriptions: RFC 4880 §7.1 strips trailing whitespace from cleartext lines before hashing, and
some archived copies carry trailing spaces, so a verifier that does not canonicalise reports those
copies as bad; this script canonicalises and reports both results.
Needs the pure-Python OpenPGP implementation pgpy (pip install pgpy); GnuPG gives the same answer:
  gpg --import data/raw/pgp/cicada_7A35090F_pubkey.asc && gpg --verify data/raw/pgp/2017-04-04_beware-false-paths.asc
Usage: python -I src/verify_pgp.py
"""
import glob, hashlib, sys, warnings
from pathlib import Path
warnings.filterwarnings("ignore")
import pgpy

HERE = Path(__file__).resolve().parent.parent / "data" / "raw" / "pgp"
EXPECTED = "6D854CD7933322A601C3286D181F01E57A35090F"
key, _ = pgpy.PGPKey.from_file(str(HERE / "cicada_7A35090F_pubkey.asc"))
fp = key.fingerprint.replace(" ", "")
print(f"key {fp} created {key.created:%Y-%m-%d} {key.key_algorithm.name} {key.key_size}; matches expected fingerprint: {fp == EXPECTED}")
assert fp == EXPECTED
for f in sorted(HERE.glob("*.asc")):
    if "pubkey" in f.name: continue
    raw = f.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
    head, sep, tail = raw.partition("-----BEGIN PGP SIGNATURE-----")
    canon = "\n".join(l.rstrip(" \t") for l in head.split("\n")) + sep + tail
    msg = pgpy.PGPMessage.from_blob(raw); sig = list(msg.signatures)[0]
    as_is = bool(key.verify(msg)); canonical = bool(key.verify(pgpy.PGPMessage.from_blob(canon)))
    print(f"{f.name:45s} signer {sig.signer}  signed {sig.created:%Y-%m-%d %H:%M}Z  {sig.hash_algorithm.name:6s} verified: as stored {as_is}, canonicalised {canonical}  sha256 {hashlib.sha256(f.read_bytes()).hexdigest()[:16]}")
