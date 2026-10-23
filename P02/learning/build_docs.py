"""Build the two local Markdown references into self-contained HTML documents.

Run with: python build_docs.py
Requires the Python-Markdown package only when source Markdown is changed.
The learning page itself uses the checked-in HTML output and needs no server.
"""

from pathlib import Path
from html import escape
import re

try:
    import markdown
except ImportError as exc:
    raise SystemExit(
        "缺少 Python-Markdown。请先运行 python -m pip install Markdown，再重新运行本脚本。"
    ) from exc


ROOT = Path(__file__).resolve().parent
DOCUMENTS = (
    {
        "source": ROOT.parent / "equation_source_table.md",
        "output": ROOT / "docs" / "equation_source_table.html",
        "title": "P02｜方程与单位来源表",
    },
    {
        "source": ROOT / "第一步_初学者讲义.md",
        "output": ROOT / "docs" / "first_step_handout.html",
        "title": "P02｜完整初学者讲义",
    },
)

DOCUMENT_CSS = """
:root { color-scheme: light; --paper: #f3f1e9; --ink: #183037; --muted: #536c70;
  --line: #c8d2cd; --accent: #087c74; --amber: #946719; }
* { box-sizing: border-box; }
html { background: var(--paper); }
body { margin: 0; background: var(--paper); color: var(--ink);
  font: 16px/1.72 "Segoe UI", "Microsoft YaHei", sans-serif; }
main { width: min(860px, calc(100% - 40px)); margin: 0 auto; padding: 36px 0 64px;
  overflow-wrap: anywhere; }
h1, h2, h3, h4 { color: #102a30; line-height: 1.35; }
h1 { margin: 0 0 24px; padding-bottom: 16px; border-bottom: 2px solid var(--accent);
  font-size: clamp(1.7rem, 4vw, 2.3rem); }
h2 { margin-top: 2.2em; padding-bottom: .35em; border-bottom: 1px solid var(--line);
  font-size: 1.45rem; }
h3 { margin-top: 1.7em; font-size: 1.15rem; }
p, li { max-width: 78ch; }
a { color: #076a65; text-underline-offset: 3px; }
strong { color: #243a35; }
blockquote { margin: 1.2em 0; padding: 12px 18px; border-left: 3px solid var(--amber);
  background: #e8e7dc; color: #3f5555; }
code { padding: .12em .35em; background: #e3e8e2; color: #18474a;
  font: .9em/1.5 ui-monospace, "Cascadia Code", Consolas, monospace; }
code sub, code sup { font: inherit; font-size: .72em; line-height: 0; }
code sub { vertical-align: sub; }
code sup { vertical-align: super; }
pre { overflow-x: auto; padding: 16px; background: #172e32; color: #e9f0e8; }
pre code { padding: 0; background: transparent; color: inherit; }
table { width: 100%; min-width: 680px; margin: 18px 0 26px; border-collapse: collapse;
  font-size: .92rem; }
th, td { padding: 10px 12px; border: 1px solid var(--line); text-align: left;
  vertical-align: top; }
th { background: #dfe8e1; color: #183e40; }
tr:nth-child(even) td { background: rgba(222, 230, 220, .48); }
hr { margin: 2em 0; border: 0; border-top: 1px solid var(--line); }
img { max-width: 100%; height: auto; }
@media (max-width: 600px) {
  main { width: min(100% - 28px, 860px); padding-top: 22px; }
  body { font-size: 15px; }
  th, td { padding: 8px; }
}
"""

MATH_IDENTIFIER = re.compile(
    r"(?<![A-Za-z])([A-Za-z\u0370-\u03FF]+)_([A-Za-z0-9]+(?:,[0-9]+)?)(?![A-Za-z])"
)
MATH_EXPONENT = re.compile(r"\^([0-9]+)")
CODE_IDENTIFIERS = {"v_thermal", "vth_mos"}
CODE_PATH = re.compile(r"^(?:\.{1,2}[/\\]|[A-Za-z]:[/\\]|/).+\.[A-Za-z0-9]{1,8}$")

