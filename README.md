# ai-apply-skill

AI 競賽/補助報名自動化 Skill，支援台灣主要競賽與政府補助平台。將 1–2 天的人工查閱與整理，壓縮至 2 小時內完成。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 功能概覽

- 🔍 **自動調研**：抓取競賽簡章（HTML/PDF），建立競賽資訊表、競品比較矩陣
- ✍️ **文件撰寫**：產出作品說明書、簡報腳本、加分佐證文件清單
- 📋 **自動填表**：依環境選擇 Computer Use / Playwright 腳本 / 半自動輔助
- 🗂️ **平台知識庫**：預設支援獎金獵人、SBIR、文化部補助等台灣主要平台

---

## Installation

### 方式一：Claude Code / Claude Desktop（推薦）

```bash
# 安裝到使用者層級（跨專案可用）
git clone https://github.com/your-username/ai-apply-skill.git ~/.claude/skills/ai-apply
```

安裝完成後，在 Claude Code 或 Claude Desktop 中輸入 `/ai-apply` 即可觸發。

### 方式二：一鍵安裝腳本

```bash
curl -sL https://raw.githubusercontent.com/your-username/ai-apply-skill/main/install.sh | bash
```

`install.sh` 會自動複製到 `~/.claude/skills/ai-apply/`，並提示建立 `user-profile.yaml`。

### 方式三：手動安裝到其他 AI 工具

依照各工具的 Skills 載入路徑安裝：

| AI 工具 | 安裝路徑 |
|---------|---------|
| Claude Code / Desktop | `~/.claude/skills/ai-apply/` |
| Cursor | 專案內 `.cursor/skills/ai-apply/` |
| Gemini CLI | 專案內 `.gemini/skills/ai-apply/` |
| Windsurf | 專案內 `.claude/skills/ai-apply/` |

```bash
# 以 symbolic link 方式安裝到多個工具（在專案根目錄執行）
git clone https://github.com/your-username/ai-apply-skill.git ./ai-apply
ln -s "$(pwd)/ai-apply" .claude/skills/ai-apply
ln -s "$(pwd)/ai-apply" .cursor/skills/ai-apply
ln -s "$(pwd)/ai-apply" .gemini/skills/ai-apply
```

---

## Configuration

安裝後**必須**設定個人資料檔：

```bash
# 1. 複製範例檔
cp ~/.claude/skills/ai-apply/user-profile.yaml.example \
   ~/.claude/skills/ai-apply/user-profile.yaml

# 2. 填入您的真實資料
vi ~/.claude/skills/ai-apply/user-profile.yaml
```

`user-profile.yaml` 結構如下：

```yaml
company:
  name: "您的公司名稱"
  tax_id: "統一編號"
  founded: "YYYY-MM-DD"
  address: "公司地址"
  website: "https://your-company.com"
  description: "公司簡介"

team:
  - name: "姓名"
    role: "職稱"
    email: "email@company.com"
    phone: "09XX-XXX-XXX"
    linkedin: "https://linkedin.com/in/username"

contact:
  primary_name: "主要聯絡人姓名"
  primary_email: "email@company.com"
  primary_phone: "09XX-XXX-XXX"
```

> ⚠️ **隱私警告**：`user-profile.yaml` 含有真實個人資料，已加入 `.gitignore`，**請勿提交至 git**。

---

## Usage

觸發 Skill：

```
/ai-apply
```

Skill 執行三個階段：

### 階段 1：調研與競品分析

1. 自動查詢 `knowledge/competition-platforms.md` 匹配競賽名稱
2. 使用 `tools/fetch-and-convert.py` 抓取競賽簡章
3. 產出：競賽資訊表、競品比較矩陣、參賽方向建議書
4. ✋ **停止點**：用戶確認參賽方向後繼續

### 階段 2：文件撰寫與 MVP 設計

1. 根據競賽要求撰寫作品說明書、提案書
2. 產出簡報腳本、加分佐證文件清單
3. ✋ **停止點**：用戶確認大綱後展開全文

### 階段 3：自動化填表

依環境選擇策略：

| 環境 | 策略 | 自動化程度 |
|------|------|-----------| 
| Claude Code / Anthropic API | Level 1: Computer Use | 最高 |
| 有 Python/Node.js | Level 2: Playwright 腳本 | 中高 |
| 其他 AI Agent | Level 3: 生成→人工貼上 | 中 |

---

## Supported Platforms

內建知識庫（`knowledge/competition-platforms.md`）包含：

| 平台 | 類型 | URL |
|------|------|-----|
| 獎金獵人 Bounty Hunter | 競賽 | https://bhuntr.com/ |
| 經濟部 SBIR | 補助 | https://www.sbir.org.tw/ |
| 文化部補助 | 補助 | https://grants.moc.gov.tw/ |

**新增自定義平台**：在 `knowledge/competition-platforms.md` 依照文件內的格式範本新增 `### 平台名稱` 區段即可，不需要修改程式碼。

---

## 網頁爬取工具

`tools/fetch-and-convert.py` 可獨立使用：

```bash
# 抓取網頁轉 Markdown（stdout）
python ~/.claude/skills/ai-apply/tools/fetch-and-convert.py https://example.com

# 輸出到檔案
python ~/.claude/skills/ai-apply/tools/fetch-and-convert.py https://example.com --output /tmp/guidelines.md
```

**依賴安裝**（選用，有更佳的轉換品質）：

```bash
pip install requests html2text     # 網頁爬取 + HTML 轉 Markdown
pip install pdfminer.six           # PDF 文字擷取
```

無上述套件時，工具會使用內建的 stdlib-only fallback，仍可運作。

---

## 注意事項

- 本 Skill 不做全自動無人值守的表單提交（敏感操作需人工確認）
- 不處理付費報名金流
- 首版僅支援台灣競賽/補助平台

---

## License

MIT License — 詳見 [LICENSE](LICENSE) 文件。
