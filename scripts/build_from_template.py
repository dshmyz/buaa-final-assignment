#!/usr/bin/env python3
"""Build a BUAA course paper DOCX from an existing template.

Input JSON shape:
{
  "title": "论文题目",
  "cover": ["课程名称：...", "姓名：XXX（学号：……）", "学院：...", "专业：...", "时间：..."],
  "abstract": "摘要正文，不含 摘  要：",
  "keywords": "关键词1；关键词2；关键词3",
  "sections": [
    {"title": "引言", "paragraphs": ["..."]},
    {"title": "一、...", "paragraphs": ["..."]}
  ],
  "references": ["[1] ...", "[2] ..."],
  "ai_disclosure": "本文写作过程中..."
}
"""

from __future__ import annotations

import argparse
import json
import re
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.etree import ElementTree as ET

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
ET.register_namespace("w", W)

# 字号标准：单位半磅
SIZE_SAN = 24    # 小四
SIZE_THREE = 32  # 三号


def q(tag: str) -> str:
    return f"{{{W}}}{tag}"


def text_of(p: ET.Element) -> str:
    return "".join(t.text or "" for t in p.iter(q("t")))


def clear_children(e: ET.Element) -> None:
    for c in list(e):
        e.remove(c)


def remove_colors(rpr: ET.Element) -> None:
    for color in list(rpr.findall(q("color"))):
        rpr.remove(color)


def set_bold(rpr: ET.Element, bold: bool | None) -> None:
    if bold is None:
        return
    for btag in (q("b"), q("bCs")):
        for old in list(rpr.findall(btag)):
            rpr.remove(old)
        b = ET.Element(btag)
        if not bold:
            b.set(q("val"), "0")
        rpr.append(b)


def set_ascii_font(rpr: ET.Element, font: str | None) -> None:
    if not font:
        return
    rf = rpr.find(q("rFonts"))
    if rf is None:
        rf = ET.Element(q("rFonts"))
        rpr.insert(0, rf)
    rf.set(q("ascii"), font)
    rf.set(q("hAnsi"), font)


def set_eastasia_font(rpr: ET.Element, font: str | None) -> None:
    if not font:
        return
    rf = rpr.find(q("rFonts"))
    if rf is None:
        rf = ET.Element(q("rFonts"))
        rpr.insert(0, rf)
    rf.set(q("eastAsia"), font)


def set_font_size(rpr: ET.Element, size_halfpt: int | None) -> None:
    if size_halfpt is None:
        return
    for stag in (q("sz"), q("szCs")):
        for old in list(rpr.findall(stag)):
            rpr.remove(old)
        s = ET.Element(stag)
        s.set(q("val"), str(size_halfpt))
        rpr.append(s)


def make_text_para(
    template_p: ET.Element,
    text: str,
    *,
    style_id: str | None = None,
    bold: bool | None = None,
    ascii_font: str | None = None,
    eastasia_font: str | None = None,
    size_halfpt: int | None = None,
) -> ET.Element:
    """基于模板段落生成新段落，保留 pPr 中的样式和段落格式，只在 run 级别覆盖字体/颜色/字号"""
    p = deepcopy(template_p)
    ppr = p.find(q("pPr"))

    # 清空所有现有的 runs，但保留 pPr
    for r in list(p.findall(q("r"))):
        p.remove(r)

    # 如果指定了新样式，替换 pStyle
    if style_id is not None and ppr is not None:
        old_style = ppr.find(q("pStyle"))
        if old_style is not None:
            ppr.remove(old_style)
        pstyle = ET.Element(q("pStyle"))
        pstyle.set(q("val"), style_id)
        ppr.insert(0, pstyle)

    # 清理 pPr 中的 rPr 颜色
    if ppr is not None:
        for rpr in ppr.iter(q("rPr")):
            remove_colors(rpr)
            if size_halfpt is not None:
                set_font_size(rpr, size_halfpt)

    # 新建 run
    r = ET.Element(q("r"))

    # 优先用模板里第一个 run 的 rPr
    first = template_p.find(q("r"))
    if first is not None and first.find(q("rPr")) is not None:
        rpr = deepcopy(first.find(q("rPr")))
    elif ppr is not None and ppr.find(q("rPr")) is not None:
        rpr = deepcopy(ppr.find(q("rPr")))
    else:
        rpr = ET.Element(q("rPr"))

    remove_colors(rpr)
    if bold is not None:
        set_bold(rpr, bold)
    if ascii_font is not None:
        set_ascii_font(rpr, ascii_font)
    if eastasia_font is not None:
        set_eastasia_font(rpr, eastasia_font)
    if size_halfpt is not None:
        set_font_size(rpr, size_halfpt)
    r.append(rpr)

    t = ET.Element(q("t"))
    if text[:1].isspace() or text[-1:].isspace():
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    t.text = text
    r.append(t)
    p.append(r)
    return p