PLAIN_MATH_SYMBOLS = {
    "Vthermal": ("V", "thermal"), "Vth": ("V", "th"), "Vbi": ("V", "bi"),
    "Wdep": ("W", "dep"), "NA": ("N", "A"), "ND": ("N", "D"), "ni": ("n", "i"),
    "Va": ("V", "a"), "Vdiode": ("V", "diode"), "Idiode": ("I", "diode"),
    "IS": ("I", "S"), "nd": ("n", "d"), "kB": ("k", "B"), "kBT": ("k", "B"),
    "xn": ("x", "n"), "xp": ("x", "p"), "Dn": ("D", "n"), "Dp": ("D", "p"),
    "Ln": ("L", "n"), "Lp": ("L", "p"), "Cox": ("C", "ox"), "εs": ("ε", "s"),
    "εox": ("ε", "ox"), "εr": ("ε", "r"), "ε0": ("ε", "0"), "tox": ("t", "ox"),
    "φF": ("φ", "F"), "VFB": ("V", "FB"), "VSB": ("V", "SB"), "VOV": ("V", "OV"),
    "VGS": ("V", "GS"), "VDS": ("V", "DS"), "ID": ("I", "D"), "μn": ("μ", "n"),
    "Wch": ("W", "ch"), "Lch": ("L", "ch"), "τn": ("τ", "n"), "τp": ("τ", "p"),
    "T0": ("T", "0"),
}
PLAIN_MATH_PATTERN = re.compile(
    r"(?<![A-Za-z])(" + "|".join(sorted(map(re.escape, PLAIN_MATH_SYMBOLS), key=len, reverse=True)) + r")(?![A-Za-z])"
)


def format_plain_math(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        base, subscript = PLAIN_MATH_SYMBOLS[match.group(1)]
        suffix = "T" if match.group(1) == "kBT" else ""
        return f"<i>{base}</i><sub>{subscript}</sub>{suffix}"

    segments = re.split(r"(```.*?```|~~~.*?~~~|`[^`\n]*`)", text, flags=re.DOTALL)
    return "".join(segment if segment.startswith(("`", "~~~")) else PLAIN_MATH_PATTERN.sub(replace, segment)
                   for segment in segments)


def format_code_math(html: str) -> str:
    def replace_code(match: re.Match[str]) -> str:
        original = match.group(1)
        if CODE_PATH.fullmatch(original.strip()):
            return f"<code>{original}</code>"
        content = re.sub(
            r"(?<![A-Za-z])ε_r,s(?![A-Za-z])",
            "<i>ε</i><sub>r,s</sub>",
            original,
        )

        def replace_identifier(identifier: re.Match[str]) -> str:
            token = identifier.group(0)
            if token in CODE_IDENTIFIERS:
                return token
            return f"<i>{identifier.group(1)}</i><sub>{identifier.group(2)}</sub>"

        content = MATH_IDENTIFIER.sub(replace_identifier, content)
        content = MATH_EXPONENT.sub(r"<sup>\1</sup>", content)
        return f"<code>{content}</code>"

    fenced = []

    def hold_fenced(match: re.Match[str]) -> str:
        fenced.append(match.group(0))
        return f"\x00FENCED{len(fenced) - 1}\x00"

    html = re.sub(r"<pre\b[^>]*>.*?</pre>", hold_fenced, html, flags=re.DOTALL)
    html = re.sub(r"<code>(.*?)</code>", replace_code, html, flags=re.DOTALL)
    for index, block in enumerate(fenced):
        html = html.replace(f"\x00FENCED{index}\x00", block)
    return html


def render_document(source: Path, title: str) -> str:
    text = format_plain_math(source.read_text(encoding="utf-8"))
    body = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "toc", "sane_lists"],
        output_format="html5",
    )
    body = format_code_math(body)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <style>{DOCUMENT_CSS}</style>
</head>
<body><main>{body}</main></body>
</html>
"""


def main() -> None:
    for document in DOCUMENTS:
        if not document["source"].is_file():
            raise SystemExit(f"找不到 Markdown 源文件：{document['source']}")
        document["output"].parent.mkdir(parents=True, exist_ok=True)
        document["output"].write_text(
            render_document(document["source"], document["title"]),
            encoding="utf-8",
        )
        print(f"已生成：{document['output']}")


if __name__ == "__main__":
    main()
