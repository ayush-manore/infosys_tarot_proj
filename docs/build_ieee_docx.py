"""
IEEE Report → Word Document Generator
Converts docs/IEEE_REPORT.md into a properly formatted .docx file
with IEEE conference paper styling.

Run:  python docs/build_ieee_docx.py
Requires: pip install python-docx
"""

from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn
import re
import os

# ── Path resolution ────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(SCRIPT_DIR, "IEEE_REPORT.md")
OUT_PATH = os.path.join(SCRIPT_DIR, "MysticAI_IEEE_Report.docx")

# ── Document setup ─────────────────────────────────────────────────────
doc = Document()

# Page setup: A4, 1-inch margins, two-column feel via narrow margins
section = doc.sections[0]
section.page_width  = Cm(21.0)
section.page_height = Cm(29.7)
section.top_margin    = Cm(2.0)
section.bottom_margin = Cm(2.0)
section.left_margin   = Cm(2.0)
section.right_margin  = Cm(2.0)

# ── Style definitions ──────────────────────────────────────────────────
style = doc.styles

# Normal text
normal = style['Normal']
normal.font.name = 'Times New Roman'
normal.font.size = Pt(10)
normal.paragraph_format.space_after = Pt(4)
normal.paragraph_format.space_before = Pt(0)
normal.paragraph_format.line_spacing = 1.15

# Title
if 'IEEE Title' not in [s.name for s in style]:
    ts = style.add_style('IEEE Title', 1)  # WD_STYLE_TYPE.PARAGRAPH
    ts.font.name = 'Times New Roman'
    ts.font.size = Pt(22)
    ts.font.bold = True
    ts.font.color.rgb = RGBColor(0x1A, 0x1A, 0x2E)
    ts.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    ts.paragraph_format.space_after = Pt(6)

# Subtitle / Author info
if 'IEEE Subtitle' not in [s.name for s in style]:
    ss = style.add_style('IEEE Subtitle', 1)
    ss.font.name = 'Times New Roman'
    ss.font.size = Pt(10)
    ss.font.italic = True
    ss.font.color.rgb = RGBColor(0x44, 0x44, 0x44)
    ss.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    ss.paragraph_format.space_after = Pt(2)

# Section heading (I, II, III...)
if 'IEEE Section' not in [s.name for s in style]:
    sh = style.add_style('IEEE Section', 1)
    sh.font.name = 'Times New Roman'
    sh.font.size = Pt(12)
    sh.font.bold = True
    sh.font.color.rgb = RGBColor(0x1A, 0x1A, 0x2E)
    sh.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sh.paragraph_format.space_before = Pt(14)
    sh.paragraph_format.space_after = Pt(6)

# Subsection heading (A, B, C...)
if 'IEEE Subsection' not in [s.name for s in style]:
    sub = style.add_style('IEEE Subsection', 1)
    sub.font.name = 'Times New Roman'
    sub.font.size = Pt(10)
    sub.font.bold = True
    sub.font.italic = True
    sub.paragraph_format.space_before = Pt(8)
    sub.paragraph_format.space_after = Pt(4)

# Code block
if 'Code Block' not in [s.name for s in style]:
    cb = style.add_style('Code Block', 1)
    cb.font.name = 'Consolas'
    cb.font.size = Pt(8)
    cb.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
    cb.paragraph_format.space_before = Pt(4)
    cb.paragraph_format.space_after = Pt(4)
    # Shading
    shading = cb.paragraph_format._element.get_or_add_pPr()
    bg = shading.makeelement(qn('w:shd'), {
        qn('w:val'): 'clear',
        qn('w:color'): 'auto',
        qn('w:fill'): 'F0F0F5'
    })
    shading.append(bg)

# Table caption
if 'Table Caption' not in [s.name for s in style]:
    tc = style.add_style('Table Caption', 1)
    tc.font.name = 'Times New Roman'
    tc.font.size = Pt(9)
    tc.font.bold = True
    tc.font.color.rgb = RGBColor(0x1A, 0x1A, 0x2E)
    tc.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    tc.paragraph_format.space_before = Pt(8)
    tc.paragraph_format.space_after = Pt(4)


# ── Helper functions ───────────────────────────────────────────────────

