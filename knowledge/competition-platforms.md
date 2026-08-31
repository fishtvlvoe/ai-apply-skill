# 台灣競賽與補助平台知識庫

> **維護指南**：若要新增平台，請依照下方 `### 平台名稱` 格式附加新區段。
> 各欄位若資訊不確定請填「待調查」，勿留空白。
> Agent 會以平台名稱（大小寫不敏感、部分匹配）查詢對應條目。

---

## 如何使用

Agent 在調研階段，若用戶指定競賽/平台名稱，執行：
1. 以用戶指定名稱對 `### ` 標題進行部分匹配搜尋（大小寫不敏感）
2. 找到匹配條目 → 使用該平台的結構化資料
3. 未找到 → 告知用戶「不在預設平台知識庫中」，使用通用調研流程

---

### 獎金獵人 Bounty Hunter

url: https://bhuntr.com/
type: competition
fields:
  - 平台通用：姓名、Email、手機（所有競賽皆有）
  - 作品型：作品名稱、創作理念（通常 300 字以內）、作品檔案/連結
  - 企業型（依主辦設定）：公司名稱、統一編號
  - 著作權授權同意書勾選
  - ⚠️ 欄位依競賽性質不同，以各競賽頁面公告為準
deadline_rules:
  - 無統一截止日，每場競賽由主辦單位各自設定
  - 系統在截止日後自動關閉收件
  - 模式：可能為年度型（annual）或單次型（one-time）
how_to_get_guidelines:
  - 進入 https://bhuntr.com → 點選「比賽列表」
  - 選擇目標競賽專頁 → 查看「參賽資格」、「活動辦法」、「注意事項」分頁
  - 部分競賽提供可下載 PDF 簡章（在競賽頁面查找下載按鈕）
  - 使用 fetch-and-convert.py 抓取競賽頁面：`python tools/fetch-and-convert.py <競賽URL>`
restrictions:
  - 無平台層級統一限制，依各競賽主辦單位設定
  - 常見限制：學生身分、年齡（未滿 20 歲需法定代理人同意書）、地區、作品原創性聲明
  - 著作財產權歸屬條款依競賽差異大，需仔細閱讀
notes:
  - 平台為「競賽技術服務商」，主辦單位為各品牌/機關（非獎項主辦方）
  - 有報名費收款功能（刷卡/ATM/超商代繳）
  - 得獎金流涉及稅務申報，主辦方通常於注意事項說明
  - 平台 LINE 客服：@irv0112w

---

### 經濟部 SBIR 中小企業創新研發計畫

url: https://www.sbir.org.tw/
type: grant
fields:
  系統必填：
  - 公司名稱（需與商業司登記一致）
  - 統一編號
  - 負責人姓名
  - 核准設立日期
  - 登記地址
  - 實收資本額
  - 計畫書（Phase 1：PPT/ODP；Phase 2/2+：Word/ODT）
  應備上傳文件：
  - 損益及稅額計算表（或營業稅申報書）
  - 勞工保險投保單位被保險人名冊及投保人數證明
  - 納稅義務人違章欠稅查復表（國稅＋地方稅）
  - 個資同意書（相關人員皆須親簽）
  - 申請者自我檢查表
  - 研發聯盟合作協議書草案（如有聯盟申請）
deadline_rules:
  - 中央型 SBIR：rolling 隨到隨受理，無統一截止期限
  - 流程：線上送件 → 辦公室確認文件齊備 → email 通知「正式收件日」→ 進入審查
  - 地方型 SBIR（縣市政府）：各自訂期，需另查各縣市公告
how_to_get_guidelines:
  - 官網下載專區：https://www.sbir.org.tw/ → 下載「申請須知」與計畫書範本
  - 諮詢電話：0800-888-968（免費）
  - Email：sbir1@admail.csd.org.tw
restrictions:
  資格（符合任一即視為中小企業）：
  - 實收資本額 ≤ 新台幣 1 億元，或
  - 經常僱用員工數 < 200 人
  不得申請（任一）：
  - 有陸資投資
  - 申請日前 3 年內有欠繳應納稅捐（已補繳並取得無欠稅證明者除外）
  - 5 年內有執行政府計畫重大違約紀錄
  - 3 年內有停權處分且期間未屆滿
  - 同一計畫重複申請其他政府機關補助
  - 公司狀態為解散/撤銷/停業/歇業
