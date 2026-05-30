# AI-APPLY 安裝與放置位置指南

## 為什麼其他 AI 代理找不到這個 Skill？

### 問題根源

各 AI 工具（Claude Code、Claude Desktop、Cursor、Gemini、Windsurf 等）各自從**不同的固定路徑**載入 Skills。如果你把 Skill 放在專案目錄下的任意資料夾，只有當前這個工作階段（session）可能看得到，其他工具或重新開啟後就找不到。

### 各工具的 Skills 路徑對照表

| AI 工具 | Skills 載入路徑 | 說明 |
|---------|----------------|------|
| **Claude Code** | `~/.claude/skills/<name>/SKILL.md` | 使用者層級，跨專案可用 |
| **Claude Desktop** | `~/.claude/skills/<name>/SKILL.md` | 同上（與 Claude Code 共用） |
| **Cursor** | 專案內 `.cursor/skills/<name>/` 或設定檔 | 目前以專案為主 |
| **Gemini** | 專案內 `.gemini/skills/<name>/` | 專案綁定 |
| **Windsurf** | 專案內 `.claude/skills/<name>/` | 與 Claude 共用結構 |
| **OpenCode** | 專案內 `.opencode/skills/<name>/` | 專案綁定 |
| **通用 Agent** | 專案內 `.agent/skills/<name>/` 或 `.agents/skills/<name>/` | 依工具而異 |

### 正確的放置方式

#### 方式一：Claude 生態系（推薦，跨專案可用）

```bash
# 建立 skill 目錄
mkdir -p ~/.claude/skills/ai-apply

# 複製所有檔案
cp -r /path/to/ai-apply/* ~/.claude/skills/ai-apply/
```

這樣 Claude Code 和 Claude Desktop 都能用 `/ai-apply` 觸發。

#### 方式二：專案內統一安裝（適合團隊協作）

在專案根目錄建立所有 AI 工具的 skills 連結：

```bash
# 專案內的 ai-apply/ 是「原始檔」
# 建立 symbolic links 讓各工具都能找到

ln -s "$(pwd)/ai-apply" .claude/skills/ai-apply
ln -s "$(pwd)/ai-apply" .cursor/skills/ai-apply
ln -s "$(pwd)/ai-apply" .gemini/skills/ai-apply
ln -s "$(pwd)/ai-apply" .opencode/skills/ai-apply
ln -s "$(pwd)/ai-apply" .agent/skills/ai-apply
```

#### 方式三：GitHub 開源發佈（讓別人也能用）

1. 把 `ai-apply/` 上傳到 GitHub Repository（如 `your-username/ai-apply-skill`）。
2. 在 README 中提供一鍵安裝腳本：

```bash
# 安裝到 Claude Code/Desktop
curl -sL https://raw.githubusercontent.com/your-username/ai-apply-skill/main/install.sh | bash
```

3. install.sh 內容：

```bash
#!/bin/bash
REPO="https://github.com/your-username/ai-apply-skill.git"
DEST="$HOME/.claude/skills/ai-apply"

echo "Installing ai-apply skill to $DEST..."
rm -rf "$DEST"
git clone --depth 1 "$REPO" "$DEST"
echo "Done. Restart Claude Code to use /ai-apply"
```

### 驗證安裝成功

在 Claude Code 中輸入：

```
/ai-apply
```

如果出現「GATE：強制對焦」的回應，代表安裝成功。

### 常見問題

**Q: 我放在專案根目錄的 `ai-apply/` 為什麼 Claude 讀不到？**
A: Claude Code 不會自動掃描專案中的任意資料夾作為 Skill。必須放在 `~/.claude/skills/` 或專案內的 `.claude/skills/`。

**Q: 一個 Skill 可以同時給多個 AI 工具用嗎？**
A: 可以。本 Skill 的結構是通用的 Markdown，只要工具支援讀取 Markdown 格式的 Skill，就能使用。只需複製或連結到對應路徑。

**Q: 更新 Skill 後需要重啟嗎？**
A: Claude Code 每次觸發 `/ai-apply` 時會重新讀取檔案，不需要重啟。但如果修改了檔案路徑或名稱，建議重啟確認。
