"""Curate the three researched vocabulary packs (poetry, CAD, industry) into what is worth shipping as optional layers.

  python curate_packs.py <vocab-packs dir> <out dir> [--jiyili <jiyili/data/content>]

Input: <packs>/poetry/{idioms,poets,poem_titles,poem_lines}.tsv, <packs>/cad/{cad_zh,cad_ascii}.tsv,
       <packs>/industry/{industry_zh,industry_ascii}.tsv (columns text, reading, category, source_url, license_note).
Output (<out dir>/<pack>.zh.tsv and <pack>.ascii.tsv, columns text, reading, category, source_url, license_note):
  poetry    idioms, poets and titles kept (titles up to 8 characters); poem lines only from the three familiar anthologies
            (Tang 300, Qianjia, Shuimo Tang poems, Song ci 300), 5 or 7 characters or ci lines of 4-9 characters.
  cad       nouns and terms only: GUI command phrases (添加/创建/修改/切换... + object) are what a menu says, not what people type.
  industry  as researched, minus very long phrases.
  ASCII     brand / format / standard / protocol names on an allowlist or at least 4 letters with no ordinary-English clash;
            two-letter and most three-letter acronyms are left out (they collide with abbreviations people type).
"""
import argparse
import csv
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from export_ai_terms import GENERIC_WORDS, pinyin_segmentable, pinyin_syllables  # noqa: E402

GUI_VERB = re.compile(r"^(添加|创建|修改|切换|设置|重命名|删除|用|从|将|按|显示|隐藏|导入|导出|选择|新建|编辑|移动|复制|粘贴|启用|禁用|打开|关闭|更改|转换|生成|合并|拆分|插入|应用|重置|取消|反转|对齐|自动|使用|沿|在|到|与|为|把)")
# pinyin readings in the researched sets were produced by pypinyin; the CAD and poetry sets reviewed heteronyms by hand.

ASCII_KEEP_SHORT = {  # three letters / formats and acronyms people really type; everything else under four letters is dropped
    "CAD", "CAM", "CAE", "BIM", "CNC", "PLC", "PCB", "BOM", "MES", "ERP", "PID", "HMI", "DWG", "DXF", "STL", "SVG", "PNG", "PDF", "OBJ",
    "FBX", "GLB", "IFC", "DGN", "SKP", "RVT", "RFA", "PLM", "PDM", "FEA", "CFD", "OEE", "SPC", "FMEA", "APQP", "PPAP", "ISO", "ANSI",
    "ASME", "ASTM", "DIN", "JIS", "AWG", "RFID", "PWM", "FPGA", "CPU", "GPU", "SCADA", "OPC UA", "Modbus", "PROFIBUS", "PROFINET",
    "EtherCAT", "CANopen", "DeviceNet", "IO-Link", "MQTT", "MOSFET", "IGBT", "SMT", "ESD", "EMI", "PTFE", "PVC", "HDPE", "G-code",
    "GD&T", "IGES", "STEP", "JPEG", "TIFF", "NURBS", "B-Rep", "BREP", "GCODE", "VRML", "COLLADA", "glTF", "USD", "USDZ", "FCStd",
    "SLDPRT", "SLDASM", "SLDDRW", "CATPart", "CATProduct", "CATDrawing", "HPGL", "Poka-yoke", "Six Sigma",
}
ASCII_DROP = {  # short or ordinary words and fragments that came out of Wikipedia lists
    "Cobalt", "Fusion", "Cycles", "Modo", "Arnold", "Basic", "Norm", "Spec", "Mach", "Panel", "Siemens", "Mitsubishi", "Inventor", "Rhino",
    "Revit", "Creo", "Shape", "Tekla", "Eagle", "Autodesk", "Rhinoceros", "Marmoset", "Mastercam",
    "ASSY", "BHCS", "CERT", "CRES", "COTS", "HHCS", "MACH", "NORM", "REQD", "SHCS", "SHSS", "SPEC", "SPOTFACE", "THRD", "THRU", "BLEND",
    "EASM", "EDRW", "ENCY", "EPRT", "SCAD", "SCDOC", "PSMODEL", "CADD", "Uniclass", "Gaffer", "CHAM", "AIAG", "ACPI", "AMQP", "CISC",
    "SIMM", "DIMM", "EPROM", "CONWIP", "AutoCAST", "PADS", "SHAPR", "Actran", "Clara.io", "Modelur", "Kubotek", "AxSTREAM", "OptiY",
}
RISKY = set("长弹行重朝还乐数传处调空难藏宿觉差着载曾好相少将间为薄降省盛得度率会都参恶夫假解卷累令蒙模切散提系兴血咽应钻没")
LINE_SOURCES = ("唐诗三百首", "tangshisanbaishou", "qianjiashi", "宋词三百首", "shuimotangshi")


