# 自動化填表指南（Phase 3）

## 三層填表策略

不同 AI 環境的 Computer Use 能力不同，採用分層 fallback 策略：

```
┌──────────────────────────────────────────────────────────────┐
│ Level 1: Native Computer Use                                 │
│ 條件：Claude Code (Anthropic) / Claude Desktop (beta)        │
│ 方式：直接操作瀏覽器，點擊輸入框、上傳檔案、提交表單          │
│ 優點：最自動化，幾乎無需人工介入                              │
│ 限制：僅特定平台支援；複雜驗證碼可能失敗                      │
├──────────────────────────────────────────────────────────────┤
│ Level 2: Browser Automation Scripts                          │
│ 條件：任何可執行 Python/Node.js 的環境                        │
│ 方式：生成 Playwright / Puppeteer / Selenium 腳本             │
│ 優點：跨平台通用；可重複執行；可處理複雜邏輯                  │
│ 限制：需安裝瀏覽器驅動；動態網頁可能需調整 selector           │
├──────────────────────────────────────────────────────────────┤
│ Level 3: Semi-Auto Helper (Copy-Paste)                       │
│ 條件：所有環境皆適用                                          │
│ 方式：AI 生成填表內容 → 人工複製貼上                          │
│ 優點：零技術門檻；100% 相容                                  │
│ 限制：仍需人工操作；無法自動上傳檔案                          │
└──────────────────────────────────────────────────────────────┘
```

## Level 1: Claude Computer Use

**適用環境**：Claude Code (CLI)、Claude Desktop (beta)、Anthropic API with computer-use。

**操作指令範例**：

```
打開瀏覽器，前往 <報名網站 URL>。
根據以下資訊填寫表單：
- 公司名稱：創新科技有限公司
- 統一編號：12345678
- ...（其他欄位）

遇到需要上傳檔案的欄位時，暫停並通知我。
```

**注意事項**：
- Computer Use 可能無法處理圖形驗證碼（CAPTCHA）或兩階段驗證（2FA）。
- 涉及敏感個資的欄位，建議人工確認後再提交。

## Level 2: Browser Automation Scripts

**生成 Playwright 腳本範本**：

```python
# auto_fill_form.py
# 使用前：pip install playwright && playwright install

from playwright.sync_api import sync_playwright

FORM_DATA = {
    "company_name": "創新科技有限公司",
    "tax_id": "12345678",
    "product_name": "創新雲端服務",
    "website": "https://example-startup.com",
    # ... 其他欄位
}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("<報名網站 URL>")

    page.fill('input[name="company_name"]', FORM_DATA["company_name"])
    page.fill('input[name="tax_id"]', FORM_DATA["tax_id"])
    # ... 其他欄位

    # page.click('button[type="submit"]')  # 人工確認後再取消註解
    print("表單已填寫，請確認後手動提交。")
    browser.close()
```

**執行方式**：
1. AI 根據報名網站生成對應的填表腳本。
2. 使用者在本地執行腳本（需安裝 Python + Playwright）。
3. 腳本自動填寫非敏感欄位，敏感欄位留空或標記待人工處理。

## Level 3: Semi-Auto Helper

**適用情境**：無法使用 Computer Use，也無法執行腳本時。

**操作流程**：

1. AI 讀取線上表單的欄位名稱（透過網頁內容或使用者貼上的欄位清單）。
2. AI 根據 TEMPLATES.md 中的「報名表單預填模板」生成對應內容。
3. 輸出填寫對照表，使用者逐欄複製貼上，敏感欄位自行處理。
