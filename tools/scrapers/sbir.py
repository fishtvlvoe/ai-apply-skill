"""
SBIR 中小企業創新研發計畫爬蟲
目標：sbir.org.tw
策略：抓取首頁公告，偵測截止日期、補助金額變動
"""
import re
from bs4 import BeautifulSoup
from .base import BaseScraper, PlatformUpdate


class SbirScraper(BaseScraper):
    name = "經濟部 SBIR 中小企業創新研發計畫"
    url = "https://www.sbir.org.tw/"

    def scrape(self) -> list[PlatformUpdate]:
        resp = self.fetch(self.url)
        if not resp:
            return []

        soup = BeautifulSoup(resp.text, 'lxml')
        notes = []

        # 抓最新公告標題（前 3 則）
        announcements = soup.select('.news-list li, .announce li, article h3')[:3]
        if announcements:
            titles = [a.get_text(strip=True) for a in announcements]
            notes.append(f"最新公告：{' / '.join(titles[:3])}")

        # 偵測補助金額
        text = soup.get_text()
        if '150萬' in text or '1,200萬' in text:
            notes.append("✓ 115年度補助上限：Phase 1 最高 150 萬、Phase 2 最高 1,200 萬（確認中）")

        # 偵測滾動受理或截止日
        dates = re.findall(r'(\d{3})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日', text)
        if dates:
            formatted = [f"{y}年{m}月{d}日" for y, m, d in dates[:3]]
            notes.append(f"頁面日期資訊：{', '.join(formatted)}")

        deadline_rules = ["中央型：rolling 隨到隨審，無統一截止日"]

        return [PlatformUpdate(
            name=self.name,
            url=self.url,
            type='grant',
            deadline_rules=deadline_rules,
            notes=notes,
        )]