notes:
  - 補助上限（115年起）：Phase 1 最高 150 萬元（6個月）、Phase 2 最高 1,200 萬元（1-2年）、Phase 2+ 最高 600 萬元
  - 政府補助不超過計畫總經費 50%，廠商需自籌 50% 以上
  - 使用工商憑證上傳可免蓋章
  - 本國設立及外國在台分公司不得申請

---

### 文化部補助（文化創意產業發展補助）

url: https://grants.moc.gov.tw/Web/
type: grant
fields:
  系統必填：
  - 申請人/單位基本資料
  - 統一編號（公司/商號/社團）或立案字號（演藝團體）
  - 個人申請：國民身分證字號
  - 計畫名稱、計畫目標與價值
  - 執行內容與時程
  - 受眾與推廣策略
  - 預算明細表（含自籌款金額）
  - 預期效益及風險評估
  應備上傳文件：
  - 申請單（線上填寫後列印簽章掃描上傳）
  - 立案證書/公司登記證明（法人/公司）或身分證正反面（個人）
  - 過往作品影音、合約、意向書等（視計畫性質）
deadline_rules:
  - 無統一截止日，各計畫獨立公告受理期間
  - 逾期系統自動關閉，無法受理
  - 部分計畫採分期徵件（季度型或年度型），待調查具體比例
how_to_get_guidelines:
  - 至 https://grants.moc.gov.tw/Web/ 註冊會員
  - 使用「獎補助案查詢」依類別篩選（文創及出版、視覺藝術、音樂等）
  - 點選目標計畫 → 下載「徵件須知」或「作業要點」
  - 部分計畫提供「懶人包」PDF
  - 使用 fetch-and-convert.py 抓取：`python tools/fetch-and-convert.py <計畫URL>`
restrictions:
  補助對象（擇一）：
  - 自然人：具中華民國國籍，部分計畫需年滿 20 歲
  - 法人/團體：依中華民國法律設立之公司行號、商號、工作室、社團法人、演藝團體等
  適用行業（依文化創意產業發展法第3條）：
    視覺藝術、音樂及表演藝術、文化資產、工藝、電影、廣播電視、出版、廣告、產品設計、視覺傳達設計、設計品牌時尚、建築設計、數位內容、創意生活、流行音樂及文化內容
  不得申請：
  - 同一計畫已獲文化部、所屬機關、國藝會等補助
  - 曾獲補助但尚未核銷結案
  - 政府機關、政黨、學校主辦計畫
notes:
  - 同時向多機關申請需在計畫書揭露所有經費來源
  - 部分計畫除線上申請外另需郵寄紙本公文（需詳閱各公告）
  - 系統送出後通常無法修改，務必確認後再送出
  - 延遲核銷或成果品質不良會影響未來申請資格
  - 不同司處（文化交流司、文創發展司等）的補助要點細節各異

---

### DIGITAL+ 數位服務創新補助計畫（數位產業署）

url: https://digiplus.adi.gov.tw/
type: grant
fields:
  - 計畫名稱
  - 申請企業統編
  - 公司設立日期
  - 計畫類別（前瞻技術開發/企業營運應用/終端消費應用/永續社會應用）
  - 計畫書（含技術說明、預算規劃）
  - 人事費、設備費、委外費等各科目預算明細
  - 公司財務報表（近一年）
  - 股東名冊（確認無陸資）
deadline_rules:
  - 每年度公告，通常 Q1 開放、Q2–Q3 截止
  - 114年度補助計畫已於 113 年底公告
  - 需至 digiplus.adi.gov.tw 系統線上申請，截止後不受理
how_to_get_guidelines:
  - 進入 https://digiplus.adi.gov.tw → 點選目標計畫（一般型補助/獎勵/主題型）
  - 下載「申請須知」PDF（含評審標準、預算格式）
  - 使用 fetch-and-convert.py：`python tools/fetch-and-convert.py https://digiplus.adi.gov.tw/`
restrictions:
  適用行業（限以下 3 碼行業代碼）：
  - J582：軟體出版業
  - J62：電腦程式設計、諮詢及相關服務業
  - J63：資訊服務業
  不得申請：
  - 陸資企業
  - 公司淨值（股東權益）為負值
  - 銀行拒絕往來戶
  - 同一計畫重複申請其他政府機關補助
