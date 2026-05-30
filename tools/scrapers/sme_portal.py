"""
中小及新創企業署（sme.gov.tw）scraper
目標：抓取最新輔導計畫、補助公告、競賽資訊
"""
import re
from bs4 import BeautifulSoup
from .base import BaseScraper, PlatformUpdate

SME_URLS = {
    'main': 'https://www.sme.gov.tw/',
    'subsidy': 'https://www.sme.gov.tw/page-tw-2794',
    'competition': 'https://www.sme.gov.tw/page-tw-2792',
}


class SmePortalScraper(BaseScraper):
    name = "中小及新創企業署（sme.gov.tw）"
    url = "https://www.sme.gov.tw/"

    def scrape(self) -> list[PlatformUpdate]:
        notes = []

        resp = self.fetch(self.url)
        if resp:
            soup = BeautifulSoup(resp.text, 'lxml')

            # 抓最新公告標題（前 5 則）
            # 試不同選擇器（不同版本的政府網站結構各異）
            items = (
                soup.select('.news-item a, .announce-item a, .list-item a, article h3 a')
                or soup.select('a[href*="news"], a[href*="article"]')
            )
            if items:
                titles = [i.get_text(strip=True) for i in items if i.get_text(strip=True)][:5]
                if titles:
                    notes.append(f"⚡ 最新公告：{' ／ '.join(titles[:3])}")

            # 偵測關鍵字
            text = soup.get_text()
            keywords = ['SBIR', 'SIIR', '數位轉型', '創業', '徵件', '補助']
            found = [k for k in keywords if k in text]
            if found:
                notes.append(f"頁面含關鍵字：{', '.join(found)}")

        return [PlatformUpdate(
            name=self.name,
            url=self.url,
            type='grant',
            notes=notes or ["sme.gov.tw 今次抓取無新動態"],
        )]
