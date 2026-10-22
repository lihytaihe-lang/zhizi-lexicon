"""AI-era product / company / model / tool names (VOCAB-COVERAGE-PLAN, family B) into two layers.

  python export_ai_terms.py <names dir with ai-names-*.tsv> <out dir> [--date YYYY-MM-DD]

Input TSVs (columns spelling, zh_name, vendor, category, source_url) come from web research where every entry was seen on
an official or authoritative page. Output:
  agent_ai_terms.dict.yaml  ASCII spellings with a lowercase letters-only reading, loaded by the core like agent_tech_terms
                            (exact spelling and capitalisation: WorkBuddy, DeepSeek, Claude Code); not imported into Rime.
  agent_ai_names.dict.yaml  Chinese product / company names with a pinyin reading, imported by agent_pinyin.
  *.provenance.tsv          one row per entry with the source page and the date it was checked.
Left out: entries already shipped, readings that are whole pinyin (the Chinese reading owns them), spellings with digits (version names), spellings that are ordinary English words
(Make, Comet, Fathom: typing the word must keep giving the word; a short explicit stoplist), and anything not letters / spaces / dots / hyphens.
"""
import argparse
import csv
import glob
import os
import re
import sys

from pypinyin import lazy_pinyin

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_general_lexicon import existing_entries  # noqa: E402

ASCII_NAME = re.compile(r"^[A-Za-z][A-Za-z .\-]*[A-Za-z]$")
HAN_NAME = re.compile(r"^[一-鿿]{2,12}$")


# Ordinary English words that happen to be product names. Typing the word must keep giving the word, so these are not
# registered (a dictionary-word test is too blunt: Claude, Codex, Perplexity, Obsidian are brands and are wanted).
GENERIC_WORDS = {w.lower() for w in (
    "Make Continue Anything Comet Cosmos Crush Composer Factory Fable Genie Granite Haystack Modal Monica Nova Pi Poe Ray "
    "Replicate Rerank Seed Void Warp Wan goose ima quantization Gamma Runway Amp Bolt Jules Janus Talkie Tana Lark Emergent "
    "Cognition Phi Mythos Zed Pika Descript Fathom Fireworks Together Groq Cloud Studio Platform Agent Skills Assistant").split()}


def pinyin_syllables():
    """The core's own pinyin syllable inventory (mixer.rs PINYIN_SYLLABLES), so the two never disagree."""
    source = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../native/core/agent-ime-core/src/mixer.rs"),
                  encoding="utf-8").read()
    return set(re.search(r'const PINYIN_SYLLABLES: &str = "([^"]*)"', source).group(1).split())


def pinyin_segmentable(reading, syllables):
    """True when the letters can be read as a chain of pinyin syllables (doubao = dou bao): those belong to Chinese typing."""
    ok = [False] * (len(reading) + 1)
    ok[0] = True
    for end in range(1, len(reading) + 1):
        ok[end] = any(ok[start] and reading[start:end] in syllables for start in range(max(0, end - 6), end))
    return ok[-1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("names_dir")
    ap.add_argument("out")
    ap.add_argument("--date", default="2026-10-13")
    args = ap.parse_args()
    existing = existing_entries(exclude_dictionaries=("agent_ai_names", "agent_ai_terms"))
    shipped_text = set(existing)
    syllables = pinyin_syllables()
    shipped_ascii_readings = {}
    for text, readings in existing.items():
        if text.isascii():
            for reading, _ in readings:
                shipped_ascii_readings.setdefault(reading.replace(" ", "").lower(), set()).add(text)
    ascii_rows, zh_rows, stats = {}, {}, {"digits": 0, "english_word": 0, "shipped": 0, "short": 0, "bad_shape": 0}
    for path in sorted(glob.glob(os.path.join(args.names_dir, "ai-names-*.tsv"))):
        for row in csv.DictReader(open(path, encoding="utf-8"), delimiter="\t"):
            spelling, zh, url = row["spelling"].strip(), (row.get("zh_name") or "").strip(), row["source_url"].strip()
            if spelling and ASCII_NAME.match(spelling):
                reading = re.sub(r"[^a-z]", "", spelling.lower())
                if len(reading) < 3:
                    stats["short"] += 1
                elif pinyin_segmentable(reading, syllables):
                    stats["pinyin_valid"] = stats.get("pinyin_valid", 0) + 1  # the Chinese reading owns these (Doubao, Pangu)
                elif spelling.lower() in GENERIC_WORDS:
                    stats["english_word"] += 1
                elif spelling in shipped_ascii_readings.get(reading, set()):
                    stats["shipped"] += 1
                else:
                    ascii_rows.setdefault((reading, spelling), (url, row["category"]))
            elif spelling and re.search(r"\d", spelling):
                stats["digits"] += 1
            elif spelling and HAN_NAME.match(spelling):
                zh = zh or spelling
            elif spelling:
                stats["bad_shape"] += 1
            if zh and HAN_NAME.match(zh):
                if zh in shipped_text:
                    stats["shipped"] += 1
                else:
                    zh_rows.setdefault(zh, (" ".join(lazy_pinyin(zh)), url, row["category"]))
    os.makedirs(args.out, exist_ok=True)
    header = lambda name, note: (f"# {note}\n# Built by scripts/lexicon/export_ai_terms.py from web-checked name lists; do not edit by hand.\n"
                                 f"---\nname: {name}\nversion: \"0.1.0\"\nsort: by_weight\n...\n\n")
    ordered = sorted(ascii_rows.items(), key=lambda kv: (kv[0][0], kv[0][1]))
    with open(os.path.join(args.out, "agent_ai_terms.dict.yaml"), "w", encoding="utf-8") as fh:
        fh.write(header("agent_ai_terms", "AI-era product, company, model and tool names: canonical spelling, lowercase letters-only reading."))
        fh.write("".join(f"{spelling}\t{reading}\t500\n" for (reading, spelling), _ in ordered))
    with open(os.path.join(args.out, "agent_ai_terms.provenance.tsv"), "w", encoding="utf-8") as fh:
        fh.write("text\treading\tweight\tcategory\tsource_url\tchecked\tlicense\n")
        for (reading, spelling), (url, category) in ordered:
            fh.write(f"{spelling}\t{reading}\t500\t{category}\t{url}\t{args.date}\tfacts-only (names)\n")
    zh_ordered = sorted(zh_rows.items(), key=lambda kv: (kv[1][0], kv[0]))
    with open(os.path.join(args.out, "agent_ai_names.dict.yaml"), "w", encoding="utf-8") as fh:
        fh.write(header("agent_ai_names", "AI-era Chinese product and company names with pinyin readings."))
        fh.write("".join(f"{zh}\t{reading}\t300\n" for zh, (reading, _, _) in zh_ordered))
    with open(os.path.join(args.out, "agent_ai_names.provenance.tsv"), "w", encoding="utf-8") as fh:
        fh.write("text\treading\tweight\tcategory\tsource_url\tchecked\tlicense\n")
        for zh, (reading, url, category) in zh_ordered:
            fh.write(f"{zh}\t{reading}\t300\t{category}\t{url}\t{args.date}\tfacts-only (names)\n")
    print({"ascii_terms": len(ordered), "chinese_names": len(zh_ordered), **stats})


if __name__ == "__main__":
    main()
