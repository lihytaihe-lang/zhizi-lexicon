"""Vocabulary pack layers (poetry, CAD, industry) from the curated lists of curate_packs.py.

  python export_packs.py <curated dir> <out dir> [--extra-readings reading-disagreements.tsv] [--date YYYY-MM-DD]

Chinese entries become agent_pack_<name>.dict.yaml (imported by agent_pinyin, weight 200, never above the existing first choice for
the same reading, nothing already shipped). ASCII names of all packs become one agent_pack_terms.dict.yaml (spelling, lowercase letters-only
reading, weight 400; loaded by the core like agent_ai_terms, not imported into Rime). Each layer has a provenance TSV with the source
page and the licence note of every row. Packs are separate files so that a pack can be switched off or shipped on its own.
"""
import argparse
import csv
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_general_lexicon import existing_entries  # noqa: E402

PACKS = ("poetry", "cad", "industry")
OWN = tuple(f"agent_pack_{p}" for p in PACKS) + ("agent_pack_terms",)


def read(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def header(name, note):
    return (f"# {note}\n# Built by scripts/lexicon/curate_packs.py + export_packs.py from researched, source-checked lists; do not edit by hand.\n"
            f"---\nname: {name}\nversion: \"0.1.0\"\nsort: by_weight\n...\n\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("curated")
    ap.add_argument("out")
    ap.add_argument("--extra-readings", help="TSV text / ours / second opinion; a differing second reading of the same length is added as another entry")
    ap.add_argument("--date", default="2026-10-13")
    args = ap.parse_args()
    existing = existing_entries(exclude_dictionaries=OWN)
    if not existing:
        raise RuntimeError("no shipped dictionaries found; run from the repository")
    top, shipped_ascii = {}, set()
    for text, rows in existing.items():
        for reading, weight in rows:
            top[reading] = max(top.get(reading, 0), weight)
            if text.isascii():
                shipped_ascii.add((text, reading.replace(" ", "").lower()))
    syllables = {s for rows in existing.values() for reading, _ in rows for s in reading.split()}
    extra = {}
    if args.extra_readings:
        for line in open(args.extra_readings, encoding="utf-8"):
            text, ours, theirs = line.rstrip("\n").split("\t")
            if len(theirs.split()) == len(text) and all(s in syllables for s in theirs.split()):
                extra.setdefault(text, []).append(theirs)
    os.makedirs(args.out, exist_ok=True)
    stats = Counter()
    claimed = set(existing)
    ascii_rows = []
    for pack in PACKS:
        rows, seen = [], set()
        for r in read(os.path.join(args.curated, f"{pack}.zh.tsv")):
            text = r["text"]
            if text in claimed:
                stats[f"{pack}.already_shipped"] += 1
                continue
            for reading in [r["reading"]] + extra.get(text, []):
                if (text, reading) in seen:
                    continue
                seen.add((text, reading))
                weight = 200
                if reading in top and weight >= top[reading]:
                    weight = max(1, top[reading] - 1)
                    stats[f"{pack}.capped"] += 1
                rows.append((text, reading, weight, r["category"], r["source_url"], r["license_note"]))
        for text in {row[0] for row in rows}:
            claimed.add(text)
        rows.sort(key=lambda x: (x[1], -x[2], x[0]))
        name = f"agent_pack_{pack}"
        with open(os.path.join(args.out, f"{name}.dict.yaml"), "w", encoding="utf-8") as fh:
            fh.write(header(name, f"Optional vocabulary pack: {pack}.") + "".join(f"{t}\t{rd}\t{w}\n" for t, rd, w, *_ in rows))
        with open(os.path.join(args.out, f"{name}.provenance.tsv"), "w", encoding="utf-8") as fh:
            fh.write("text\treading\tweight\tcategory\tsource_url\tchecked\tlicense\n")
            for t, rd, w, cat, url, lic in rows:
                fh.write(f"{t}\t{rd}\t{w}\t{cat}\t{url}\t{args.date}\t{lic}\n")
        stats[f"{pack}.rows"] = len(rows)
        for r in read(os.path.join(args.curated, f"{pack}.ascii.tsv")):
            if (r["text"], r["reading"]) in shipped_ascii or r["text"] in claimed:
                stats[f"{pack}.ascii_shipped"] += 1
                continue
            claimed.add(r["text"])
            ascii_rows.append({**r, "pack": pack})
    ascii_rows.sort(key=lambda r: (r["reading"], r["text"]))
    name = "agent_pack_terms"
    with open(os.path.join(args.out, f"{name}.dict.yaml"), "w", encoding="utf-8") as fh:
        fh.write(header(name, "Optional vocabulary packs (CAD, industry): names, formats and acronyms (exact spelling, lowercase letters-only reading).")
                 + "".join(f"{r['text']}\t{r['reading']}\t400\n" for r in ascii_rows))
    with open(os.path.join(args.out, f"{name}.provenance.tsv"), "w", encoding="utf-8") as fh:
        fh.write("text\treading\tweight\tcategory\tsource_url\tchecked\tlicense\n")
        for r in ascii_rows:
            fh.write(f"{r['text']}\t{r['reading']}\t400\t{r['pack']}\t{r['source_url']}\t{args.date}\t{r['license_note']}\n")
    stats["ascii_rows"] = len(ascii_rows)
    print(dict(stats))


if __name__ == "__main__":
    main()
