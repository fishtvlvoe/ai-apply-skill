---
name: ai-apply
description: "Automate competition & grant application workflows. Trigger: '報名比賽'、'申請補助'、'參賽'、'填表單'."
disable-model-invocation: true
user-invocable: true
---

# AI-APPLY

**目標**：將 1–2 天的人工查閱與整理，壓縮至 2 小時內完成查閱、整理、歸納、自動填表。

> **⚠️ 用戶資料責任聲明**：本 Skill 不內建任何個人或公司資料。所有真實資料（公司名稱、統編、聯絡資訊等）須由用戶透過 `user-profile.yaml` 自行提供。Skill 本身僅包含虛擬示範資料，不會代入任何真實個資。

---

## 前置步驟：載入用戶資料

**每次觸發 `/ai-apply` 時，必須先執行此步驟，才能進入 GATE。**

1. **嘗試讀取** `~/.claude/skills/ai-apply/user-profile.yaml`
2. **若檔案不存在**：
   ```
   ⚠️ 找不到 user-profile.yaml。

   請先建立您的用戶資料檔：
     cp ~/.claude/skills/ai-apply/user-profile.yaml.example ~/.claude/skills/ai-apply/user-profile.yaml

   然後編輯 user-profile.yaml，填入您的真實公司與聯絡資訊。
   完成後重新執行 /ai-apply。
   ```
   **停止執行，等待用戶建立檔案。**

3. **若檔案存在**，載入資料並檢查必填欄位：
   - 若 `company.name` 為空 → 警告：「⚠️ user-profile.yaml 缺少 company.name，填表時將使用空白值」
   - 若 `contact.primary_email` 為空 → 警告：「⚠️ user-profile.yaml 缺少 contact.primary_email，填表時將使用空白值」
   - 列出所有空白欄位並提示用戶補充（非阻斷，可繼續）

4. **資料載入成功後**，在後續步驟中：
   - 以 `user-profile.yaml` 中的值替換模板 `{{token}}` 佔位符
   - 替換規則：`{{company.name}}` → `company.name` 的值，以此類推
   - 若 token 對應值為空，保留 token 原樣並在輸出中標注 ⚠️

---

## GATE：強制對焦（不可跳過）

1. 一句話複述「我理解你要報名 / 申請 ___」。
2. 判斷模式：
   - **新建**：從零開始報名新比賽
   - **轉換**：把過去的參賽資料改寫成新比賽版本
   - **升級**：優化現有申請文件
3. 問「方向對嗎？」→ 用戶說 OK 才往下。

---

## 流程

### 步驟 1：調研與競品分析

**1a-0. 當前機會速覽**（GATE 通過後，步驟 1a 前執行）

Read `knowledge/UPCOMING.md`。

- 若用戶未指定特定平台：列出「常態受理」與「⚡ 自動偵測活躍」項目，問「你對哪個方向有興趣？」
- 若用戶已指定平台：跳過，直接進 1a。

**1a. 平台知識庫查詢**（在執行 research-guide.md 前先做）

Read `knowledge/competition-platforms.md`，對用戶指定的競賽/平台名稱執行部分匹配（大小寫不敏感）：

- **匹配成功**：使用該平台條目的 `fields`、`deadline_rules`、`how_to_get_guidelines`、`restrictions` 等結構化資料，帶入後續調研與填表流程。告知用戶：「✓ 找到預設平台資料：<平台名稱>，已載入相關欄位規範。」
- **未匹配**：告知用戶：「<競賽名稱>不在預設平台知識庫中，將使用通用調研流程搜尋報名資訊。」然後繼續執行通用調研流程。

**1b. 通用調研流程**

Read `knowledge/research-guide.md` 執行查閱與分析。

產出：競賽資訊表 + 競品比較矩陣 + 參賽方向建議書。

> **強制停止點：參賽方向建議書產出後，必須等用戶確認才繼續。**


### 步驟 2：資料撰寫與 MVP 設計

Read `knowledge/content-writing.md` 執行內容產出。

產出：作品說明書 / 提案書 + Demo 簡報腳本 + 加分佐證文件清單。

> **強制停止點：作品說明書大綱確認後，才展開全文撰寫。**

### 步驟 3：自動化填表

Read `knowledge/form-filling.md` 依環境選擇填表策略。

| 環境 | 策略 | 自動化程度 | 說明 |
|------|------|------------|------|
| Claude Code / Anthropic API | Level 1: Computer Use | 最高 | 直接控制瀏覽器填表、截圖驗證 |
| Codex CLI (OpenAI) | Level 2: Bash + Python 腳本 | 中高 | 批次執行 Playwright 腳本；Claude Code 派任 → Codex 執行 |
| Kimi MCP (`mcp__kimi-code__*`) | Level 2: 文件分析 + 草稿生成 | 中高 | 大 context 讀規則書 → 生成申請文件草稿；不直接填表 |
| 有 Python/Node.js | Level 2: Playwright/Puppeteer 腳本 | 中高 | 生成腳本後由用戶執行 |
| Kimi Code (VS Code 插件) | Level 3: 半自動輔助（生成→人工貼上） | 中 | 編輯器側生成文件，需人工複製貼上 |
| 其他 AI Agent | Level 3: 半自動輔助（生成→人工貼上） | 中 | 生成填表內容，用戶手動操作 |
| Kimi CLI | ❌ 已停用（2026-05-24） | — | 改用 Kimi MCP 替代 |

---

## 品質檢查（結構完整性 — 分析類）

- [ ] 所有必填區塊已完成（競賽資訊表、競品比較、提案大綱）
- [ ] 數據有來源引用（市場規模、統計數字附出處）
- [ ] 結論有依據支撐（差異化論述對應競品矩陣）
- [ ] 建議可操作（有具體下一步：文件清單 + 時程 + 填表策略）

---

## 完成條件（全部達到才算完成）

- [ ] user-profile.yaml 已載入且必填欄位非空
- [ ] GATE 已通過
- [ ] 參賽方向已確認（步驟 1 停止點）
- [ ] 作品說明書大綱已確認（步驟 2 停止點）
- [ ] 品質檢查已通過
- [ ] 用戶已確認最終產出

