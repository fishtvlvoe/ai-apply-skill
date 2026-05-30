"""
全台地方型 SBIR 縣市追蹤 scraper
資料來源：backtrue/sbir-grants（MIT 授權，社群維護）
策略：透過 GitHub API 抓取 local_sbir_2026_tracker.md，解析縣市狀態表
"""
import re
import requests
from .base import BaseScraper, PlatformUpdate

TRACKER_API = (
    "https://api.github.com/repos/backtrue/sbir-grants/contents/"
    "sbir-grants/references/local_sbir_2026_tracker.md"
)


class SbirCountyTrackerScraper(BaseScraper):
    name = "全台地方型 SBIR 縣市追蹤（115年度）"
    url = "https://github.com/backtrue/sbir-grants/blob/main/sbir-grants/references/local_sbir_2026_tracker.md"

    def scrape(self) -> list[PlatformUpdate]:
        try:
            resp = requests.get(
                TRACKER_API,
                headers={'Accept': 'application/vnd.github.v3+json'},
                timeout=10,
            )
            if resp.status_code != 200:
                return self._fallback()

            import base64
            content = base64.b64decode(resp.json()['content']).decode('utf-8')
            return self._parse(content)
        except Exception as e:
            print(f"  [SbirCountyTrackerScraper] error: {e}")
            return self._fallback()

    def _parse(self, content: str) -> list[PlatformUpdate]:
        notes = []

        # 抓 source_date（最後更新）
        date_match = re.search(r'source_date:\s*(\S+)', content)
        if date_match:
            notes.append(f"資料來源更新日：{date_match.group(1)}（backtrue/sbir-grants）")

        # 抓快速總覽
        open_match = re.search(r'已公告/可申請\s*\|\s*(\d+)', content)
        prep_match = re.search(r'籌備中.*?\|\s*(\d+)', content)
        pending_match = re.search(r'待公告\s*\|\s*(\d+)', content)

        summary_parts = []
        if open_match:
            summary_parts.append(f"已可申請 {open_match.group(1)} 縣市")
        if prep_match:
            summary_parts.append(f"籌備中 {prep_match.group(1)} 縣市")
        if pending_match:
            summary_parts.append(f"待公告 {pending_match.group(1)} 縣市")
        if summary_parts:
            notes.append(f"⚡ 目前狀態：{' / '.join(summary_parts)}")

        # 抓已可申請的縣市
        open_cities = re.findall(r'✅.*?運作中.*?\|.*?\|.*?\|.*?全年.*?\|.*?([台北新北桃園台中台南高雄基隆宜蘭花蓮台東苗栗彰化南投雲林嘉義新竹屏東澎湖連江金門]+)', content)
        already_open = re.search(r'已可申請.*?：([^\n]+)', content)
        if already_open:
            notes.append(f"⚡ 已可申請：{already_open.group(1).strip()}")

        # 抓六都中預計最快開放的
        coming_soon = re.findall(r'\| (台北市|新北市|台中市|台南市|高雄市|桃園市).*?預計\s*([\d/]+)', content)
        if coming_soon:
            soon_list = [f"{city} {date}" for city, date in coming_soon[:3]]
            notes.append(f"六都近期預計：{' / '.join(soon_list)}")

        deadline_rules = [
            "各縣市各自公告，通常集中於 4–6 月",
            "台北市 SITI：全年隨到隨審（唯一全年受理）",
            "其他縣市：待各縣市官網公告後才開放收件",
        ]

        how_to = [
            "詳細縣市狀態（即時）：https://github.com/backtrue/sbir-grants/blob/main/sbir-grants/references/local_sbir_2026_tracker.md",
            "各縣市補助上限通常為個別 100 萬元、聯合申請 200 萬元",
            "台北市 SITI 最高 500 萬元（特例）",
        ]

        return [PlatformUpdate(
            name=self.name,
            url=self.url,
            type='grant',
            deadline_rules=deadline_rules,
            how_to_get_guidelines=how_to,
            notes=notes,
        )]

    def _fallback(self) -> list[PlatformUpdate]:
        return [PlatformUpdate(
            name=self.name,
            url=self.url,
            type='grant',
            notes=[
                "GitHub API 暫時無法取得，建議直接查：https://github.com/backtrue/sbir-grants",
                "備用查詢：https://www.sbir.org.tw/",
            ],
        )]
