# zhizi-lexicon / 知字词库

官网 / Website: <https://zhizi.dabblecove.com/>

中文词库的权威来源仓库：已生成好的词典成品、逐条来源（provenance）与许可清单，以及随迁的生成/校验工具。输入法仓库持有一份钉死版本的词库快照；本仓库是词库的单一权威来源。

This is the authoritative home of the Chinese lexicon: generated dictionary artifacts, per-row provenance and licensing information, plus the migrated generation and checking tools. The input-method repository consumes a pinned snapshot of a specific lexicon version; this repository is the single source of truth for lexicon content.

**本仓库当前发布的是成品数据，不是一套可以完全独立再生成全部派生文件的流水线。** 部分生成工具的输入包含仍留在输入法仓库里的文件，详见下文「限制」。/ **This repository ships finished data, not a pipeline that can fully regenerate every derived file on its own.** Some generators take inputs that remain in the input-method repository; see *Limitations* below.

## 与输入法仓库的关系 / Relationship to the input-method repository

- 输入法仓库（Apache-2.0，另行发布）在其源码树里钉死了某个词库版本的快照（`native/resources/Rime/` 下的词典与派生 TSV），并参与编译与打包。
- 快照的版本登记与一致性校验（SNAPSHOT 机制）**尚在规划中，未实现**；目前输入法侧靠逐文件 sha256 校验脚本对账。
- 词库更新器、下载窗口均为**规划中**，本仓库与输入法都未实现。
- 词库内容（含词典、派生索引、provenance）以本仓库为权威；输入法侧不应手改快照。

- The input-method repository (Apache-2.0, published separately) pins a snapshot of one lexicon version in its source tree and compiles/packages it.
- Version registration and consistency checking of the snapshot (a SNAPSHOT manifest) are **planned but not implemented**; today the input-method side reconciles via per-file sha256 checks.
- A lexicon updater and download UI are **planned only**; neither repository implements them.
- Lexicon content is authoritative here; the input-method side must not hand-edit its snapshot.

## 内容 / Contents

Core 与 extension 是输入法自带的通用词库层，pack（诗词、CAD、行业）为默认关闭的可选专业包。/ Core and extension ship enabled with the input method; packs are optional and off by default.

| Group / 层组 | Catalog rows / 条数 |
|---|---:|
| core | 117715 |
| extension | 22335 |
| pack | 17578 |

数字由 `native/resources/Lexicon/lexicon_catalog.json` 汇总，含上游基础表 `pinyin_simp`（65,125 条，钉死版本未随本仓库分发）。`agent_ai_terms` 与 `agent_pack_terms` 已随本仓库发布，但在 catalog 中列为 unlisted，不计入上表；catalog 的 unlisted 还包括留在输入法侧的表（`agent_pinyin`、`agent_english`、`agent_project_terms`、`agent_tech_terms`）。catalog 保持与输入法仓库逐字节一致，因此它的 unlisted 清单并不等于本目录的文件清单。

Counts are summed from the catalog, including the upstream `pinyin_simp` base (65,125 rows; the pinned upstream copy is not distributed here). The ASCII tables `agent_ai_terms`/`agent_pack_terms` are included here but unlisted in the catalog; the catalog's unlisted entries also name IME-side tables absent here. The catalog is byte-identical to the input-method copy, so its unlisted list does not equal this directory's manifest.

## 可独立运行的部分 / What runs standalone here

以下均已在本目录实测通过（见仓库报告，不承诺其他环境）：/ Each item below was verified in this directory (see the report; no promise for other environments):

```sh
# 单元测试（36 项：build_catalog / build_release_pack / check_contribution）
# Unit tests (36: build_catalog / build_release_pack / check_contribution)
cd scripts/lexicon
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -p 'test_*.py'

# heavy_garble 生成器校验（无需输入法侧文件；需钉死的上游基础表，见下节）
# heavy_garble generator check (no IME-side inputs; needs the pinned upstream base, see below)
cd ../..
node scripts/generate_heavy_garble_words.mjs --check

# 贡献检查工具（对任意 --rime 目录运行，供词库投稿校验）
# Contribution checker (runs against any --rime directory; used for entry submissions)
PYTHONDONTWRITEBYTECODE=1 python3 scripts/lexicon/check_contribution.py contrib/*.tsv --rime native/resources/Rime

# 发布包构建（产出字典、纯文本 TSV、MANIFEST.json、SHA256SUMS 与 tar.gz）
# Release pack build (dictionaries, plain TSV, MANIFEST.json, SHA256SUMS, tar.gz)
PYTHONDONTWRITEBYTECODE=1 python3 scripts/lexicon/build_release_pack.py \
  --rime native/resources/Rime --provenance quality/corpus --version 2026.10 --out dist
```

