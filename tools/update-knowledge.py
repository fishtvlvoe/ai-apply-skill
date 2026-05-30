#!/usr/bin/env python3
"""
知識庫自動更新腳本
- 執行各爬蟲取得最新補助/標案資訊
- 更新 competition-platforms.md 中的 last_auto_checked 日期
- 動態偵測到的資訊（dates / amounts）若已存在就不重複插入
"""
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from scrapers.eii_moea import EIIMoeaScraper
from scrapers.sbir import SbirScraper
from scrapers.pcc_tender import PccTenderScraper
from scrapers.digiplus import DigiplusScraper
from scrapers.sbir_county_tracker import SbirCountyTrackerScraper
from scrapers.sme_portal import SmePortalScraper
from scrapers.base import PlatformUpdate

KNOWLEDGE_FILE = Path(__file__).parent.parent / 'knowledge' / 'competition-platforms.md'
TODAY = date.today().isoformat()

SCRAPERS = [
    EIIMoeaScraper(),
    SbirScraper(),
    PccTenderScraper(),
    DigiplusScraper(),
    SbirCountyTrackerScraper(),
    SmePortalScraper(),
]


def load_md() -> str:
    return KNOWLEDGE_FILE.read_text(encoding='utf-8')


def save_md(content: str):
    KNOWLEDGE_FILE.write_text(content, encoding='utf-8')


def platform_exists(content: str, name: str) -> bool:
    return f"### {name}" in content


def get_section(content: str, name: str) -> tuple[int, int]:
    """回傳該 section 的 start/end index（不含結尾 ---）。"""
    marker = f"### {name}"
    start = content.find(marker)
    if start == -1:
        return -1, -1
    # 找下一個 --- 分隔線
    end = content.find('\n---\n', start)
    if end == -1:
        end = len(content)
    return start, end


def update_entry(content: str, update: PlatformUpdate) -> str:
    """
    更新既有 section：
    1. 替換 last_auto_checked 日期（只改日期，不重複插入）
    2. 插入不重複的新 notes（僅限含「⚡」的動態偵測行）
    """
    start, end = get_section(content, update.name)
    if start == -1:
        return content

    section = content[start:end]

    # 替換 last_auto_checked（不重複插入）
    section = re.sub(
        r'(  - last_auto_checked:)\s*\S+',
        rf'\1 {TODAY}',
        section,
    )

    # 插入動態偵測 notes（只加「⚡」開頭的，且確認不重複）
    dynamic_notes = [n for n in update.notes if n.startswith('⚡')]
    for note in dynamic_notes:
        if note not in section:
            # 插在 last_auto_checked 前
            section = re.sub(
                r'(  - last_auto_checked:)',
                f'  - {note}\n\\1',
                section,
            )

    return content[:start] + section + content[end:]


def build_new_entry(update: PlatformUpdate) -> str:
    lines = [f"### {update.name}", "", f"url: {update.url}", f"type: {update.type}"]

    if update.fields:
        lines.append("fields:")
        lines.extend(f"  - {f}" for f in update.fields)

    if update.deadline_rules:
        lines.append("deadline_rules:")
        lines.extend(f"  - {r}" for r in update.deadline_rules)

    if update.how_to_get_guidelines:
        lines.append("how_to_get_guidelines:")
        lines.extend(f"  - {g}" for g in update.how_to_get_guidelines)

    if update.restrictions:
        lines.append("restrictions:")
        lines.extend(f"  - {r}" for r in update.restrictions)

    notes = list(update.notes) + [f"last_auto_checked: {TODAY}"]
    lines.append("notes:")
    lines.extend(f"  - {n}" for n in notes)

    return "\n".join(lines)


def append_new_platform(content: str, update: PlatformUpdate) -> str:
    """在 ## 擴充說明 之前插入新平台條目。"""
    entry = build_new_entry(update)
    insert_marker = "## 擴充說明"
    idx = content.find(insert_marker)
    if idx == -1:
        return content + "\n---\n\n" + entry + "\n"
    return content[:idx] + entry + "\n\n---\n\n" + content[idx:]


def main():
    content = load_md()
    changed = False

    for scraper in SCRAPERS:
        print(f"Running: {scraper.__class__.__name__}")
        try:
            updates = scraper.scrape()
        except Exception as e:
            print(f"  ERROR: {e}")
            continue

        for update in updates:
            if platform_exists(content, update.name):
                new_content = update_entry(content, update)
                if new_content != content:
                    content = new_content
                    changed = True
                    print(f"  ✓ Updated: {update.name}")
                else:
                    print(f"  — No change: {update.name}")
            else:
                content = append_new_platform(content, update)
                changed = True
                print(f"  + New entry: {update.name}")

    if changed:
        save_md(content)
        print(f"\nSaved to {KNOWLEDGE_FILE}")
    else:
        print("\nNo changes detected.")


if __name__ == '__main__':
    main()