notes:
  - 補助上限：一般型補助最高 500 萬元；主題型依公告另定
  - 補助比例：政府最高補助 50%，企業需自籌 50% 以上
  - 可申請科目：人事費、消耗材料、設備使用費、無形資產引進、委外研究驗證費、差旅費、創新推廣費
  - 每一企業每年只能申請 1 案
  - 系統申請後通常不可修改，送出前需仔細確認
  - ⚠️ 此網站為 SPA，自動抓取能力有限，建議定期人工確認截止日
  - last_auto_checked: 2026-08-31
---

### 經濟部 AI+ 產業計畫（製造業數位轉型）

url: https://eii.nat.gov.tw/moeai-plus/
type: grant
fields:
  - 公司名稱、統一編號
  - 工廠登記或商業登記文件
  - AI 診斷申請表
  - 導入計畫書（診斷後才進入此階段）
deadline_rules:
  - 滾動式受理，無固定截止日
  - 以梯次方式進行，額滿即截止
  - 建議盡早申請（預算用完即停止）
how_to_get_guidelines:
  - 進入 https://eii.nat.gov.tw/moeai-plus/ → 點選「立即申請」
  - 服務業入口：頁面有獨立「服務業申請」按鈕
  - 電話：0800-023-800 / Email：ai-office@itri.org.tw
  - 使用 fetch-and-convert.py：`python tools/fetch-and-convert.py https://eii.nat.gov.tw/moeai-plus/`
restrictions:
  - 主要適用：製造業（工廠登記）
  - 服務業另有專屬入口
  - 已申請其他政府 AI 補助者可能不得重複申請（需確認）
notes:
  - 三階段設計：診斷輔導（19萬+自籌1萬）→ AI應用導入（最高10萬設備+12萬人才）→ 研發轉型（個案最高500萬、聯盟最高4,000萬）
  - 由工研院（ITRI）執行，非直接向經濟部申請
  - 圖片中顯示每家企業個案最高可達 500 萬元
  - ⚡ 頁面顯示仍在受理申請（自動偵測）
  - last_auto_checked: 2026-08-31

---

### SIIR 服務業創新研發補助計畫（中小企業處）

url: https://sme.moeasmea.gov.tw/startup/modules/funding/detail/?sId=13
type: grant
fields:
  - 公司基本資料（名稱、統編、設立日期）
  - 創新研發計畫書
  - 財務報表
  - 研發團隊資料
deadline_rules:
  - 待調查（需至官網確認年度公告）
  - 通常年度上半年開放申請
how_to_get_guidelines:
  - 進入 https://sme.moeasmea.gov.tw → 搜尋「SIIR」
  - 或直接至 https://www.sbir.org.tw 查詢服務業版 SBIR
restrictions:
  - 服務業為主（對應 SBIR 的服務業版本）
  - 中小企業資格：資本額 ≤ 1 億元 或 員工數 < 200 人
notes:
  - 補助上限：Phase 1 最高 50 萬、Phase 2 最高 500 萬（待確認）
  - 與 SBIR（製造業）同源，申請邏輯相近
  - last_auto_checked: 2026-05-30

---

### 中小企業數位轉型補助（中小企業處）

url: https://www.sme.gov.tw/
type: grant
fields:
  - 公司基本資料
  - 數位轉型計畫書
  - 轉型目標說明
deadline_rules:
  - 114 年度補助計畫已開放（詳見官網公告）
  - 滾動受理，建議確認目前批次截止日
how_to_get_guidelines:
  - 進入 https://www.sme.gov.tw → 「補助貸款」→「數位轉型補助」
  - 或至 https://www.sme.gov.tw/drsme/ 查中小微企業多元振興平台
restrictions:
  - 中小企業資格（資本額 ≤ 1 億 或 員工 < 200 人）
  - 不得有陸資
notes:
  - 最高補助 10 萬元（一般數位轉型），大型方案另定
  - 可補助電商平台建置、數位行銷、雲端服務導入
  - last_auto_checked: 2026-05-30

---

## 標案類（政府採購）

> 適用情境：協助企業搜尋、評估、撰寫政府採購投標文件。與補助類不同——標案是「競標政府合約」，企業提供服務並收費，非申請補助金。

---

### Startup Terrace 台灣新創競技場

url: https://www.startupterrace.tw/
type: competition
fields:
  - 公司/團隊基本資料
  - 產品/服務說明
  - 商業模式與市場規模
  - 團隊介紹
