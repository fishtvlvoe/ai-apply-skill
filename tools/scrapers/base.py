import requests
from dataclasses import dataclass, field
from datetime import date
from typing import Optional


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; ai-apply-knowledge-bot/1.0; +https://github.com/fishtvlvoe/ai-apply-skill)',
    'Accept-Language': 'zh-TW,zh;q=0.9',
}


@dataclass
class PlatformUpdate:
    """一筆平台更新資料。name 是 competition-platforms.md 中 ### 標題的精確比對鍵。"""
    name: str                           # 對應 MD 中 `### <name>` 的完整標題
    url: str
    type: str                           # grant | competition | tender | award
    deadline_rules: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    fields: list[str] = field(default_factory=list)
    restrictions: list[str] = field(default_factory=list)
    how_to_get_guidelines: list[str] = field(default_factory=list)
    is_new: bool = False                # True = 不在 MD 中，需 append
    last_checked: str = field(default_factory=lambda: date.today().isoformat())


class BaseScraper:
    name: str = ""
    url: str = ""

    def fetch(self, url: str, timeout: int = 10) -> Optional[requests.Response]:
        import urllib3
        for verify in (True, False):
            try:
                if not verify:
                    # 部分政府網站憑證不完整（Missing SKI），本機開發時 fallback
                    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                resp = requests.get(url, headers=HEADERS, timeout=timeout, verify=verify)
                resp.raise_for_status()
                return resp
            except requests.exceptions.SSLError:
                if verify:
                    continue  # retry without verify
                print(f"[{self.__class__.__name__}] SSL failed even with verify=False: {url}")
                return None
            except Exception as e:
                print(f"[{self.__class__.__name__}] fetch failed: {e}")
                return None
        return None

    def scrape(self) -> list[PlatformUpdate]:
        raise NotImplementedError