def make_multirun_para(
    template_p: ET.Element,
    parts: list[tuple[str, bool]],
    *,
    style_id: str | None = None,
    ascii_font: str | None = None,
    eastasia_font: str | None = None,
    size_halfpt: int | None = None,
) -> ET.Element:
    p = make_text_para(template_p, "", style_id=style_id, eastasia_font=eastasia_font, size_halfpt=size_halfpt)
    for r in list(p.findall(q("r"))):
        p.remove(r)
    first = template_p.find(q("r"))
    base_rpr = deepcopy(first.find(q("rPr"))) if first is not None and first.find(q("rPr")) is not None else ET.Element(q("rPr"))
    remove_colors(base_rpr)
    if ascii_font is not None:
        set_ascii_font(base_rpr, ascii_font)
    if eastasia_font is not None:
        set_eastasia_font(base_rpr, eastasia_font)
    if size_halfpt is not None:
        set_font_size(base_rpr, size_halfpt)
    for text, bold in parts:
        r = ET.Element(q("r"))
        rpr = deepcopy(base_rpr)
        set_bold(rpr, bold)
        r.append(rpr)
        t = ET.Element(q("t"))
        if text[:1].isspace() or text[-1:].isspace():
            t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        t.text = text
        r.append(t)
        p.append(r)
    return p


def make_page_break(template_p: ET.Element) -> ET.Element:
    p = make_text_para(template_p, "")
    for r in list(p.findall(q("r"))):
        p.remove(r)
    r = ET.Element(q("r"))
    br = ET.Element(q("br"))
    br.set(q("type"), "page")
    r.append(br)
    p.append(r)
    return p


def find_template_paragraphs(paras: list[ET.Element], body: ET.Element) -> dict[str, ET.Element]:
    by_text = [(i, text_of(p), p) for i, p in enumerate(paras)]

    def find_contains(*needles: str) -> ET.Element | None:
        for _, text, p in by_text:
            if all(n in text for n in needles):
                return p
        return None

    # 找正文段落模板（引言后的第一个正文段落，带有正确缩进）
    body_template = paras[14] if len(paras) > 14 else paras[0]

    # 找各个功能段落的原型
    title_template = find_contains("题目（宋体") or find_contains("题目") or body_template
    abstract_template = find_contains("摘  要：") or body_template
    keyword_template = find_contains("关键词：") or abstract_template

    # 找标题段落：style=2（一级标题）且 line=240，无首行缩进
    heading_template = None
    for p in paras:
        ppr = p.find(q("pPr"))
        if ppr is not None:
            pstyle = ppr.find(q("pStyle"))
            spacing = ppr.find(q("spacing"))
            if pstyle is not None and pstyle.get(q("val")) == "2":
                if spacing is not None and spacing.get(q("line")) == "240":
                    heading_template = p
                    break

    if heading_template is None:
        heading_template = body_template

    refs_template = find_contains("参考文献") or heading_template

    # 找表格（封面信息表格）
    cover_table = None
    for p in body:
        if p.tag.endswith("}tbl"):
            cover_table = p
            break

    # 找 Logo 和最后一个 section break（作为文档末尾）
    logo = None
    logo_idx = -1
    for i, p in enumerate(paras):
        if any(e.tag.endswith("}drawing") for e in p.iter()):
            logo = p
            logo_idx = i
            break

    final_sect = None
    for p in reversed(paras):
        ppr = p.find(q("pPr"))
        if ppr is not None and ppr.find(q("sectPr")) is not None:
            final_sect = deepcopy(ppr.find(q("sectPr")))
            break

    return {
        "title": title_template,
        "abstract": abstract_template,
        "keywords": keyword_template,
        "heading": heading_template,
        "body": body_template,
        "refs": refs_template,
        "logo": logo,
        "logo_idx": logo_idx,
        "cover_table": cover_table,
        "final_sect": final_sect,
    }


def clean_formulaic(text: str) -> str:
    replacements = {
        "众所周知，": "",
        "不可否认，": "",
        "值得注意的是，": "",
        "总而言之，": "",
        "综上所述，": "",
        "显而易见，": "",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r"首先，?", "", text)
    text = re.sub(r"其次，?", "", text)
    text = re.sub(r"再次，?", "", text)
    text = re.sub(r"最后，?", "", text)
    return text