deadline_rules:
  - 各活動獨立公告截止日，建議直接查 https://www.startupterrace.tw/ActivityList.aspx
  - 大型競賽（科技新創競賽、潛力新創選拔）通常每年 Q1–Q2 徵件
  - 海外拓銷團通常 Q2–Q3 招募
how_to_get_guidelines:
  - 活動列表：https://www.startupterrace.tw/ActivityList.aspx
  - 科技新創競賽（Hi-Tech）：可爭取 80 萬驗證金 + 一對一企業鏈結
  - 潛力新創選拔（Hi-Po Star）：年度旗艦選拔，每年 Q1–Q2 受理
  - 海外拓銷：Techsauce / Electronica India / Meet Greater South 等機會
restrictions:
  - 部分活動需具公司登記
  - 科技相關競賽通常要求已有 MVP 或產品原型
notes:
  - 政府支持的新創生態平台，結合競賽、加速、海外拓銷
  - ⚡ 近期活動：園區活動/園區服務
  - last_auto_checked: 2026-08-31

---

### 獎金獵人 Bounty Hunter 競賽列表

url: https://bhuntr.com/tw/competitions
type: competition
fields:
  - 依各競賽主辦方設定（詳見各競賽頁面）
deadline_rules:
  - 無統一截止日，每場競賽由主辦單位各自設定
  - 推薦分類：創業競賽、設計競賽、黑客松、AI 挑戰賽、QITC
how_to_get_guidelines:
  - 進入 https://bhuntr.com/tw/competitions → 依類別/關鍵字篩選
  - 高通台灣創新競賽（QITC）：https://bhuntr.com/tw/competitions/r7rvrt77t7ht66xxvh（入圍即 USD 10,000）
  - 黑客松類：https://bhuntr.com/tw/competitions?category=116,117,118
restrictions:
  - ⚠️ 網站為 React SPA，自動抓取能力有限，部分競賽資訊需人工查閱
notes:
  - 台灣最大競賽聚合平台，涵蓋民間品牌、政府機關、學術單位主辦的比賽
  - QITC 高通台灣創新競賽：每年 Q1 徵件，入圍即 USD 10,000，聚焦 AI PC / Edge AI
  - last_auto_checked: 2026-05-30

---

### 政府電子採購網（公共工程委員會）

url: https://web.pcc.gov.tw/
type: tender
fields:
  - 投標廠商基本資料
  - 資格審查文件（公司登記、財務報表、履約實績）
  - 技術規格說明書
  - 報價單（投標單）
  - 押標金（部分採購需繳）
deadline_rules:
  - 每個標案各自設定截止投標日時
  - 截止後系統鎖定，不受理補件
  - 通常公告至截止 10–30 天
how_to_get_guidelines:
  - 官網：https://web.pcc.gov.tw → 採購公告 → 關鍵字搜尋
  - g0v API（結構化 JSON）：https://pcc.g0v.ronny.tw/api/tender/
    - 範例：`GET /api/tender/?unit_id=<機關代碼>&year=114`
    - 新 API 端點（已遷移）：https://pcc-api.openfun.app/
  - 關鍵字建議：「AI」「數位轉型」「資訊服務」「系統建置」「軟體開發」
restrictions:
  - 需具採購金額對應資格（小額/未達查核/查核/巨額各有不同門檻）
  - 部分標案要求特定認證（ISO、CMMI、政府資安）
  - 不得有欠稅、停業、撤銷登記等紀錄
notes:
  - 機關代碼可至 https://web.pcc.gov.tw 查詢
  - 推薦相關 GitHub 資源：
    - pcc.g0v.ronny.tw — g0v 標案資料 API（結構化資料必備底層）
    - evergabe-tenders-scraper — 關鍵字自動監控 + 自動蒐集架構參考
    - Tender-Documents-AI-Agent — 標案文件 AI 解讀、提案協作
    - GitHub Topics: tender-intelligence / tender-evaluation
  - 整合建議：pcc API + 關鍵字監控 + AI 文件助理 = 完整標案小幫手
  - ⚡ API 查詢「AI」：找到 ? 筆近期標案
  - 關鍵字建議：AI、數位轉型、資訊服務、系統建置、軟體開發
  - 相關資源：pcc.g0v.ronny.tw（已遷至 pcc-api.openfun.app）
  - last_auto_checked: 2026-08-31
---