说明 / Notes:

- 单测只使用合成夹具，不读取任何真实输入记录。/ Unit tests use synthetic fixtures only; no real input records are read.
- `build_release_pack.py` 可运行，但内部逐层来源/许可审计文档未随本仓库导出，在本仓库里自行构建时 MANIFEST 的 source/license 字段会写 `TODO`（见下文）；维护者发布的归档由完整审计构建，不带 `TODO`。/ `build_release_pack.py` runs, but the internal layer-audit document is not part of this repository, so a pack you build here gets `TODO` in MANIFEST source/license cells (below); archives published by the maintainers are built with the full audit and carry none.
- 各生成器还需要钉死的上游基础表 `.build-deps/rime-pinyin-simp/0c6861ef7420ee780270ca6d993d18d4101049d0/pinyin_simp.dict.yaml`（Apache-2.0，rime-pinyin-simp）。它不属于本仓库，也不随本仓库分发；当前用指向输入法仓库 `.build-deps` 的本地符号链接仅为验证，发布时不得包含该链接。获取方式待定（见「未决事项」）。/ The generators also need the pinned upstream base `.build-deps/rime-pinyin-simp/0c6861ef…/pinyin_simp.dict.yaml` (Apache-2.0, rime-pinyin-simp). It is not part of this repository and is not distributed here; the symlink to the input-method checkout exists for local verification only and must not be published. How to fetch it is undecided (see *Open items*).

## 限制：依赖输入法仓库输入的生成器 / Limitations: generators that need input-method-repo inputs

这些工具随迁保留原样，但**暂时不能只靠本仓库完整再生成**，`--check` 在本目录会失败：/ These tools are copied unchanged, but **this repository alone cannot fully regenerate the derived files**; their `--check` runs fail here:

- `scripts/generate_exact_reading_index.mjs`（派生 `agent_exact_readings.tsv`、`agent_extra_readings.tsv`、`agent_factory_reading_priorities.tsv`）：输入含输入法侧的 `agent_pinyin.dict.yaml`（聚合导入表）、`agent_english.dict.yaml`、`agent_project_terms.dict.yaml`、`agent_tech_terms.dict.yaml`，另有钉死 `pinyin_simp`。缺前三者之外，`agent_pinyin`/`agent_english`/`agent_project_terms`/`agent_tech_terms` 均不在本目录。
  / Inputs include the IME-side `agent_pinyin.dict.yaml` (aggregate import table), `agent_english.dict.yaml`, `agent_project_terms.dict.yaml`, `agent_tech_terms.dict.yaml`, plus the pinned `pinyin_simp`; none of those four tables is present here.
- `scripts/generate_idiom_dictionary.py` 与 `scripts/generate_modern_dictionary.py`：需要 `pypinyin`（未随附），并把 `agent_english`、`agent_project_terms`、`agent_tech_terms`（及 modern 的其余去重输入中的输入法侧表）当作去重边界，这些表不在本目录。
  / Both need `pypinyin` (not bundled) and deduplicate against `agent_english`, `agent_project_terms`, `agent_tech_terms` (IME-side tables absent here).
- `scripts/lexicon/build_catalog.py`：可以运行，但用本目录的词典子集再生成会得到不同的 `unlisted` 清单与 core 计数（catalog 的 unlisted 引用输入法侧表，且 core 计数含 `pinyin_simp` 基础表），**无法逐字节复现**随附的冻结 `lexicon_catalog.json` 与 `lexicon_membership.tsv`。
  / Runs, but regenerating from this subset yields a different `unlisted` list and core counts (the frozen catalog references IME-side tables and counts the `pinyin_simp` base); it **cannot reproduce** the shipped frozen `lexicon_catalog.json` / `lexicon_membership.tsv` byte-for-byte.
- 语料挖掘/审校流水线（`mine_words.py`、`judge_*.py`、`export_*.py`、`build_general_lexicon.py`、`curate_packs.py`、`evaluate_lexicon_owner.py`、`find_gaps.py` 等）依赖未随附的本地工作区、外部模型服务与 owner 本机记录，随迁存档用，本仓库不保证可运行，也不要在缺少明确输入时运行 owner 评估脚本。
  / The mining/curation pipeline depends on a local workspace, external model services and owner-local records that are not exported. It is archived as-is; running it is not supported here, and do not run the owner evaluators without explicit inputs.

