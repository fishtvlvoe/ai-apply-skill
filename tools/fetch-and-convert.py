#!/usr/bin/env python3
"""
fetch-and-convert.py — 抓取網頁 / PDF 並轉換為 Markdown

使用方式：
  python tools/fetch-and-convert.py <URL>
  python tools/fetch-and-convert.py <URL> --output /tmp/output.md

依賴（優先使用，不可用時自動 fallback）：
  pip install requests html2text

PDF 支援（選用）：
  pip install pdfminer.six
"""

from __future__ import annotations

import argparse
import re
import sys
from html import unescape
from html.parser import HTMLParser
from typing import Optional


# ---------------------------------------------------------------------------
# 內建 Markdown 轉換器（stdlib-only fallback）
# ---------------------------------------------------------------------------

class SimpleMarkdownConverter(HTMLParser):
    """小型 stdlib fallback：HTML → Markdown，無需外部依賴。"""

    BLOCK_TAGS = {
        "article", "body", "div", "footer", "form",
        "header", "main", "nav", "p", "section",
        "table", "tbody", "thead", "tr",
    }
    SKIP_TAGS = {"script", "style", "noscript"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip_depth = 0
        self.link_stack: list[Optional[str]] = []
        self.pre_depth = 0
        self.list_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        tag = tag.lower()
        attrs_dict = {name.lower(): value for name, value in attrs}

        if tag in self.SKIP_TAGS:
            self.skip_depth += 1
            return
        if self.skip_depth:
            return

        if tag in self.BLOCK_TAGS:
            self._newline(2 if tag in {"p", "section", "article", "body", "main"} else 1)
        elif tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            level = int(tag[1])
            self._newline(2)
            self.parts.append("#" * level + " ")
        elif tag == "br":
            self._newline(1)
        elif tag == "li":
            self._newline(1)
            self.parts.append("  " * max(0, self.list_depth - 1) + "- ")
        elif tag in {"ul", "ol"}:
            self.list_depth += 1
            self._newline(1)
        elif tag == "a":
            self.link_stack.append(attrs_dict.get("href"))
            self.parts.append("[")
        elif tag in {"strong", "b"}:
            self.parts.append("**")
        elif tag in {"em", "i"}:
            self.parts.append("*")
        elif tag == "code" and not self.pre_depth:
            self.parts.append("`")
        elif tag == "pre":
            self.pre_depth += 1
            self._newline(2)
            self.parts.append("```text\n")
        elif tag in {"td", "th"}:
            self.parts.append(" | ")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in self.SKIP_TAGS:
            self.skip_depth = max(0, self.skip_depth - 1)
            return
        if self.skip_depth:
            return

        if tag == "a":
            href = self.link_stack.pop() if self.link_stack else None
            self.parts.append("]")
            if href:
                self.parts.append(f"({href})")
        elif tag in {"strong", "b"}:
            self.parts.append("**")
        elif tag in {"em", "i"}:
            self.parts.append("*")
        elif tag == "code" and not self.pre_depth:
            self.parts.append("`")
        elif tag == "pre":
            self.parts.append("\n```")
            self.pre_depth = max(0, self.pre_depth - 1)
            self._newline(2)
        elif tag in {"ul", "ol"}:
            self.list_depth = max(0, self.list_depth - 1)
            self._newline(1)
        elif tag in self.BLOCK_TAGS or tag in {"h1", "h2", "h3", "h4", "h5", "h6", "li"}:
            self._newline(1)

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        if self.pre_depth:
            self.parts.append(data)
            return
        text = re.sub(r"\s+", " ", unescape(data))
        if text.strip():
            self.parts.append(text)

    def markdown(self) -> str:
        text = "".join(self.parts)
        text = re.sub(r"[ \t]+\n", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r" +", " ", text)
        text = re.sub(r"\n +", "\n", text)
        return text.strip() + "\n"

    def _newline(self, count: int) -> None:
        current = "".join(self.parts[-3:])
        existing = len(current) - len(current.rstrip("\n"))
        needed = max(0, count - existing)
        if needed:
            self.parts.append("\n" * needed)


# ---------------------------------------------------------------------------
# HTML → Markdown 轉換（優先 html2text，fallback 到 SimpleMarkdownConverter）
# ---------------------------------------------------------------------------

def html_to_markdown(html: str) -> str:
    """將 HTML 字串轉換為 Markdown。優先使用 html2text，不可用時 fallback。"""
    try:
        import html2text  # type: ignore
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.body_width = 0  # 不強制換行
        return h.handle(html)
    except ImportError:
        # fallback: 內建 SimpleMarkdownConverter
        converter = SimpleMarkdownConverter()
        converter.feed(html)
        return converter.markdown()


# ---------------------------------------------------------------------------
# PDF 文字擷取
# ---------------------------------------------------------------------------

def pdf_bytes_to_markdown(content: bytes) -> str:
    """嘗試從 PDF bytes 擷取文字並以 Markdown 回傳。"""
    try:
        from pdfminer.high_level import extract_text_to_fp  # type: ignore
        from pdfminer.layout import LAParams  # type: ignore
        import io

        output = io.StringIO()
        input_stream = io.BytesIO(content)
        extract_text_to_fp(input_stream, output, laparams=LAParams(), output_type="text", codec="utf-8")
        text = output.getvalue().strip()
        if not text:
            raise ValueError("PDF extracted empty text")
        return text + "\n"
    except ImportError:
        print(
            "⚠️  警告：未安裝 pdfminer.six，無法擷取 PDF 文字。\n"
            "   安裝方式：pip install pdfminer.six",
            file=sys.stderr,
        )
        raise
    except Exception as exc:
        print(f"⚠️  警告：PDF 文字擷取失敗：{exc}", file=sys.stderr)
        raise


# ---------------------------------------------------------------------------
# 網路請求
# ---------------------------------------------------------------------------

def fetch_url(url: str) -> tuple[str, bytes]:
    """
    抓取 URL，回傳 (content_type, body_bytes)。
    網路錯誤時 print 到 stderr 並以 SystemExit(1) 終止。
    """
    try:
        import requests  # type: ignore
        resp = requests.get(url, timeout=30, headers={"User-Agent": "ai-apply-fetch/1.0"})
        resp.raise_for_status()
        content_type = resp.headers.get("Content-Type", "")
        return content_type, resp.content
    except ImportError:
        # requests 不可用時，fallback 到 urllib
        import urllib.request
        import urllib.error

        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ai-apply-fetch/1.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                content_type = resp.headers.get("Content-Type", "")
                return content_type, resp.read()
        except urllib.error.HTTPError as exc:
            print(f"HTTP 錯誤 {exc.code}：{url}", file=sys.stderr)
            sys.exit(1)
        except Exception as exc:
            print(f"網路錯誤：{exc}", file=sys.stderr)
            sys.exit(1)
    except Exception as exc:
        print(f"請求失敗：{exc}", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def convert(url: str) -> str:
    """
    抓取 URL 並轉換為 Markdown 字串。
    - HTML → html_to_markdown（優先 html2text，fallback SimpleMarkdownConverter）
    - PDF  → pdf_bytes_to_markdown（需要 pdfminer.six）
    其他 Content-Type 時，嘗試以 UTF-8 解碼並回傳純文字。
    """
    content_type, body = fetch_url(url)

    if "application/pdf" in content_type or url.lower().endswith(".pdf"):
        try:
            return pdf_bytes_to_markdown(body)
        except Exception:
            print("⚠️  PDF 擷取失敗，無法輸出內容。", file=sys.stderr)
            sys.exit(1)
    else:
        # 嘗試以 HTML 處理
        try:
            html = body.decode("utf-8", errors="replace")
        except Exception as exc:
            print(f"解碼失敗：{exc}", file=sys.stderr)
            sys.exit(1)
        return html_to_markdown(html)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="抓取網頁或 PDF，轉換為 Markdown。",
        epilog="範例：python tools/fetch-and-convert.py https://example.com --output /tmp/out.md",
    )
    parser.add_argument("url", help="要抓取的 URL")
    parser.add_argument(
        "--output", "-o",
        metavar="PATH",
        help="輸出路徑（預設：stdout）",
    )
    args = parser.parse_args()

    markdown = convert(args.url)

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(markdown)
            print(f"✓ 已寫入：{args.output}", file=sys.stderr)
        except OSError as exc:
            print(f"寫入失敗：{exc}", file=sys.stderr)
            sys.exit(1)
    else:
        sys.stdout.write(markdown)


if __name__ == "__main__":
    main()