### 國科會計畫補助（國家科學及技術委員會）

url: https://www.nstc.gov.tw/
type: grant
fields:
  - 計畫主持人資料（學研界）
  - 研究計畫書
  - 合作企業資料（產學合作案）
  - 預算明細
deadline_rules:
  - 依計畫類型不同，通常 Q3–Q4 徵件（下一年度）
  - 前瞻計畫等特殊項目另行公告
how_to_get_guidelines:
  - https://www.nstc.gov.tw → 業務主題 → 補助 / 委辦 → 查詢各計畫公告
restrictions:
  - 學術單位主持為主
  - 企業可透過「產學合作」身份參與
notes:
  - 企業適用方向：產學合作計畫（出資部分，取得研發成果）
  - last_auto_checked: 2026-05-30

---

### 全台地方型 SBIR 縣市追蹤（115年度）

url: https://github.com/backtrue/sbir-grants/blob/main/sbir-grants/references/local_sbir_2026_tracker.md
type: grant
deadline_rules:
  - 各縣市各自公告，通常集中於 4–6 月
  - 台北市 SITI：全年隨到隨審（唯一全年受理）
  - 其他縣市：待各縣市官網公告後才開放收件
how_to_get_guidelines:
  - 即時縣市狀態：https://github.com/backtrue/sbir-grants（community 維護，MIT 授權）
  - 各縣市補助上限通常為個別 100 萬元、聯合申請 200 萬元
  - 台北市 SITI 最高 500 萬元（特例）
restrictions:
  - 各縣市自訂資格，通常需有工廠或商業登記在當地
  - 部分縣市有行業別限制（如嘉義縣優先無人機、新竹縣優先 AI/低碳）
notes:
  - 此條目由 GitHub Action 自動同步 backtrue/sbir-grants 追蹤表
  - 2026-02-21 狀態：已可申請 1 縣市（台北市）、籌備中 4 縣市、待公告 17 縣市
  - ⚡ 目前狀態：已可申請 1 縣市 / 籌備中 4 縣市 / 待公告 17 縣市
  - ⚡ 已可申請：台北市（SITI 隨到隨審）
  - last_auto_checked: 2026-08-31

---

### 中小及新創企業署（sme.gov.tw）

url: https://www.sme.gov.tw/
type: grant
fields:
  - 公司基本資料
  - 依各計畫另行規定
deadline_rules:
  - 各輔導計畫獨立公告，sme.gov.tw 為入口匯集頁
  - 建議設定頁面通知或定期回訪
how_to_get_guidelines:
  - 進入 https://www.sme.gov.tw → 8 大輔導主軸（數位轉型/淨零/研發/新創/融資/投資/通路/競賽）
  - 客服專線：0800-280-280（馬上辦中心）
  - 智能客服：sme.gov.tw 首頁右下角
restrictions:
  - 依各個計畫各自規定
notes:
  - 整合 SBIR、SIIR、數位轉型、青創貸款、女性創業等多個計畫的單一入口
  - 「獎項競賽」分類含各類表揚與競賽資訊
  - ⚡ 最新公告：2026-06-05APEC中小企業AI人才培力論壇 ／ 2026-05-29新創導師門診-《創業實驗室》親手調配出市場瘋搶的成功配方 ／ 2026-05-27管理顧問業個資宣導說明會
  - ⚡ 最新公告：2026-08-272026 G Camp 高雄場 ／ 2026-08-06中小企業網路大學校 AI應用工作坊：在大人機AI時代下必備的經營思維與實作練習 ／ 2026-07-07中小企業網路大學校 AI應用工作坊：AI 工具實作
  - ⚡ 最新公告：2026-08-272026 G Camp 高雄場 ／ 2026-08-06中小企業網路大學校 AI應用工作坊：在大人機AI時代下必備的經營思維與實作練習 ／ 2026-07-14管理顧問業資訊安全與個人資料保護宣導說明會
  - ⚡ 最新公告：2026-08-272026 G Camp 高雄場 ／ 2026-08-06中小企業網路大學校 AI應用工作坊：在大人機AI時代下必備的經營思維與實作練習 ／ 2026-07-21AI NEXT：新創企業創新應用論壇
  - ⚡ 最新公告：2026-08-272026 G Camp 高雄場 ／ 2026-08-06永續材質圖書館攜帶「行動圖書館模組」於臺灣文博會展出 ／ 2026-08-06中小企業網路大學校 AI應用工作坊：在大人機AI時代下必備的經營思維與實作練習
  - ⚡ 最新公告：2026-08-272026 G Camp 高雄場 ／ 2026-08-18綠色及永續金融知能系列講座 第四場-企業永續治理與金融實務 ／ 2026-08-06永續材質圖書館攜帶「行動圖書館模組」於臺灣文博會展出
  - ⚡ 最新公告：2026-08-29綠色及永續金融知能系列講座 第六場-永續發展基礎能力養成講座（下） ／ 2026-08-29綠色及永續金融知能系列講座 第五場-永續發展基礎能力養成講座（上） ／ 2026-08-27中小企業網路大學校【峰企業小聚｜《績效管理解方》解決實務常見問題】
  - ⚡ 最新公告：2026-09-09【精采臺灣 城鄉厚禮】OTOP 20週年  臺北車站展售會 ／ 2026-08-29綠色及永續金融知能系列講座 第六場-永續發展基礎能力養成講座（下） ／ 2026-08-29綠色及永續金融知能系列講座 第五場-永續發展基礎能力養成講座（上）
  - last_auto_checked: 2026-08-31