def add_styled_run(paragraph, text, bold=False, italic=False, font_size=None, color=None, font_name=None):
    """Add a run with specific formatting to a paragraph."""
    run = paragraph.add_run(text)
    if bold:
        run.bold = True
    if italic:
        run.italic = True
    if font_size:
        run.font.size = Pt(font_size)
    if color:
        run.font.color.rgb = color
    if font_name:
        run.font.name = font_name
    return run


def format_inline_text(paragraph, text, base_size=10):
    """Parse markdown inline formatting (**bold**, *italic*, `code`) and add runs."""
    # Split by bold, italic, and code markers
    parts = re.split(r'(\*\*.*?\*\*|\*.*?\*|`[^`]+`)', text)
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            add_styled_run(paragraph, part[2:-2], bold=True, font_size=base_size)
        elif part.startswith('*') and part.endswith('*') and not part.startswith('**'):
            add_styled_run(paragraph, part[1:-1], italic=True, font_size=base_size)
        elif part.startswith('`') and part.endswith('`'):
            add_styled_run(paragraph, part[1:-1], font_name='Consolas', font_size=base_size - 1,
                          color=RGBColor(0x88, 0x22, 0x44))
        else:
            add_styled_run(paragraph, part, font_size=base_size)


def add_table_from_lines(lines):
    """Parse markdown table lines and add a formatted table to the document."""
    # Filter separator lines
    data_lines = [l for l in lines if not re.match(r'^\|[\s\-:|]+\|$', l)]
    if not data_lines:
        return

    rows = []
    for line in data_lines:
        cells = [c.strip() for c in line.strip('|').split('|')]
        rows.append(cells)

    if len(rows) < 1:
        return

    num_cols = len(rows[0])
    table = doc.add_table(rows=len(rows), cols=num_cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = 'Table Grid'

    for ri, row_data in enumerate(rows):
        for ci in range(min(len(row_data), num_cols)):
            cell = table.cell(ri, ci)
            cell.text = ''
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.space_before = Pt(2)

            text = row_data[ci].strip()
            if ri == 0:  # Header row
                run = p.add_run(text)
                run.bold = True
                run.font.size = Pt(8)
                run.font.name = 'Times New Roman'
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                # Header bg
                tc_pr = cell._element.get_or_add_tcPr()
                shading = tc_pr.makeelement(qn('w:shd'), {
                    qn('w:val'): 'clear',
                    qn('w:color'): 'auto',
                    qn('w:fill'): '2D2D5E'
                })
                tc_pr.append(shading)
            else:
                # Handle inline formatting
                format_inline_text(p, text, base_size=8)
                # Alternating row colors
                if ri % 2 == 0:
                    tc_pr = cell._element.get_or_add_tcPr()
                    shading = tc_pr.makeelement(qn('w:shd'), {
                        qn('w:val'): 'clear',
                        qn('w:color'): 'auto',
                        qn('w:fill'): 'F5F5FA'
                    })
                    tc_pr.append(shading)

    doc.add_paragraph()  # Spacer after table


def add_horizontal_rule():
    """Add a thin horizontal rule."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    pPr = p._element.get_or_add_pPr()
    pBdr = pPr.makeelement(qn('w:pBdr'), {})
    bottom = pBdr.makeelement(qn('w:bottom'), {
        qn('w:val'): 'single',
        qn('w:sz'): '4',
        qn('w:space'): '1',
        qn('w:color'): 'CCCCCC'
    })
    pBdr.append(bottom)
    pPr.append(pBdr)


# ── Parse and convert the markdown ─────────────────────────────────────

with open(MD_PATH, 'r', encoding='utf-8') as f:
    md_content = f.read()

lines = md_content.split('\n')

i = 0
in_code_block = False
code_lines = []
table_lines = []
in_table = False

while i < len(lines):
    line = lines[i]

    # ── Code block handling ──
    if line.strip().startswith('```'):
        if in_code_block:
            # End of code block - flush
            code_text = '\n'.join(code_lines)
            if code_text.strip():
                p = doc.add_paragraph(style='Code Block')
                run = p.add_run(code_text)
                run.font.name = 'Consolas'
                run.font.size = Pt(8)
            code_lines = []
            in_code_block = False
        else:
            # Flush any pending table
            if in_table and table_lines:
                add_table_from_lines(table_lines)
                table_lines = []
                in_table = False
            in_code_block = True
        i += 1
        continue

    if in_code_block:
        code_lines.append(line)
        i += 1
        continue

    # ── Table handling ──
    if line.strip().startswith('|') and '|' in line.strip()[1:]:
        table_lines.append(line.strip())
        in_table = True
        i += 1
        continue
    elif in_table and table_lines:
        add_table_from_lines(table_lines)
        table_lines = []
        in_table = False

    # ── Horizontal rule ──
    if line.strip() == '---':
        add_horizontal_rule()
        i += 1
        continue

    # ── Main title (# ...) ──
    if line.startswith('# ') and not line.startswith('## '):
        title_text = line[2:].strip()
        p = doc.add_paragraph(title_text, style='IEEE Title')
        i += 1
        continue

    # ── Section heading (## ...) ──
    if line.startswith('## ') and not line.startswith('### '):
        heading_text = line[3:].strip()
        p = doc.add_paragraph(heading_text, style='IEEE Section')
        i += 1
        continue

    # ── Subsection heading (### ...) ──
    if line.startswith('### '):
        sub_text = line[4:].strip()
        p = doc.add_paragraph(sub_text, style='IEEE Subsection')
        i += 1
        continue

    # ── Table caption (bold text ending with TABLE) ──
    if line.strip().startswith('**TABLE') and line.strip().endswith('**'):
        cap_text = line.strip().strip('*')
        p = doc.add_paragraph(cap_text, style='Table Caption')
        i += 1
        continue

    # ── Metadata lines (bold key: value) ──
    meta_match = re.match(r'^\*\*(.*?):\*\*\s*(.*)', line.strip())
    if meta_match and i < 10:
        p = doc.add_paragraph(style='IEEE Subtitle')
        add_styled_run(p, meta_match.group(1) + ': ', bold=True, font_size=10)
        add_styled_run(p, meta_match.group(2), font_size=10)
        i += 1
        continue

    # ── Numbered list ──
    num_match = re.match(r'^(\d+)\.\s+(.*)', line.strip())
    if num_match:
        p = doc.add_paragraph(style='Normal')
        p.paragraph_format.left_indent = Inches(0.3)
        format_inline_text(p, f"{num_match.group(1)}. {num_match.group(2)}")
        i += 1
        continue

    # ── Bullet list (- item) ──
    bullet_match = re.match(r'^[-*]\s+(.*)', line.strip())
    if bullet_match:
        p = doc.add_paragraph(style='Normal')
        p.paragraph_format.left_indent = Inches(0.3)
        format_inline_text(p, f"\u2022 {bullet_match.group(1)}")
        i += 1
        continue

    # ── Empty line ──
    if line.strip() == '':
        i += 1
        continue

    # ── Regular paragraph ──
    p = doc.add_paragraph(style='Normal')
    format_inline_text(p, line.strip())
    i += 1

# Flush any remaining table
if in_table and table_lines:
    add_table_from_lines(table_lines)


# ── Footer ─────────────────────────────────────────────────────────────
add_horizontal_rule()

footer_section = doc.sections[0]
footer = footer_section.footer
fp = footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = fp.add_run("MysticAI: AI-Powered Palmistry & Tarot Intelligence Platform | Ayush Manore | Infosys Springboard 2026")
run.font.size = Pt(8)
run.font.color.rgb = RGBColor(0x88, 0x88, 0x88)
run.font.name = 'Times New Roman'

# Add page numbers
from docx.oxml import OxmlElement
fld = OxmlElement('w:fldSimple')
fld.set(qn('w:instr'), 'PAGE')
run2 = fp.add_run(' | Page ')
run2.font.size = Pt(8)
run2.font.color.rgb = RGBColor(0x88, 0x88, 0x88)
fp._element.append(fld)
fld_run = OxmlElement('w:r')
fld_run_text = OxmlElement('w:t')
fld_run_text.text = ''
fld_run.append(fld_run_text)
fld.append(fld_run)


# ── Save ───────────────────────────────────────────────────────────────
doc.save(OUT_PATH)
print(f"[OK] IEEE Report saved to: {OUT_PATH}")
print(f"     Paragraphs: {len(doc.paragraphs)}")
print(f"     Tables: {len(doc.tables)}")
