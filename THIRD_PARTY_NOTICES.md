# Third-party notices — zhizi-lexicon

以下摘自输入法仓库根 THIRD_PARTY_NOTICES.md；保留原文，段后标注原文件行号。 / Verbatim excerpts; source line ranges follow each paragraph.

## Rime Pinyin Simplified Dictionary

> Source: THIRD_PARTY_NOTICES.md:L13-L13

The `rime-pinyin-simp` dictionary is licensed under the Apache License 2.0.

> Source: THIRD_PARTY_NOTICES.md:L15-L15

Source: https://github.com/rime/rime-pinyin-simp

> Source: THIRD_PARTY_NOTICES.md:L17-L17

The project-authored schema is separate from the unmodified upstream dictionary. The bundle carries the fixed upstream `LICENSE` and `AUTHORS` files.

> Source: THIRD_PARTY_NOTICES.md:L19-L19

## THUOCL lexicons (chengyu, IT, caijing)

> Source: THIRD_PARTY_NOTICES.md:L21-L21

`agent_idioms.dict.yaml`, `agent_thuocl_it.dict.yaml`, and `agent_thuocl_caijing.dict.yaml` are generated from the 8,519-row chengyu, 16,000-row IT, and 3,830-row caijing tables at commit `a30ce79d895d01ab5132a5c74c29703ff7efb4cc`. The generated dictionaries are deduplicated against the pinned base and each other and distributed under the MIT License, Copyright (c) 2018 THUNLP. The input-method bundle carries the existing full `THUOCL-MIT.txt` license. `pypinyin` 0.55.0 (MIT) supplies reproducible build-time readings; its code is not bundled. Its phrase data now also contributes to the general vocabulary layer below, which carries the full pypinyin notice.

> Source: THIRD_PARTY_NOTICES.md:L23-L23

Source: https://github.com/thunlp/THUOCL

> Source: THIRD_PARTY_NOTICES.md:L25-L25

## General vocabulary and new words

> Source: THIRD_PARTY_NOTICES.md:L27-L27

`agent_general.dict.yaml` contains 26,947 reviewed entries, SHA-256 `cb656a657b7e8edbe0de5c2c25c019fb3c94d3368d6611c04828771a4b99eb93`. Sources are jieba 0.42.1 `dict.txt` (MIT; PyPI source archive SHA-256 `055ca12f62674fafed09427f176506079bc135638a14e23e25be909131928db2`, author Sun, Junyi), pypinyin 0.55.0 phrase data (MIT; Copyright (c) 2016 mozillazg, 闲耘), and project-authored mined/generated phrases. Per-row sources, counts and grants are preserved in `quality/corpus/agent-general-provenance.tsv` (SHA-256 `610c58f3dc1e5c7c8d0ce3a2eca79a529dafac478681625a86727e2adc6e5c8b`). No third-party Python implementation is bundled.

> Source: THIRD_PARTY_NOTICES.md:L29-L29

`agent_newwords.dict.yaml` is a separately replaceable 14,633-entry project-authored layer (recent coinages, everyday modern words and spoken phrases, and category-by-category names of everyday things; DeepSeek-generated, 2026-10-17), SHA-256 `ea30dbe7defde2c427d83aa314f567fa7a5c7fc713e360299ad43912194a227b`; `quality/corpus/agent-newwords-provenance.tsv` (SHA-256 `ac717eca076a96a2c6129b455675b413699788b407a93eb4c68ac1eae2c68325`) preserves generation/review source and corpus counts. The original two exports were SHA-verified before import. The general layer was re-exported with 10 explicit frozen-gate exclusions; every retained entry and the new-word export are byte-identical. The new-word layer was re-exported from the repository after review found its first export had run outside it (179 duplicates of shipped words, no first-choice caps); it now drops every shipped word and caps 116 weights below the existing first choice.

> Source: THIRD_PARTY_NOTICES.md:L31-L31

