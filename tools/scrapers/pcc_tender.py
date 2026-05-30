"""
政府電子採購網標案爬蟲
目標：pcc-api.openfun.app（原 pcc.g0v.ronny.tw）
策略：查詢「AI」「數位轉型」「軟體開發」等關鍵字的近期標案，統計數量
"""
import requests
from .base import BaseScraper, PlatformUpdate

API_BASE = "https://pcc-api.openfun.app"
SEARCH_KEYWORDS = ["AI", "數位轉型", "軟體開發", "資訊服務", "系統建置"]


class PccTenderScraper(BaseScraper):
    name = "政府電子採購網（公共工程委員會）"
    url = "https://web.pcc.gov.tw/"

    def scrape(self) -> list[PlatformUpdate]:
        notes = []

        # 嘗試查詢 g0v pcc API
        for keyword in SEARCH_KEYWORDS[:2]:
            try:
                resp = requests.get(
                    f"{API_BASE}/api/tender/",
                    params={"keyword": keyword, "size": 1},
                    timeout=8,
                    headers={'Accept': 'application/json'},
                )
                if resp.status_code == 200:
                    data = resp.json()
                    total = data.get('total', data.get('count', '?'))
                    notes.append(f"⚡ API 查詢「{keyword}」：找到 {total} 筆近期標案")
                    break  # API 可用，測一個就夠
            except Exception as e:
                notes.append(f"API 查詢暫時失敗（{e}），建議改用 https://web.pcc.gov.tw 手動搜尋")
                break

        if not notes:
            notes.append("API 端點：https://pcc-api.openfun.app/api/tender/?keyword=AI")

        notes.append("關鍵字建議：AI、數位轉型、資訊服務、系統建置、軟體開發")
        notes.append("相關資源：pcc.g0v.ronny.tw（已遷至 pcc-api.openfun.app）")

        return [PlatformUpdate(
            name=self.name,
            url=self.url,
            type='tender',
            notes=notes,
        )]
