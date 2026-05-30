"""
DIGITAL+ 數位服務創新補助計畫爬蟲
目標：digiplus.adi.gov.tw（數位產業署）
注意：為 SPA（React），requests 僅能抓 HTML 骨架，無法取得動態資料
策略：抓取頁面判斷是否仍在受理，偵測截止日期關鍵字
"""
import re
from bs4 import BeautifulSoup
from .base import BaseScraper, PlatformUpdate


class DigiplusScraper(BaseScraper):
    name = "DIGITAL+ 數位服務創新補助計畫（數位產業署）"
    url = "https://digiplus.adi.gov.tw/"

    def scrape(self) -> list[PlatformUpdate]:
        resp = self.fetch(self.url)
        notes = ["⚠️ 此網站為 SPA，自動抓取能力有限，建議定期人工確認截止日"]

        if resp:
            soup = BeautifulSoup(resp.text, 'lxml')
            text = soup.get_text()

            # 偵測截止日或受理狀態
            dates = re.findall(r'(\d{3,4})[/年](\d{1,2})[/月](\d{1,2})', text)
            if dates:
                formatted = [f"{y}/{m}/{d}" for y, m, d in dates[:3]]
                notes.append(f"頁面偵測到日期：{', '.join(formatted)}")

            if '受理' in text or '申請' in text:
                notes.append("⚡ 頁面含「受理/申請」關鍵字，計畫可能仍在進行")

            amounts = re.findall(r'[\d,]+\s*萬元', text)
            if amounts:
                notes.append(f"補助金額相關：{', '.join(set(amounts[:3]))}")

        return [PlatformUpdate(
            name=self.name,
            url=self.url,
            type='grant',
            notes=notes,
        )]
