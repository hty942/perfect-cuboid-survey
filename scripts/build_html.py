#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render paper-zh.md / paper-en.md to standalone HTML (MathJax from CDN)."""

import re
import pathlib
import markdown

BASE = pathlib.Path(__file__).resolve().parent.parent

TEMPLATE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>
  :root{{--ink:#1c1c1c;--mut:#6d6d6d;--line:#ddd8cf;--bg:#faf8f4;--box:#f3efe6;--accent:#8a2020}}
  *{{box-sizing:border-box}}
  body{{margin:0;padding:56px 26px 120px;background:var(--bg);color:var(--ink);
    font-family:"Segoe UI","Microsoft YaHei","PingFang SC",system-ui,sans-serif;
    font-size:16px;line-height:1.9;-webkit-font-smoothing:antialiased}}
  main{{max-width:900px;margin:0 auto}}
  .langbar{{max-width:900px;margin:0 auto 22px;font-size:14px;color:var(--mut)}}
  .langbar a{{color:#1f4d7a;text-decoration:none;margin-right:14px}}
  h1{{font-size:30px;line-height:1.35;margin:0 0 18px;letter-spacing:-.3px}}
  h2{{font-size:21px;margin:54px 0 16px;padding-bottom:8px;border-bottom:2px solid var(--ink)}}
  h3{{font-size:17.5px;margin:32px 0 10px}}
  h4{{font-size:16px;margin:24px 0 8px;color:#333}}
  p{{margin:12px 0}}
  ul,ol{{margin:12px 0;padding-left:26px}}
  li{{margin:6px 0}}
  code{{background:#f2eee5;padding:1px 5px;border-radius:4px;
    font-family:Consolas,"Cascadia Mono",monospace;font-size:14.5px}}
  pre{{background:#f6f3ec;border:1px solid var(--line);border-radius:8px;
    padding:14px 18px;overflow-x:auto;font-family:Consolas,"Cascadia Mono",monospace;
    font-size:14.5px;line-height:1.7}}
  pre code{{background:none;padding:0}}
  table{{border-collapse:collapse;width:100%;margin:20px 0;font-size:15px;background:#fff}}
  th,td{{border:1px solid var(--line);padding:8px 12px;text-align:left;vertical-align:top}}
  th{{background:var(--box);font-weight:600}}
  blockquote{{margin:20px 0;padding:14px 20px;background:var(--box);
    border-left:4px solid var(--accent);border-radius:0 8px 8px 0;color:#333}}
  blockquote p:first-child{{margin-top:0}} blockquote p:last-child{{margin-bottom:0}}
  hr{{border:none;border-top:1px solid var(--line);margin:40px 0}}
  a{{color:#1f4d7a}}
</style>
<script>
MathJax = {{
  tex: {{inlineMath: [['$','$'], ['\\\\(','\\\\)']], displayMath: [['$$','$$'], ['\\\\[','\\\\]']]}},
  svg: {{fontCache: 'global'}}
}};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js" async></script>
</head>
<body>
<div class="langbar">{langbar}</div>
<main>
{body}
</main>
</body>
</html>
"""


def render(src_name, out_name, title, lang, langbar):
    text = (BASE / src_name).read_text(encoding="utf-8")

    # stash LaTeX so Markdown does not eat underscores / asterisks
    store = []

    def stash(m):
        store.append(m.group(0))
        return "MATHZZ%dZZ" % (len(store) - 1)

    text = re.sub(r"\$\$(.+?)\$\$", stash, text, flags=re.S)
    text = re.sub(r"(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)", stash, text, flags=re.S)

    body = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "sane_lists", "nl2br"],
    )

    def unstash(m):
        return store[int(m.group(1))]

    body = re.sub(r"MATHZZ(\d+)ZZ", unstash, body)

    html = TEMPLATE.format(title=title, lang=lang, langbar=langbar, body=body)
    (BASE / out_name).write_text(html, encoding="utf-8")
    print("wrote", out_name, len(html), "bytes")


render(
    "paper-zh.md", "paper-zh.html",
    "完美长方体：一个经计算验证的综述",
    "zh-CN",
    '<a href="paper-zh.html">中文</a><a href="paper-en.html">English</a>'
    '<a href="README.md">README</a>',
)
render(
    "paper-en.md", "paper-en.html",
    "Perfect Cuboids: A Computationally Verified Survey",
    "en",
    '<a href="paper-zh.html">中文</a><a href="paper-en.html">English</a>'
    '<a href="README.md">README</a>',
)
