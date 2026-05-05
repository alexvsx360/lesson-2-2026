"""Sync landing-related <pre><code> blocks in index.html with exact slices from landing-page/."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def esc_html_markup(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def lines_slice(lines: list[str], start: int, end: int) -> str:
    """1-based inclusive line numbers."""
    return "".join(lines[start - 1 : end])


def css_slice(css_text: str, start: int, end: int) -> str:
    ls = css_text.splitlines(True)
    return "".join(ls[start - 1 : end]).rstrip("\n")


def replace_pre_inner(regex: re.Pattern[str], html: str, index_to_inner: dict[int, str]) -> str:
    matches = list(regex.finditer(html))
    parts: list[str] = []
    last = 0
    for i, m in enumerate(matches):
        parts.append(html[last : m.start()])
        inner = index_to_inner.get(i)
        if inner is not None:
            parts.append(m.group(1) + inner + m.group(3))
        else:
            parts.append(m.group(0))
        last = m.end()
    parts.append(html[last:])
    return "".join(parts)


def main() -> None:
    idx_lines = (ROOT / "landing-page/index.html").read_text(encoding="utf-8").splitlines(True)
    css_text = (ROOT / "landing-page/css/style.css").read_text(encoding="utf-8")
    js_text = (ROOT / "landing-page/js/script.js").read_text(encoding="utf-8")

    MK = {
        "skel": esc_html_markup(lines_slice(idx_lines, 9, 23)),
        "header": esc_html_markup(lines_slice(idx_lines, 11, 21)),
        "hero_partial": esc_html_markup(lines_slice(idx_lines, 24, 37)),
        "hero_img": esc_html_markup(lines_slice(idx_lines, 39, 45)),
        "hero_full": esc_html_markup(lines_slice(idx_lines, 24, 46)),
        "benefits": esc_html_markup(lines_slice(idx_lines, 48, 58)),
        "process": esc_html_markup(lines_slice(idx_lines, 60, 67)),
        "footer": esc_html_markup(lines_slice(idx_lines, 99, 102)),
        "signup": esc_html_markup(lines_slice(idx_lines, 69, 96)),
        "label_email": esc_html_markup(lines_slice(idx_lines, 85, 92)),
        "in_full": esc_html_markup(lines_slice(idx_lines, 77, 83)),
        "in_mail": esc_html_markup(lines_slice(idx_lines, 86, 92)),
        "a_signup": esc_html_markup(lines_slice(idx_lines, 34, 34)),
    }

    CSS = {
        "base": css_slice(css_text, 1, 17),
        "header_nav": css_slice(css_text, 19, 50),
        "hero": css_slice(css_text, 52, 101),
        "hero_img": css_slice(css_text, 103, 110),
        "benefits": css_slice(css_text, 112, 133),
        "process": css_slice(css_text, 135, 146),
        "footer": css_slice(css_text, 148, 160),
        "signup": css_slice(css_text, 162, 211),
    }

    pre_markup = re.compile(
        r'(<pre><code class="language-markup">)(.*?)(</code></pre>)',
        re.DOTALL,
    )
    pre_css = re.compile(
        r'(<pre><code class="language-css">)(.*?)(</code></pre>)',
        re.DOTALL,
    )
    pre_js = re.compile(
        r'(<pre><code class="language-javascript">)(.*?)(</code></pre>)',
        re.DOTALL,
    )

    path = ROOT / "index.html"
    raw = path.read_text(encoding="utf-8")

    markup_map = {
        3: MK["skel"],
        4: MK["header"],
        5: MK["a_signup"],
        6: MK["hero_partial"],
        7: MK["hero_img"],
        8: MK["hero_full"],
        9: MK["benefits"],
        10: MK["process"],
        11: MK["footer"],
        12: MK["signup"],
        13: MK["label_email"],
        14: MK["in_full"],
        15: MK["in_mail"],
        16: MK["signup"],
    }

    css_map = {i: CSS[k] for i, k in enumerate([
        "base",
        "header_nav",
        "hero",
        "hero_img",
        "benefits",
        "process",
        "footer",
        "signup",
    ])}

    out = replace_pre_inner(pre_markup, raw, markup_map)
    out = replace_pre_inner(pre_css, out, css_map)
    out = replace_pre_inner(pre_js, out, {0: js_text.rstrip("\n")})

    n_m = len(pre_markup.findall(out))
    n_c = len(pre_css.findall(out))
    n_j = len(pre_js.findall(out))
    assert n_m == len(pre_markup.findall(raw))
    assert n_c == len(pre_css.findall(raw))
    assert n_j == len(pre_js.findall(raw))

    path.write_text(out, encoding="utf-8")
    print(f"Synced index.html: {n_m} markup, {n_c} css, {n_j} js pre blocks")


if __name__ == "__main__":
    main()
