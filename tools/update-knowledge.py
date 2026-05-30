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
from scrapers.startup_terrace import StartupTerraceScraper
from scrapers.bhuntr import BhuntrScraper
from scrapers.base import PlatformUpdate

KNOWLEDGE_FILE = Path(__file__).parent.parent / 'knowledge' / 'competition-platforms.md'
UPCOMING_FILE = Path(__file__).parent.parent / 'knowledge' / 'UPCOMING.md'
TODAY = date.today().isoformat()

SCRAPERS = [
    EIIMoeaScraper(),
    SbirScraper(),
    PccTenderScraper(),
    DigiplusScraper(),
    SbirCountyTrackerScraper(),
    SmePortalScraper(),
    StartupTerraceScraper(),
    BhuntrScraper(),
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


def generate_upcoming(kb_content: str) -> str:
    """
    從 competition-platforms.md 產生 UPCOMING.md。
    策略：掃描各 entry 的 ⚡ notes + type，分類輸出。
    """
    lines = [
        f"# 當前可申請機會（更新：{TODAY}）",
        "",
        "> 由 GitHub Action 每週一自動更新。⚡ 為自動偵測，人工確認前請以官網為準。",
        "",
    ]

    # 解析所有 platform entries
    entries: list[dict] = []
    current: dict | None = None
    for line in kb_content.splitlines():
        if line.startswith("### "):
            if current:
                entries.append(current)
            current = {'name': line[4:].strip(), 'url': '', 'type': '', 'notes': [], 'deadline_rules': []}
        elif current:
            if line.startswith("url:"):
                current['url'] = line.split("url:", 1)[1].strip()
            elif line.startswith("type:"):
                current['type'] = line.split("type:", 1)[1].strip()
            elif line.strip().startswith("- ") and '⚡' in line:
                current['notes'].append(line.strip()[2:])
            elif line.strip().startswith("- ") and 'deadline_rules' not in line:
                txt = line.strip()[2:]
                if '隨到隨審' in txt or 'rolling' in txt.lower() or '隨到隨受' in txt:
                    current['deadline_rules'].append(txt)
    if current:
        entries.append(current)

    # 常態受理補助（rolling）
    rolling_grants = [e for e in entries if e['type'] == 'grant' and
                      any('隨到' in n or '常態' in n or '額滿' in n for n in e['deadline_rules'])]
    # 偵測到活躍的補助
    active_grants = [e for e in entries if e['type'] == 'grant' and e['notes']]
    # 競賽
    competitions = [e for e in entries if e['type'] == 'competition']
    # 標案
    tenders = [e for e in entries if e['type'] == 'tender']
    # 工具
    tools = [e for e in entries if e['type'] == 'tool']

    def fmt_entry(e: dict, show_notes: bool = True) -> str:
        url = e['url']
        note_str = ""
        if show_notes and e['notes']:
            note_str = " — " + e['notes'][0]
        return f"- **{e['name']}**{note_str} | [{url}]({url})"

    # 補助類
    lines += ["## 補助類", ""]
    lines += ["### 常態受理（可隨時申請）", ""]
    rolling_names = {"經濟部 SBIR 中小企業創新研發計畫", "全台地方型 SBIR 縣市追蹤（115年度）",
                     "經濟部 AI+ 產業計畫（製造業數位轉型）"}
    for e in entries:
        if e['name'] in rolling_names:
            lines.append(fmt_entry(e))
    lines += [""]

    lines += ["### 年度申請（確認截止日）", ""]
    annual_names = {"DIGITAL+ 數位服務創新補助計畫（數位產業署）", "SIIR 服務業創新研發補助計畫（中小企業處）",
                    "中小企業數位轉型補助（中小企業處）"}
    for e in entries:
        if e['name'] in annual_names:
            lines.append(fmt_entry(e, show_notes=False))
    lines += [""]

    lines += ["### ⚡ 自動偵測活躍狀態", ""]
    for e in active_grants:
        if e['name'] not in rolling_names | annual_names:
            lines.append(fmt_entry(e))
    lines += [""]

    # 競賽類
    lines += ["## 競賽類", ""]
    for e in competitions:
        lines.append(fmt_entry(e))
    lines += [""]

    # 標案類
    lines += ["## 標案類（政府採購）", ""]
    for e in tenders:
        lines.append(fmt_entry(e, show_notes=False))
    lines += [""]

    # 工具
    if tools:
        lines += ["## AI 輔助工具", ""]
        for e in tools:
            lines.append(fmt_entry(e, show_notes=False))
        lines += [""]

    lines += [
        "---",
        f"*自動產生於 {TODAY}，資料來源：knowledge/competition-platforms.md*",
    ]
    return "\n".join(lines) + "\n"


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
        print("\nNo changes to competition-platforms.md")

    # 每次都重新產生 UPCOMING.md（反映最新 ⚡ 資料）
    upcoming = generate_upcoming(content)
    old_upcoming = UPCOMING_FILE.read_text(encoding='utf-8') if UPCOMING_FILE.exists() else ""
    if upcoming != old_upcoming:
        UPCOMING_FILE.write_text(upcoming, encoding='utf-8')
        print(f"Updated UPCOMING.md")
    else:
        print("No changes to UPCOMING.md")


if __name__ == '__main__':
    main()