def build(template: Path, content_path: Path, output: Path) -> None:
    data = json.loads(content_path.read_text(encoding="utf-8"))

    print('🔍 正在读取和分析模板...')
    with ZipFile(template) as zin:
        root = ET.fromstring(zin.read("word/document.xml"))
        body = root.find(q("body"))
        if body is None:
            raise RuntimeError("template has no word/body")
        original_paras = body.findall(q("p"))
        t = find_template_paragraphs(original_paras, body)
        print(f'✅ 模板样式分析完成，共 {len(original_paras)} 个段落')

        print('📝 正在提取章节和样式...')
        final_sect = None
        for p in reversed(original_paras):
            ppr = p.find(q("pPr"))
            if ppr is not None and ppr.find(q("sectPr")) is not None:
                final_sect = deepcopy(ppr.find(q("sectPr")))
                break

        print('📄 正在生成文档结构...')
        new_elements: list[ET.Element] = []

        # Logo
        if t["logo"] is not None:
            new_elements.append(deepcopy(t["logo"]))
            print('✅ 已保留封面 Logo')

        title = data["title"]

        # 封面表格（替换里面的占位符）
        if t["cover_table"] is not None:
            tbl = deepcopy(t["cover_table"])
            rows = tbl.findall(q("tr"))
            cover = data.get("cover", [])
            today = datetime.now().strftime("%Y年%m月%d日")

            def replace_cell_text(cell, new_text, eastasia_font=None, ascii_font=None, size_halfpt=None):
                """替换单元格中的文本：删除所有旧 runs，创建新的 run"""
                paras_in_cell = cell.findall(q("p"))
                if paras_in_cell:
                    para = paras_in_cell[0]
                    # 删除所有旧 runs
                    for r_elem in para.findall(q("r")):
                        para.remove(r_elem)
                    # 创建新的 run
                    r_new = ET.Element(q("r"))
                    rpr = ET.Element(q("rPr"))
                    # 添加字体
                    rf = ET.Element(q("rFonts"))
                    if eastasia_font:
                        rf.set(q("eastAsia"), eastasia_font)
                    else:
                        rf.set(q("eastAsia"), "宋体")
                    if ascii_font:
                        rf.set(q("ascii"), ascii_font)
                        rf.set(q("hAnsi"), ascii_font)
                    rpr.append(rf)
                    # 添加字号
                    if size_halfpt:
                        sz = ET.Element(q("sz"))
                        sz.set(q("val"), str(size_halfpt))
                        rpr.append(sz)
                        szCs = ET.Element(q("szCs"))
                        szCs.set(q("val"), str(size_halfpt))
                        rpr.append(szCs)
                    r_new.append(rpr)
                    t_elem = ET.Element(q("t"))
                    t_elem.text = new_text
                    r_new.append(t_elem)
                    para.append(r_new)

            # Row 1: 论文题目（第1个单元格）→ 黑体二号（44半磅）
            if len(rows) > 1:
                cell = rows[1].find(q("tc"))
                replace_cell_text(cell, title, eastasia_font="黑体", size_halfpt=44)

            # Row 3: 课程名称 → cover[0]（宋体四号，数字字母用新罗马）
            if len(rows) > 3 and len(cover) > 0:
                cell = rows[3].findall(q("tc"))[1]
                replace_cell_text(cell, cover[0].replace("课程名称：", ""), eastasia_font="宋体", ascii_font="Times New Roman", size_halfpt=28)

            # Row 4: 姓名+学号 → cover[1] + cover[2]（宋体四号，数字字母用新罗马）
            if len(rows) > 4 and len(cover) > 2:
                cell = rows[4].findall(q("tc"))[1]
                name_part = cover[1].replace("姓名：", "").replace("姓    名：", "")
                id_part = cover[2].replace("学号：", "").replace("学    号：", "")
                replace_cell_text(cell, f"{name_part}（学号：{id_part}）", eastasia_font="宋体", ascii_font="Times New Roman", size_halfpt=28)

            # Row 5: 学院 → cover[3]（宋体四号，数字字母用新罗马）
            if len(rows) > 5 and len(cover) > 3:
                cell = rows[5].findall(q("tc"))[1]
                replace_cell_text(cell, cover[3].replace("学院：", "").replace("院    别：", ""), eastasia_font="宋体", ascii_font="Times New Roman", size_halfpt=28)

            # Row 6: 时间（当前日期）（宋体四号，数字字母用新罗马）
            if len(rows) > 6:
                cell = rows[6].findall(q("tc"))[1]
                replace_cell_text(cell, today, eastasia_font="宋体", ascii_font="Times New Roman", size_halfpt=28)

            new_elements.append(tbl)
            print('✅ 已填入封面信息到表格')

        new_elements.append(make_page_break(t["body"]))

        # 正文标题（宋体三号加粗）
        new_elements.append(make_text_para(t["title"], title, eastasia_font="宋体", bold=True))

        # 摘要、关键词
        new_elements.append(make_multirun_para(t["abstract"], [("摘  要：", True), (clean_formulaic(data["abstract"]), False)], eastasia_font="宋体", ascii_font="Times New Roman"))
        new_elements.append(make_multirun_para(t["keywords"], [("关键词：", True), (data["keywords"], False)], eastasia_font="宋体", ascii_font="Times New Roman"))
        print('✅ 已生成摘要和关键词')

        # 正文章节
        for section in data.get("sections", []):
            new_elements.append(make_text_para(t["heading"], section["title"], eastasia_font="黑体"))
            for para in section.get("paragraphs", []):
                new_elements.append(make_text_para(t["body"], clean_formulaic(para), eastasia_font="宋体", ascii_font="Times New Roman"))
        print(f'✅ 已生成 {len(data.get("sections", []))} 个章节')

        # 参考文献
        new_elements.append(make_text_para(t["heading"], "参考文献", eastasia_font="黑体"))
        for ref in data.get("references", []):
            new_elements.append(make_text_para(t["body"], ref, eastasia_font="宋体", ascii_font="Times New Roman"))
        print(f'✅ 已写入 {len(data.get("references", []))} 条参考文献')

        # AI 披露（如果有）
        if data.get("ai_disclosure"):
            new_elements.append(make_text_para(t["heading"], "人工智能使用披露", eastasia_font="黑体"))
            new_elements.append(make_text_para(t["body"], data["ai_disclosure"], eastasia_font="宋体", ascii_font="Times New Roman"))
            print('✅ 已写入 AI 使用披露')

        # 保留最后的 sectionPr
        if final_sect is not None and new_elements:
            ppr = new_elements[-1].find(q("pPr"))
            if ppr is None:
                ppr = ET.Element(q("pPr"))
                new_elements[-1].insert(0, ppr)
            for sp in list(ppr.findall(q("sectPr"))):
                ppr.remove(sp)
            ppr.append(final_sect)

        clear_children(body)
        for p in new_elements:
            body.append(p)

        print('💾 正在写入 DOCX 文件...')
        xml = ET.tostring(root, encoding="utf-8", xml_declaration=True)
        with ZipFile(output, "w", ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                payload = zin.read(item.filename)
                if item.filename == "word/document.xml":
                    payload = xml
                zout.writestr(item, payload)

    print('🔍 正在进行最终自检...')
    validate(output)


def validate(path: Path) -> None:
    with ZipFile(path) as z:
        root = ET.fromstring(z.read("word/document.xml"))
        text = "".join(t.text or "" for t in root.iter(q("t")))
        media = [n for n in z.namelist() if n.startswith("word/media/")]

    # 提取实际使用的样式
    paras = root.findall(f'{q("body")}/{q("p")}')
    styles_used = set()
    for p in paras:
        ppr = p.find(q("pPr"))
        pstyle = ppr.find(q("pStyle")) if ppr is not None else None
        if pstyle is not None:
            styles_used.add(pstyle.get(q("val")))

    chinese_chars = sum(1 for ch in text if '一' <= ch <= '鿿')
    has_drawing = any(e.tag.endswith('}drawing') for e in root.iter())
    has_ai_disclosure = "人工智能使用披露" in text
    has_template_leftover = any(x in text for x in ["请删除此文本框", "题目（宋体", "正文（宋体", "考核方式与基本要求"])
    has_today_date = datetime.now().strftime("%Y年%m月%d日") in text

    print()
    print("=" * 50)
    print("✅ 最终自检报告")
    print("=" * 50)
    print(f'📄 输出文件：{path.name}')
    print(f'📝 总字符数：{len(text)}')
    print(f'🀄️ 中文字符数：{chinese_chars}')
    print(f'🖼️ Logo/图片：{"已保留" if has_drawing and media else "❌缺失"}')
    print(f'📁 媒体文件：{media}')
    print(f'🎨 使用样式：{sorted(styles_used)}')
    print(f'📅 当前日期：{"已正确写入" if has_today_date else "❌缺失"}')
    print(f'💬 模板残留：{"无" if not has_template_leftover else "⚠️ 检测到残留提示文字"}')
    print(f'🤖 AI 披露：{"已写入" if has_ai_disclosure else "未写入"}')
    print("=" * 50)
    print("✅ 文档生成完成！请打开 Word 目视检查分页和格式。")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--template", required=True, type=Path)
    ap.add_argument("--content", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()
    build(args.template, args.content, args.output)


if __name__ == "__main__":
    main()
