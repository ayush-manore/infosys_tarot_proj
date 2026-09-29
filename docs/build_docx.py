"""
Convert docs/PROJECT_REPORT.md into a beautifully formatted Word document (docs/PROJECT_REPORT.docx).
Uses python-docx with professional styling, typography, table design, code callout boxes, and headers/footers.
"""

import os
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    """Set the background color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=160, right=160):
    """Set padding for a cell in dxa (1 pt = 20 dxa)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def add_code_block(doc, code_text):
    """Render preformatted text or code in a light grey box with Consolas font."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    
    # Border
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>
            <w:left w:val="single" w:sz="18" w:space="0" w:color="4F46E5"/>
            <w:bottom w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>
            <w:right w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>
        </w:tcBorders>
    ''')
    tcPr.append(tcBorders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.05
    
    run = p.add_run(code_text.strip("\n"))
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
    
    # Add empty space after table
    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_before = Pt(2)
    spacer.paragraph_format.space_after = Pt(6)

def format_inline_markdown(p, text):
    """Parse basic bold (**text**) and inline code (`code`) and normal text."""
    # Pattern matching bold and inline code
    tokens = re.split(r'(\*\*.*?\*\*|`.*?`)', text)
    for token in tokens:
        if not token:
            continue
        if token.startswith('**') and token.endswith('**'):
            run = p.add_run(token[2:-2])
            run.bold = True
            run.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        elif token.startswith('`') and token.endswith('`'):
            run = p.add_run(token[1:-1])
            run.font.name = "Consolas"
            run.font.size = Pt(9.5)
            run.font.color.rgb = RGBColor(0x43, 0x38, 0xCA)
            run.bold = True
        else:
            run = p.add_run(token)
            run.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

def build_docx(md_path, docx_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    doc = docx.Document()
    
    # Page setup - Margins: 1 inch
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        # Header & Footer
        footer = section.footer
        p_ft = footer.paragraphs[0]
        p_ft.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_ft = p_ft.add_run("Palmistry & Tarot Intelligence Platform — Infosys Springboard Project Report")
        r_ft.font.name = "Segoe UI"
        r_ft.font.size = Pt(8.5)
        r_ft.font.color.rgb = RGBColor(0x94, 0xA3, 0xB8)
        
    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Segoe UI'
    normal_style.font.size = Pt(10.5)
    normal_style.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
    
    i = 0
    in_code_block = False
    code_lines = []
    
    # Table accumulation
    in_table = False
    table_rows = []
    
    while i < len(lines):
        raw_line = lines[i]
        line = raw_line.rstrip('\r\n')
        
        # Handle code blocks
        if line.strip().startswith('```'):
            if in_code_block:
                in_code_block = False
                add_code_block(doc, '\n'.join(code_lines))
                code_lines = []
            else:
                in_code_block = True
                code_lines = []
            i += 1
            continue
            
        if in_code_block:
            code_lines.append(line)
            i += 1
            continue
            
        # Handle markdown tables
        if line.strip().startswith('|') and line.strip().endswith('|'):
            # Check if separator row like |---|---|
            is_sep = all(c in ' |-:' for c in line.strip())
            if not is_sep:
                cells = [c.strip() for c in line.strip().split('|')[1:-1]]
                table_rows.append(cells)
            i += 1
            continue
        else:
            if table_rows:
                # Flush table
                num_cols = max(len(r) for r in table_rows)
                num_rows = len(table_rows)
                t = doc.add_table(rows=num_rows, cols=num_cols)
                t.alignment = WD_TABLE_ALIGNMENT.CENTER
                t.autofit = False
                
                col_widths = [Inches(6.5 / num_cols)] * num_cols
                # Adjust column widths if 2 or 3 cols
                if num_cols == 2:
                    col_widths = [Inches(2.5), Inches(4.0)]
                elif num_cols == 3:
                    col_widths = [Inches(2.0), Inches(3.2), Inches(1.3)]
                    
                for r_idx, row_data in enumerate(table_rows):
                    row = t.rows[r_idx]
                    is_header = (r_idx == 0)
                    for c_idx in range(num_cols):
                        cell = row.cells[c_idx]
                        cell.width = col_widths[c_idx]
                        text = row_data[c_idx] if c_idx < len(row_data) else ""
                        p = cell.paragraphs[0]
                        p.paragraph_format.space_before = Pt(3)
                        p.paragraph_format.space_after = Pt(3)
                        
                        set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
                        
                        if is_header:
                            set_cell_background(cell, "312E81") # Deep indigo
                            run = p.add_run(text)
                            run.font.name = "Segoe UI"
                            run.font.size = Pt(9.5)
                            run.bold = True
                            run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                        else:
                            bg_color = "F8FAFC" if (r_idx % 2 == 1) else "FFFFFF"
                            set_cell_background(cell, bg_color)
                            p.paragraph_format.line_spacing = 1.15
                            format_inline_markdown(p, text)
                            for r in p.runs:
                                r.font.name = "Segoe UI"
                                r.font.size = Pt(9)
                                
                        # Light borders
                        tcPr = cell._tc.get_or_add_tcPr()
                        tcBorders = parse_xml(f'''
                            <w:tcBorders {nsdecls("w")}>
                                <w:top w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
                                <w:left w:val="none"/>
                                <w:bottom w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
                                <w:right w:val="none"/>
                            </w:tcBorders>
                        ''')
                        tcPr.append(tcBorders)
                        
                spacer = doc.add_paragraph()
                spacer.paragraph_format.space_before = Pt(4)
                spacer.paragraph_format.space_after = Pt(4)
                table_rows = []
                
        # Skip horizontal rules
        if line.strip() == '---':
            i += 1
            continue
            
        # Headings
        if line.startswith('# '):
            # Document Title
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(8)
            
            run = p.add_run(line[2:].strip())
            run.font.name = "Segoe UI"
            run.font.size = Pt(22)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0x1E, 0x1B, 0x4B) # Midnight Indigo
            
            # Add subtitle banner
            p_sub = doc.add_paragraph()
            p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_sub.paragraph_format.space_before = Pt(0)
            p_sub.paragraph_format.space_after = Pt(22)
            r_sub = p_sub.add_run("Infosys Springboard Internship Project · All 4 Milestones Completed · Author: Ayush Manore")
            r_sub.font.name = "Segoe UI Semibold"
            r_sub.font.size = Pt(10)
            r_sub.font.color.rgb = RGBColor(0x4F, 0x46, 0xE5)
            
            i += 1
            continue
            
        elif line.startswith('## '):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.keep_with_next = True
            
            run = p.add_run(line[3:].strip())
            run.font.name = "Segoe UI"
            run.font.size = Pt(14)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0x31, 0x2E, 0x81) # Indigo 900
            
            i += 1
            continue
            
        elif line.startswith('### '):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            
            run = p.add_run(line[4:].strip())
            run.font.name = "Segoe UI Semibold"
            run.font.size = Pt(11.5)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0x43, 0x38, 0xCA) # Indigo 700
            
            i += 1
            continue
            
        elif line.startswith('#### '):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.keep_with_next = True
            
            run = p.add_run(line[5:].strip())
            run.font.name = "Segoe UI"
            run.font.size = Pt(10.5)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
            
            i += 1
            continue

        # Bullet points
        if line.strip().startswith('- ') or line.strip().startswith('* '):
            indent_level = (len(line) - len(line.lstrip())) // 2
            bullet_text = line.strip()[2:]
            
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.left_indent = Inches(0.25 * (indent_level + 1))
            
            format_inline_markdown(p, bullet_text)
            i += 1
            continue
            
        # Numbered list
        m_num = re.match(r'^\s*(\d+)\.\s+(.*)$', line)
        if m_num:
            num_text = m_num.group(2)
            p = doc.add_paragraph(style='List Number')
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.15
            format_inline_markdown(p, num_text)
            i += 1
            continue

        # Regular Paragraph
        if line.strip():
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(5)
            p.paragraph_format.line_spacing = 1.2
            format_inline_markdown(p, line.strip())
            
        i += 1
        
    doc.save(docx_path)
    print(f"[OK] Word file generated successfully at {docx_path}")

if __name__ == '__main__':
    md_file = r"c:\Users\ayush\Desktop\infosys_tarot_proj\docs\PROJECT_REPORT.md"
    docx_file = r"c:\Users\ayush\Desktop\infosys_tarot_proj\docs\PROJECT_REPORT.docx"
    build_docx(md_file, docx_file)