def read(path):
    with open(path, encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def write(path, rows):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("text\treading\tcategory\tsource_url\tlicense_note\n")
        for r in rows:
            fh.write("\t".join(r[k] for k in ("text", "reading", "category", "source_url", "license_note")) + "\n")


def ascii_rows(rows, syllables):
    out, seen = [], set()
    for r in rows:
        text = r["text"].strip()
        letters = re.sub(r"[^a-z]", "", text.lower())
        if text in seen or text in ASCII_DROP:
            continue
        if not re.match(r"^[A-Za-z][A-Za-z0-9 .&/\-]*$", text) or re.search(r"\d", text):
            continue
        if len(text.split()) > 2 or len(text) > 22:
            continue
        if text.lower() in GENERIC_WORDS or pinyin_segmentable(letters, syllables):
            continue
        if len(letters) < 4 and text not in ASCII_KEEP_SHORT:
            continue
        seen.add(text)
        out.append({**r, "reading": letters})
    return out


def jiyili_rows(content_dir):
    """Poets, poem titles, familiar line clauses and idioms from the owner's own memory-training project (jiyili): a hand-reviewed
    list of 1500 classical poems and 300 idioms. Texts are public-domain classical works taken from chinese-poetry; the selection is
    the project's. Names are converted to simplified characters; readings come from pypinyin (checked against the project's idiom pinyin)."""
    import glob
    import re
    from opencc import OpenCC
    from itertools import product
    from pypinyin import Style, lazy_pinyin, pinyin
    t2s = OpenCC("t2s")
    base = "https://github.com/chinese-poetry/chinese-poetry"
    lic = "MIT; classical originals public domain; selected from the owner's jiyili project"
    han = re.compile(r"^[一-鿿]+$")
    rows = {}

    def readings(text):
        """pypinyin's phrase reading first; where a character from the risky heteronym set is present the other readings of those
        characters are added as further readings (long: chang/zhang), at most four, otherwise the row is left out."""
        first = [r[0] for r in pinyin(text, style=Style.NORMAL, v_to_u=False)]
        options = [[syl] if ch not in RISKY else list(dict.fromkeys([syl] + pinyin(ch, style=Style.NORMAL, heteronym=True, v_to_u=False)[0]))
                   for ch, syl in zip(text, first)]
        combos = [" ".join(c).replace("ü", "v") for c in product(*options)]
        return combos if len(combos) <= 4 else None

    def add(text, category):
        text = t2s.convert(text.strip())
        if not han.match(text) or text in rows:
            return
        found = readings(text)
        if found:
            rows[text] = [{"text": text, "reading": r, "category": category, "source_url": base, "license_note": lic} for r in found]

    poems = [json.load(open(f, encoding="utf-8")) for f in sorted(glob.glob(os.path.join(content_dir, "poems", "*.json")))]
    for poem in poems:
        author = poem["author"].strip()
        if 2 <= len(author) <= 4 and author not in ("不詳", "不详", "佚名", "无名氏"):
            add(author, "poet")
        title = re.sub(r"[（(].*?[）)]", "", poem["title"])
        if 2 <= len(title) <= 8:
            add(title, "poem-title")
        if poem["difficulty"] <= 2:
            for line in poem["content_lines"]:
                for clause in re.split(r"[，。！？、；：,.!?;: ]", line):
                    if 4 <= len(clause) <= 9:
                        add(clause, "poem-line")
    for f in sorted(glob.glob(os.path.join(content_dir, "idioms", "*.json"))):
        idiom = json.load(open(f, encoding="utf-8"))["idiom"]
        if len(idiom) == 4:
            add(idiom, "idiom")
    return [row for group in rows.values() for row in group]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("packs")
    ap.add_argument("out")
    ap.add_argument("--jiyili", help="jiyili/data/content directory")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    syllables = pinyin_syllables()
    p = args.packs
    poetry = []
    for name, keep in (("idioms", lambda r: True), ("poets", lambda r: True),
                       ("poem_titles", lambda r: len(r["text"]) <= 8)):
        poetry += [r for r in read(os.path.join(p, "poetry", name + ".tsv")) if keep(r)]
    famous = {}
    for line in open(os.path.join(p, "poetry", "provenance.jsonl"), encoding="utf-8"):
        rec = json.loads(line)
        if rec["file"] == "poem_lines.tsv" and any(s in rec["source_file"] for s in LINE_SOURCES):
            famous[rec["text"]] = rec["source_file"]
    for r in read(os.path.join(p, "poetry", "poem_lines.tsv")):
        n = len(r["text"])
        if r["text"] in famous and (n in (5, 7) or (4 <= n <= 9 and "宋词" in famous[r["text"]])):
            poetry.append(r)
    if args.jiyili:
        have = {r["text"] for r in poetry}
        poetry += [r for r in jiyili_rows(args.jiyili) if r["text"] not in have]
    write(os.path.join(args.out, "poetry.zh.tsv"), poetry)
    cad = [r for r in read(os.path.join(p, "cad", "cad_zh.tsv")) if not GUI_VERB.match(r["text"]) and 2 <= len(r["text"]) <= 7]
    write(os.path.join(args.out, "cad.zh.tsv"), cad)
    write(os.path.join(args.out, "cad.ascii.tsv"), ascii_rows(read(os.path.join(p, "cad", "cad_ascii.tsv")), syllables))
    industry = [r for r in read(os.path.join(p, "industry", "industry_zh.tsv")) if 2 <= len(r["text"]) <= 8]
    write(os.path.join(args.out, "industry.zh.tsv"), industry)
    write(os.path.join(args.out, "industry.ascii.tsv"), ascii_rows(read(os.path.join(p, "industry", "industry_ascii.tsv")), syllables))
    for name in ("poetry.zh", "cad.zh", "cad.ascii", "industry.zh", "industry.ascii"):
        print(name, sum(1 for _ in open(os.path.join(args.out, name + ".tsv"), encoding="utf-8")) - 1)


if __name__ == "__main__":
    main()
