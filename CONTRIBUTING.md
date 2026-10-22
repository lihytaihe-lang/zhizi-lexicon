# 贡献指南 · Contributing（词库仓库 / lexicon repository）

[中文](#中文) · [English](#english)

---

## 中文

### 怎么提交词条

词库接受 PR 投稿。投稿是 TSV 文件，放在 `contrib/` 目录（例如 `contrib/my-words.tsv`），每行一条：

```text
词<TAB>拼音[<TAB>权重]
```

规则（由 `scripts/lexicon/check_contribution.py` 检查；投稿前请先本地自检，PR 合并前也会用同一工具检查）：

- 词必须是 2–8 个纯汉字；不能是单个字、ASCII、数字或表情符号。
- 拼音音节之间用一个空格，不带声调，`ü` 写作 `v`（如「绿豆」写 `lv dou`）；音节数必须与字数一致。
- 权重可省略；填则是 1–1000 的整数。
- `#` 开头是注释，空行忽略；每行最多 3 列。
- 与现有词库（同词同音）、与本投稿文件内已有条目重复，会判失败。
- **隐私**：请勿提交包含个人信息的词句；检查工具会拒绝形如手机号、邮箱、网址的内容，且不会在报告里回显词条内容。
- 提示（不判失败）：现有词的新读音、叠字词、单次超过 500 条的投稿会给出警告。

流程：fork → 在 `contrib/` 加 TSV 文件 → 发 PR。维护者会在例行的词库更新里把采纳的词条并入相应词层；**不要直接改 `native/resources/Rime/` 下的词典**，它们是生成/冻结产物。本地自检：

```sh
python3 scripts/lexicon/check_contribution.py contrib/my-words.tsv --rime native/resources/Rime
```

（只需 Python 标准库。）也可以只开 issue 建议词条（用「词条建议」模板），不一定非要 PR。

### 贡献的授权

- **词条投稿按 CC0 1.0（公有领域贡献）授权**：在法律允许的范围内，你放弃这些词条的著作权与邻接权，本项目可将其并入按 CC BY-SA 4.0 发布的词库，且无需为你署名。若你希望保留权利，请不要提交。
- 词库整体仍按 CC BY-SA 4.0 授权；你放弃的只是自己对所投词条的权利。单个词条通常不构成有创造性的作品，按 CC0 提交便于词库长期维护与将来的重新授权。
- 提交即表示内容为你本人创作或你有权提交，且不含他人未公开的私密信息。

### 行为与沟通

对事不对人，保持友善；行为准则遵循 Contributor Covenant（与输入法仓库相同，全文见其 CODE_OF_CONDUCT.md）。

---

## English

### How to submit entries

Contributions are accepted via PR. Add a TSV file under `contrib/` (e.g. `contrib/my-words.tsv`), one entry per line:

```text
word<TAB>pinyin[<TAB>weight]
```

Rules (implemented by `scripts/lexicon/check_contribution.py`; run it locally before submitting — the same check runs before a PR is merged):

- The word must be 2–8 pure Han characters: not a single character, ASCII, digits, or emoji.
- Pinyin syllables are separated by a single space, toneless, with `ü` written as `v` (e.g. 绿豆 is `lv dou`); the syllable count must match the character count.
- The weight is optional; when present it is an integer from 1 to 1000.
- Lines starting with `#` are comments; blank lines are ignored; at most 3 columns per row.
- Duplicates — same word and reading against the shipped dictionaries, or within your own file — fail the check.
- **Privacy**: do not submit words or phrases containing personal information; the checker rejects phone-number/email/URL shapes and never echoes submitted content in its report.
- Warnings (not failures): a new reading for an existing word, heavily repeated characters, and submissions over 500 entries at once.

Process: fork → add your TSV under `contrib/` → open a PR. Maintainers fold accepted entries into the dictionary layers during regular lexicon updates; **do not edit `native/resources/Rime/` dictionaries directly** — they are generated/frozen artifacts. Check locally:

```sh
python3 scripts/lexicon/check_contribution.py contrib/my-words.tsv --rime native/resources/Rime
```

(Python standard library only.) You may also just open an issue with the "word suggestion" template instead of a PR.

### Licensing of contributions

- **Entries you submit are dedicated to the public domain under CC0 1.0**: to the extent permitted by law, you waive copyright and related rights in them, and this project may fold them into the CC BY-SA 4.0 lexicon without attribution to you. Do not submit if you prefer to retain rights.
- The lexicon as a whole remains CC BY-SA 4.0; what you waive is only your own rights to the entries you submit. Individual entries usually do not constitute creative works, and CC0 keeps long-term maintenance and future relicensing of the lexicon simple.
- By submitting, you declare the content is yours to contribute and contains no one else's undisclosed private information.

### Conduct

Be respectful; critique the content, not the person. We follow the Contributor Covenant (same as the input-method repository; see its CODE_OF_CONDUCT.md).
