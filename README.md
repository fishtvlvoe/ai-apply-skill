# ai-apply-skill

AI 競賽／補助報名自動化 Skill，支援台灣主要補助、競賽與政府採購平台。

將 1–2 天的人工查閱與整理，壓縮至 2 小時內完成查閱、整理、歸納、自動填表。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platforms](https://img.shields.io/badge/Platforms-15+-blue.svg)](#supported-platforms)
[![Auto Update](https://img.shields.io/badge/知識庫-每週自動更新-green.svg)](../../actions/workflows/update-knowledge.yml)
[![Weekly Report](https://img.shields.io/badge/週報-訂閱_Issues-orange.svg)](../../issues?q=label%3Aweekly-update)

---

## 功能概覽

- 🔍 **自動調研**：抓取競賽簡章（HTML/PDF），建立競賽資訊表、競品比較矩陣
- ✍️ **文件撰寫**：產出作品說明書、簡報腳本、加分佐證文件清單
- 📋 **自動填表**：依環境選擇 Computer Use / Playwright 腳本 / 半自動輔助
- 🗂️ **平台知識庫**：15+ 台灣主要補助、競賽、標案平台，結構化資料自動帶入流程
- 🤖 **每週自動更新**：GitHub Action 定期爬取各平台，同步最新補助金額、截止日、受理狀態
- 📬 **週報 Issue 通知**：每週一自動建立 GitHub Issue，訂閱後收 email 即可掌握最新機會

---

## 每週訂閱（零安裝）

不需要安裝任何軟體，只要訂閱 Issue 即可每週收到補助/競賽機會彙整：

1. 前往此 repo → 右上角 **Watch** → **Custom**
2. 勾選 **Issues** → Save
3. 每週一收到 email，包含：
   - ⚡ 自動偵測「仍在受理申請」的補助
   - 22 縣市地方型 SBIR 即時狀態（由 [backtrue/sbir-grants](https://github.com/backtrue/sbir-grants) 同步）
   - 近期競賽活動
   - 政府標案關鍵字建議

最新週報：[Issues › weekly-update](../../issues?q=label%3Aweekly-update)

---

## Installation

### 方式一：Claude Code / Claude Desktop（推薦）

```bash
git clone https://github.com/fishtvlvoe/ai-apply-skill.git ~/.claude/skills/ai-apply
```

安裝後在 Claude Code 中輸入 `/ai-apply` 即可觸發。

### 方式二：其他 AI 工具

| AI 工具 | 安裝路徑 |
|---------|---------|
| Claude Code / Desktop | `~/.claude/skills/ai-apply/` |
| Codex CLI | 專案內 `AGENTS.md` 中 reference 此 Skill 路徑 |
| Cursor | 專案內 `.cursor/skills/ai-apply/` |

---

## Configuration

安裝後設定個人資料（填表時自動帶入）：

```bash
cp ~/.claude/skills/ai-apply/user-profile.yaml.example \
   ~/.claude/skills/ai-apply/user-profile.yaml

vi ~/.claude/skills/ai-apply/user-profile.yaml
```

`user-profile.yaml` 包含公司名稱、統編、聯絡人等欄位。已加入 `.gitignore`，**請勿提交至 git**。

---

## Usage

```
/ai-apply
```

執行流程：

**1. 速覽當前機會**（`knowledge/UPCOMING.md`）
啟動時自動讀取，列出目前常態受理與即將截止的補助/競賽。

**2. 調研與競品分析**
- 自動匹配 `knowledge/competition-platforms.md` 的平台資料
- 抓取競賽簡章，產出競賽資訊表、競品比較矩陣、參賽方向建議書
- ✋ 停止點：確認方向後繼續

**3. 文件撰寫**
- 根據競賽要求撰寫作品說明書、提案書、簡報腳本
- ✋ 停止點：確認大綱後展開全文

**4. 自動化填表**

| 環境 | 策略 | 自動化程度 |
|------|------|------------|
| Claude Code / Anthropic API | Level 1: Computer Use | 最高 |
| Codex CLI | Level 2: Bash + Python 腳本 | 中高 |
| Kimi MCP (`mcp__kimi-code__*`) | Level 2: 文件分析 + 草稿生成 | 中高 |
| 有 Python/Node.js | Level 2: Playwright/Puppeteer 腳本 | 中高 |
| Kimi Code（VS Code 插件） | Level 3: 半自動輔助（生成→人工貼上） | 中 |
| 其他 AI Agent | Level 3: 半自動輔助（生成→人工貼上） | 中 |

> Kimi CLI 已於 2026-05-24 停用，請改用 Kimi MCP。

---

## Supported Platforms

知識庫（`knowledge/competition-platforms.md`）涵蓋 15+ 平台，由 GitHub Action 每週自動更新：

### 補助類

| 平台 | 補助上限 | 特色 |
|------|----------|------|
| [經濟部 SBIR](https://www.sbir.org.tw/) | Phase 2 最高 1,200 萬 | 中小企業創新研發，rolling 隨到隨審 |
| [全台地方型 SBIR（22縣市）](https://github.com/backtrue/sbir-grants) | 個別 100 萬 / 聯合 200 萬 | 每週自動同步縣市受理狀態 |
| [經濟部 AI+ 計畫](https://eii.nat.gov.tw/moeai-plus/) | 個案最高 500 萬 | 製造業/服務業 AI 數位轉型三階段 |
| [DIGITAL+ 數位服務創新補助](https://digiplus.adi.gov.tw/) | 最高 500 萬 | 數位產業署，軟體/資訊服務業適用 |
| [SIIR 服務業創新研發](https://sme.moeasmea.gov.tw/) | Phase 2 最高 500 萬 | SBIR 服務業版本 |
| [文化部補助](https://grants.moc.gov.tw/Web/) | 依計畫各異 | 文創/出版/音樂/影視 |
| [中小企業數位轉型補助](https://www.sme.gov.tw/) | 最高 10 萬 | 電商/雲端/數位行銷 |
| [國科會計畫補助](https://www.nstc.gov.tw/) | 依計畫各異 | 企業透過產學合作參與 |
| [中小及新創企業署](https://www.sme.gov.tw/) | 多計畫整合入口 | 8 大輔導主軸單一入口 |
| [G2B 企業得來速 smepass](https://www.sme.gov.tw/smepass) | — | 輸入統編即篩選適合計畫 |
| [經濟部補助計畫入口網](https://buzu.moea.gov.tw/NewPortal/) | 多計畫整合入口 | 工業局/商業司/中小企業處 |

### 競賽類

| 平台 | 特色 |
|------|------|
| [獎金獵人 Bounty Hunter](https://bhuntr.com/tw/competitions) | 台灣最大競賽聚合平台，含 QITC 高通台灣創新競賽（入圍即 USD 10,000）|
| [Startup Terrace 台灣新創競技場](https://www.startupterrace.tw/) | 科技新創競賽（80 萬驗證金）、潛力新創選拔 Hi-Po Star |

### 標案類

| 平台 | 特色 |
|------|------|
| [政府電子採購網](https://web.pcc.gov.tw/) | 含 g0v pcc API 整合說明，AI/數位轉型標案關鍵字監控 |

### AI 輔助工具

| 工具 | 適用 |
|------|------|
| [sbir-grants（backtrue，MIT）](https://github.com/backtrue/sbir-grants) | SBIR 計畫書深度撰寫，170K+ 字知識庫，含 [SaaS 版](https://sbir.thinkwithblack.com/) |

> **自訂平台**：在 `knowledge/competition-platforms.md` 依格式範本新增 `### 平台名稱` 區段，不需修改程式碼。

---

## 自動更新機制

```
每週一 09:00（台灣時間）
  ├── 8 個 scraper 爬取各平台
  ├── 更新 knowledge/competition-platforms.md（⚡ 即時狀態注入）
  ├── 重新產生 knowledge/UPCOMING.md（常態受理 + 年度申請 + 自動偵測）
  ├── commit 到 main
  └── 建立 GitHub Issue（週報）→ Watch 訂閱者收 email
```

| Scraper | 資料來源 |
|---------|----------|
| eii_moea | 經濟部 AI+ 官網（受理狀態偵測）|
| sbir | sbir.org.tw（補助金額、公告）|
| pcc_tender | pcc-api.openfun.app（g0v 標案 API）|
| digiplus | digiplus.adi.gov.tw（SPA，有限抓取）|
| sbir_county_tracker | backtrue/sbir-grants GitHub API（22 縣市即時狀態）|
| sme_portal | sme.gov.tw（最新公告）|
| startup_terrace | startupterrace.tw（近期活動）|
| bhuntr | bhuntr.com（SPA，有限抓取）|

**手動觸發**：[Actions → Update Knowledge Base → Run workflow](../../actions/workflows/update-knowledge.yml)

---

## 工具

### 網頁爬取工具

```bash
python ~/.claude/skills/ai-apply/tools/fetch-and-convert.py https://example.com
python ~/.claude/skills/ai-apply/tools/fetch-and-convert.py https://example.com --output /tmp/result.md
```

### 知識庫手動更新

```bash
pip install -r tools/requirements-scraper.txt
python tools/update-knowledge.py
```

---

## 注意事項

- 不做全自動無人值守的表單提交（敏感操作需人工確認）
- 不處理付費報名金流
- 政府網站可能有 SSL 憑證問題（macOS 本機），CI 環境（Ubuntu）不受影響
- bhuntr.com / digiplus.adi.gov.tw 為 React SPA，自動抓取能力有限

---

## License

MIT License — 詳見 [LICENSE](LICENSE) 文件。
