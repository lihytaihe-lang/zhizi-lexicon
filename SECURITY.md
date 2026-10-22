# 安全政策 · Security Policy（词库仓库 / lexicon repository）

[中文](#中文) · [English](#english)

---

## 中文

### 支持的版本

| 版本 | 是否支持 |
|---|---|
| 最新发布版 | 支持 |
| 更早版本 | 不支持 |

### 如何报告

- **请通过 GitHub 私密漏洞报告（private vulnerability reporting）提交**：入口在仓库的 Security 标签 → Report a vulnerability。
- 不要用公开 issue 报告安全问题。

### 范围

- **本仓库**：词库数据文件、生成/校验/打包脚本、发布包（MANIFEST/SHA256SUMS）。
  例如：发布包校验和与实际内容不符、贡献检查工具在处理投稿时回显或泄露提交内容、
  打包脚本对恶意输入的不安全行为（路径穿越、跟随符号链接等）。
- **不在范围**：输入法应用本身的安全问题（请到输入法仓库报告）；上游数据源
  （THUOCL、jieba、pypinyin 等）的问题请向上游报告。
- 词库是数据：恶意「词条内容」更多是滥用问题（诱导候选、冒名词条），请用普通 issue
  报告；只有影响机密性/完整性/可用性的技术问题才走安全渠道。

### 响应

尽力而为，不承诺具体时限。报告请附：涉及的文件与行、词库版本（FILES.sha256 或发布包版本）、复现命令。

---

## English

### Supported versions

| Version | Supported |
|---|---|
| Latest release | Yes |
| Older versions | No |

### Reporting

- **Please report via GitHub private vulnerability reporting**: the repository's Security tab → Report a vulnerability.
- Do not use public issues for security reports.

### Scope

- **This repository**: lexicon data files, the generation/check/packaging scripts, and release packs (MANIFEST/SHA256SUMS). For example: checksums that do not match shipped content, the contribution checker echoing or leaking submitted content, unsafe handling of malicious input in the packager (path traversal, following symlinks).
- **Out of scope**: security issues in the input-method app itself (report to the input-method repository); issues in upstream data sources (THUOCL, jieba, pypinyin, …) go upstream.
- The lexicon is data: malicious "entries" are mostly abuse (manipulative candidates, impersonating entries) — report those as ordinary issues; only technical confidentiality/integrity/availability issues belong in the security channel.

### Response

Best effort, no committed timelines. Include: affected file(s) and lines, the lexicon version (from FILES.sha256 or the release pack), and a reproduction command.
