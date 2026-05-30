"""
獎金獵人（bhuntr.com）scraper
注意：bhuntr.com 為 React SPA，requests 只能抓 HTML 骨架
策略：嘗試抓靜態 meta / og 資訊，偵測頁面活躍狀態
"""
import re
from bs4 import BeautifulSoup
from .base import BaseScraper, PlatformUpdate

BHUNTR_API_HINT = "https://bhuntr.com/tw/competitions"


class BhuntrScraper(BaseScraper):
    name = "獎金獵人 Bounty Hunter"
    url = "https://bhuntr.com/"

    def scrape(self) -> list[PlatformUpdate]:
        resp = self.fetch(BHUNTR_API_HINT)
        notes = []

        if resp:
            soup = BeautifulSoup(resp.text, 'lxml')
            text = soup.get_text()

            # SPA 通常在骨架裡還是有部分資料
            # 嘗試抓 og:description / meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'}) or \
                        soup.find('meta', attrs={'property': 'og:description'})
            if meta_desc:
                desc = meta_desc.get('content', '')
                if desc:
                    notes.append(f"頁面描述：{desc[:80]}")

            # 嘗試偵測比賽關鍵字
            competitions = re.findall(r'[「「」』]([^「「」』]{5,30})[」」]', text)
            if competitions:
                notes.append(f"⚡ 偵測到活動關鍵字：{' ／ '.join(competitions[:3])}")
            else:
                notes.append("⚠️ bhuntr.com 為 React SPA，自動抓取能力有限。詳細比賽列表請直接查詢網站。")
                notes.append("⚡ 建議搜尋類別：創業競賽、設計競賽、黑客松、AI 挑戰賽")

        return [PlatformUpdate(
            name=self.name,
            url=self.url,
            type='competition',
            notes=notes or ["⚠️ bhuntr.com 今次抓取無內容"],
        )]
