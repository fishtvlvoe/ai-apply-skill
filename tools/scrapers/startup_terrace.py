"""
Startup Terrace（startupterrace.tw）scraper
目標：抓取當前活動/競賽列表
"""
import re
from datetime import date
from bs4 import BeautifulSoup
from .base import BaseScraper, PlatformUpdate

ACTIVITY_URL = "https://www.startupterrace.tw/ActivityList.aspx"


class StartupTerraceScraper(BaseScraper):
    name = "Startup Terrace 台灣新創競技場"
    url = "https://www.startupterrace.tw/"

    def scrape(self) -> list[PlatformUpdate]:
        resp = self.fetch(ACTIVITY_URL)
        notes = []

        if resp:
            soup = BeautifulSoup(resp.text, 'lxml')

            # 抓活動標題
            titles = []
            for tag in soup.select('h2, h3, .activity-title, .event-title, td a, .list-item a'):
                t = tag.get_text(strip=True)
                if t and len(t) > 5 and '活動' not in t[:3]:
                    titles.append(t)

            titles = list(dict.fromkeys(titles))[:5]  # 去重，取前 5
            if titles:
                notes.append(f"⚡ 近期活動：{' ／ '.join(titles[:3])}")

            # 偵測截止日期
            text = soup.get_text()
            year = date.today().year
            dates = re.findall(rf'{year}[年/]\s*(\d{{1,2}})[月/](\d{{1,2}})', text)
            if dates:
                formatted = [f"{year}/{m}/{d}" for m, d in dates[:3]]
                notes.append(f"頁面日期：{', '.join(formatted)}")

            # 偵測獎金
            prizes = re.findall(r'(\d+)\s*萬', text)
            if prizes:
                notes.append(f"頁面獎金關鍵字：{', '.join(set(prizes[:3]))} 萬")

        return [PlatformUpdate(
            name=self.name,
            url=self.url,
            type='competition',
            deadline_rules=[
                "各活動獨立公告截止日，建議直接查 https://www.startupterrace.tw/ActivityList.aspx",
                "大型競賽（如科技新創競賽、潛力新創選拔）通常每年 Q1–Q2 徵件",
            ],
            how_to_get_guidelines=[
                "進入 https://www.startupterrace.tw/ActivityList.aspx 查看所有活動",
                "科技新創競賽（Hi-Tech）：可爭取 80 萬驗證金 + 一對一企業鏈結",
                "潛力新創選拔（Hi-Po Star）：年度旗艦選拔，每年 Q1–Q2 受理",
            ],
            restrictions=[
                "部分活動需具公司登記",
                "科技相關競賽通常要求已有 MVP 或產品原型",
            ],
            notes=notes or ["startupterrace.tw 今次抓取無新動態"],
        )]