## 本地打包 / Local packaging

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/lexicon/build_release_pack.py \
  --rime native/resources/Rime --provenance quality/corpus --version 2026.10 --out dist
(cd dist/zhizi-lexicon-2026.10 && shasum -a 256 -c SHA256SUMS)
```

打包输出字典、纯文本 TSV、MANIFEST.json、SHA256SUMS 和可复现归档。**注意：** 内部逐层许可审计文档不在本仓库里，自行构建时脚本会把来源/许可字段写为 `TODO`；带 TODO 的包不是许可完备的发布包，不得当作正式分发物，请使用维护者发布的归档。/ Packaging emits dictionaries, plain TSV, manifest, checksums and a reproducible archive. **Note:** the internal audit document is not in this repository, so a pack built here has `TODO` source/license cells; such a pack is not license-complete and must not be treated as an approved release. Use the archive the maintainers publish.

## 授权 / License

- 词库数据（`native/`、`quality/` 下的词典、派生表与逐层 provenance，以及发布归档）采用 **CC BY-SA 4.0**，全文见 `LICENSE`（与输入法仓库 `LICENSE-LEXICON` 逐字节一致）。
- 随迁的生成/校验工具代码（`scripts/` 下的 Python、Node 脚本及其测试）采用 **Apache-2.0**，全文见 `LICENSE-CODE`（与输入法仓库 `LICENSE` 一致）。`third_party/` 下的内容保持各自的上游许可。
- 第三方来源各自的许可与署名见 `THIRD_PARTY_NOTICES.md` 与逐层 provenance（`quality/corpus/*-provenance.tsv`）；本仓库不重新认定第三方许可。
- 词库作为数据文件被打包进输入法再分发时，CC BY-SA 4.0 的署名与相同方式共享要求仍然适用；具体合规请自行确认。
- 输入法代码同为 Apache-2.0（另一仓库）；皮肤单独授权，不在本仓库范围内。

- Lexicon data (dictionaries, derived tables and per-layer provenance under `native/` and `quality/`, plus the release archives): **CC BY-SA 4.0**; see `LICENSE` (byte-identical to `LICENSE-LEXICON` in the input-method repository).
- The migrated generation and checking tools (the Python and Node scripts under `scripts/` and their tests): **Apache-2.0**; see `LICENSE-CODE` (same text as `LICENSE` in the input-method repository). Content under `third_party/` keeps its upstream licenses.
- Third-party sources keep their own licenses and attribution as recorded in `THIRD_PARTY_NOTICES.md` and the per-row provenance files; this repository does not re-adjudicate them.
- When the lexicon is packaged into the input method as data files, the attribution and ShareAlike requirements of CC BY-SA 4.0 still apply; please confirm compliance for your own distribution.
- The input-method code is Apache-2.0 as well (separate repository); skins are separately licensed and out of scope here.

## 追溯 / Provenance of this export

`FILES.sha256` 记录 70 个从输入法仓库复制的文件的 sha256 与源路径。唯一例外：`scripts/lexicon/test_check_contribution.py` 在本目录做了有意修改（修正包导入路径，使其不依赖仓库根位置），详见 `FILES.sha256` 中该行附近的注释（含新旧 sha256）；除此之外全部文件与源逐字节一致。

`FILES.sha256` lists the sha256 and source path of the 70 files copied from the input-method repository. One intentional exception: `scripts/lexicon/test_check_contribution.py` was modified here (package-import path fix so it works regardless of the repository root); see the comment next to that line in `FILES.sha256` (old and new sha256 included). Every other file is byte-identical to its source.

## 未决事项 / Open items

- 钉死上游基础表 `pinyin_simp` 的获取方式（本仓库自行下载脚本，或随仓库分发）未定。/ How to obtain the pinned `pinyin_simp` base (a fetch script here vs. distributing it) is undecided.
- exact/idiom/modern 生成器对输入法侧表的输入耦合如何拆解（把输入迁来、参数化，或接受"成品 + 校验"模式）未定。/ How to decouple the exact/idiom/modern generators from IME-side inputs is undecided.
- 公开版逐层来源/许可总表（替代内部审计文档、供 `build_release_pack.py` 读取）未建。/ A public per-layer source/license summary (replacing the internal audit for `build_release_pack.py`) does not exist yet.
- 快照（SNAPSHOT）登记机制与词库更新器：规划中。/ The SNAPSHOT manifest and the lexicon updater: planned.
