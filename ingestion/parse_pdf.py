import fitz
import re
import json

SECTION_PATTERN = re.compile(r"^\d+(\.\d+)*\s+.*")
FIGURE_PATTERN = re.compile(r"(Figure\s+\d+.*)", re.IGNORECASE)

def split_text(text, max_chars=1500):
    chunks = []
    while len(text) > max_chars:
        chunks.append(text[:max_chars])
        text = text[max_chars:]
    chunks.append(text)
    return chunks

def is_table_line(line):
    return "|" in line or "\t" in line or re.search(r"\s{2,}", line)

def parse_table(table_lines):
    rows = [re.split(r"\s{2,}|\t|\|", line.strip()) for line in table_lines]

    if len(rows) < 2:
        return None

    headers = rows[0]
    structured = []

    for row in rows[1:]:
        if len(row) == len(headers):
            structured.append(dict(zip(headers, row)))

    return {
        "headers": headers,
        "rows": structured
    }

def extract_hierarchy(section):
    parts = section.split()[0]
    levels = parts.split(".")

    return {
        "level_1": levels[0] if len(levels) > 0 else None,
        "level_2": ".".join(levels[:2]) if len(levels) > 1 else None,
        "level_3": ".".join(levels[:3]) if len(levels) > 2 else None
    }

def enrich_figure_context(buffer, figures):
    if not figures:
        return buffer

    return f"Related Figures: {figures}\n\n{buffer}"

def extract_sections(pdf_path):
    doc = fitz.open(pdf_path)

    data = []
    current_section = "Unknown"
    buffer = ""
    figures = []
    table_buffer = []
    in_table = False

    for page_num, page in enumerate(doc):
        text = page.get_text()
        lines = text.split("\n")

        for line in lines:
            line = line.strip()

            if FIGURE_PATTERN.match(line):
                figures.append(line)

            if is_table_line(line):
                table_buffer.append(line)
                in_table = True
                continue

            if in_table:
                table_json = parse_table(table_buffer)

                data.append({
                    "content": json.dumps(table_json) if table_json else "\n".join(table_buffer),
                    "section": current_section,
                    "page": page_num + 1,
                    "type": "table"
                })

                table_buffer = []
                in_table = False

            if SECTION_PATTERN.match(line):
                if buffer:
                    chunks = split_text(buffer)
                    hierarchy = extract_hierarchy(current_section)
                    enriched = enrich_figure_context(buffer, figures)

                    for chunk in chunks:
                        data.append({
                            "content": enriched,
                            "section": current_section,
                            "page": page_num + 1,
                            "figures": figures,
                            "hierarchy": hierarchy
                        })

                    buffer = ""
                    figures = []

                current_section = line

            buffer += " " + line

    if buffer:
        chunks = split_text(buffer)
        hierarchy = extract_hierarchy(current_section)

        for chunk in chunks:
            data.append({
                "content": buffer,
                "section": current_section,
                "page": page_num + 1,
                "hierarchy": hierarchy
            })

    with open("data/processed.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print("✅ Advanced parsing complete!")

if __name__ == "__main__":
    extract_sections("data/nasa.pdf")