---

### 經濟部補助計畫入口網（buzu.moea.gov.tw）

url: https://buzu.moea.gov.tw/NewPortal/
type: grant
fields:
  - 依各計畫另行規定
deadline_rules:
  - 依各個補助計畫各自公告
how_to_get_guidelines:
  - 進入 https://buzu.moea.gov.tw/NewPortal/ → 依部別/類型搜尋
  - 涵蓋工業局、商業司、中小企業處等多個單位的補助計畫
restrictions:
  - 依各個計畫各自規定
notes:
  - ⚠️ 此網站外部連線不穩定，建議在台灣網路環境下使用
  - 為經濟部底下各司處補助的整合查詢入口
  - last_auto_checked: 2026-05-30

---

### G2B 企業服務整合網（smepass 企業得來速）

url: https://www.sme.gov.tw/smepass
type: grant
fields:
  - 公司統編（自動帶入相關資格篩選）
deadline_rules:
  - 依各個政府資源各自公告
how_to_get_guidelines:
  - 進入 sme.gov.tw → 搜尋「企業得來速」或 smepass
  - 可用統編自動匹配適合的政府資源、補助、輔導計畫
restrictions:
  - 需具工商登記
notes:
  - 跨部會政府資源單一入口，涵蓋多個部會的輔導計畫
  - 特色：輸入統編即可篩選「你適合申請的計畫」
  - last_auto_checked: 2026-05-30

---

## 工具資源（AI 輔助申請工具）

> 非補助平台本身，而是協助撰寫申請文件的 AI 工具。

---

### sbir-grants Skill（SBIR 計畫書撰寫工具）

url: https://github.com/backtrue/sbir-grants
type: tool
how_to_get_guidelines:
  - SaaS 版（免安裝）：https://sbir.thinkwithblack.com/
  - Claude Code Skill：clone repo → 按 INSTALLATION.md 安裝
  - MCP Server：按 CLAUDE_CODE_MCP_SETUP.md 設定（11 個 MCP 工具）
notes:
  - MIT 授權，社群維護（200+ stars）
  - 適用：SBIR Phase 1/2/2+ 計畫書深度撰寫、審查委員視角檢核、市場分析擴寫
  - 包含：22 縣市地方型 SBIR 追蹤、170K+ 字知識庫、6 維度品質雷達圖
  - 使用時機：ai-apply 找到 SBIR 機會後，深度撰寫計畫書改用此工具
  - last_auto_checked: 2026-05-30

---

## 擴充說明

### 新增平台格式

複製以下模板，填入新平台資料：

```markdown
### 平台名稱（中英文）

url: https://
type: competition | grant | award
fields:
  - 欄位1
  - 欄位2
deadline_rules:
  - 待調查
how_to_get_guidelines:
  - 待調查
restrictions:
  - 待調查
notes:
  - 待調查
```

### 常見待補充平台（建議未來擴充）

- **獎金獵人以外的民間競賽平台**：漩渦競賽 Swirl、臺灣青年競技大賽等
- **國發會補助**：https://www.ndc.gov.tw/
- **科技部（國科會）計畫補助**：https://www.nstc.gov.tw/
- **勞動部創業補助（微型創業鳳凰）**：待調查
