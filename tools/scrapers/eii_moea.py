"""
經濟部 AI+ 產業計畫爬蟲
目標：eii.nat.gov.tw/moeai-plus/
策略：抓取頁面確認補助計畫仍在受理，提取最新金額/聯絡資訊
"""
import re
from bs4 import BeautifulSoup
from .base import BaseScraper, PlatformUpdate


class EIIMoeaScraper(BaseScraper):
    name = "經濟部 AI+ 產業計畫（製造業數位轉型）"
    url = "https://eii.nat.gov.tw/moeai-plus/"

    def scrape(self) -> list[PlatformUpdate]:
        resp = self.fetch(self.url)
        if not resp:
            return []

        soup = BeautifulSoup(resp.text, 'lxml')
        notes = [
            "三階段：診斷輔導 → AI應用導入 → 研發轉型",
            "執行單位：工研院（ITRI）",
        ]

        # 嘗試從頁面提取最新補助金額關鍵數字
        text = soup.get_text()
        amounts = re.findall(r'[\d,]+\s*萬元', text)
        if amounts:
            notes.append(f"頁面顯示金額關鍵字：{', '.join(set(amounts[:5]))}")

        # 確認受理狀態
        if '申請' in text or '立即' in text:
            notes.append("⚡ 頁面顯示仍在受理申請（自動偵測）")

        return [PlatformUpdate(
            name=self.name,
            url=self.url,
            type='grant',
            notes=notes,
        )]