`agent_spoken.dict.yaml` is a separately replaceable 10,853-row spoken-phrase layer (everyday chat combinations such as 你看下, 我刚刚, 捞手机, plus interface and everyday-operation phrases such as 前一页, 上一步, 长按保存; regenerated 2026-10-16), SHA-256 `1294b968bfb0e6e2946991c349ea1f62dc3afa388bc984963216e2a26c2f4293`; `quality/corpus/agent-spoken-provenance.tsv` (SHA-256 `8651403810bea8474e955c7d1e9e2856f1bd35a834b710b7e3c473cf710aedfb`) records, per row, how many independent generation calls produced it and how many backends did (one: DeepSeek). The phrases were generated from scenario prompts through the DeepSeek API (DeepSeek's terms of use, section 4.2(3), allow using outputs for derivative products and for training other models; the earlier version of this layer was generated with other providers whose terms do not allow this, and was replaced on 2026-10-16). A phrase is kept when it has at least three characters and at least five independent generation calls produced it. Readings come from pypinyin, with a second reading added where an independent check by DeepSeek disagreed on a heteronym character. Only the prompts left the machine; no owner data was read or sent. This layer can be dropped independently.

> Source: THIRD_PARTY_NOTICES.md:L33-L33

`agent_ai_terms.dict.yaml` (286 entries, SHA-256 `2e4e058bc42a1a83f4fedf1c9b2a31ed93d63f1c7558f63dcdef01caed2ec4b3`) and `agent_ai_names.dict.yaml` (24 entries, SHA-256 `c458a49954b7e2f9f1e53942f2ee5b9deb4601fb2c80b53e256a72e947af9a7f`) are separately replaceable layers of AI-era product, company, model and tool names (WorkBuddy, DeepSeek, Claude Code; 硅基流动, 火山方舟), 2026-10-13. Each entry was seen on an official or authoritative web page by a research pass and is recorded with that page's URL and the check date in `quality/corpus/agent-ai-terms-provenance.tsv` (SHA-256 `464574b1bcb3e16fd7cae28dd3ba4617dd837c6425cb4c40f0c56a2ed0cf1680`) and `quality/corpus/agent-ai-names-provenance.tsv` (SHA-256 `b25c5e6d77715665675635593167b1667a7c3aa85b114e8fbfa419c9a20df4ec`). Only names and their official spelling are used (facts); no page text is copied. Product names are trademarks of their owners and are listed only to be typed.

> Source: THIRD_PARTY_NOTICES.md:L35-L35

`agent_pack_poetry.dict.yaml` (14,880 entries), `agent_pack_cad.dict.yaml` (687), `agent_pack_industry.dict.yaml` (2,011) and `agent_pack_terms.dict.yaml` (319 ASCII names, formats and acronyms; loaded by the core, not imported into Rime) are separately replaceable optional vocabulary packs (2026-10-13). They are lists of terms only; no definitions, translations, example sentences or page text are copied. Every row has its source URL, check date and licence note in `quality/corpus/agent-pack-{poetry,cad,industry,terms}-provenance.tsv`. Sources and their licences: Wiktionary Chinese chengyu category titles and Chinese Wikipedia / English Wikipedia names and category titles (CC-BY-SA-4.0, contributors of those projects; used as lists of facts); chinese-poetry (MIT, classical originals in the public domain) for poets, poem titles and anthology line fragments from Tang 300, Qianjia, Shuimo Tang poems and Song ci 300, and the selection of 1,500 poems and 300 idioms of the owner's own jiyili project (texts from chinese-poetry and chinese-xinhua, public domain); Wikisource transcription of the Nineteen Ancient Poems (public-domain originals); FreeCAD Chinese interface terms (LGPL-2.1-or-later, FreeCAD contributors; terminology only, no program code); jieba dictionary (MIT, Copyright (c) 2013 Sun Junyi) for industrial terms. Product, company and standard names are trademarks of their owners and are listed only to be typed. If the packs are redistributed on their own, keep these notices with them.

> Source: THIRD_PARTY_NOTICES.md:L37-L37

The full `pypinyin-MIT.txt` and `jieba-MIT.txt` notices are bundled and locked by byte count and SHA-256. The jieba 0.42.1 source archive declares MIT but omits the LICENSE file; the notice is the upstream LICENSE at tag v0.42.1 (commit `1e20c89b66f56c9301b0feed211733ffaa1bd72a`, Copyright (c) 2013 Sun Junyi), 1,075 bytes, SHA-256 `18ba0984839f85853b29fadaf992f7dba8fd0ca0fbeae34de2b8735222dc7a37`.

> Source: THIRD_PARTY_NOTICES.md:L41-L41

