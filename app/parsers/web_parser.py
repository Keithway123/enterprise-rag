import logging
from pathlib import Path

from bs4 import BeautifulSoup


def parse_web(file_path: str) -> dict:
    """
    Parse a local HTML file and align output with PDF/Word parsers.
    Boundary: first version only handles static local HTML, not URL or JS rendering.
    """
    html = Path(file_path).read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    # Remove common page chrome to reduce noisy vectors.
    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()

    content = []
    table_index = 0
    body = soup.body or soup

    for element in body.descendants:
        if not getattr(element, "name", None):
            continue

        if element.name in ["h1", "h2", "h3", "h4", "h5", "h6", "p", "li"]:
            if _is_inside_table(element):
                continue

            text = element.get_text(" ", strip=True)
            if text:
                content.append({
                    "page": None,
                    "type": "text",
                    "text": text,
                })

        elif element.name == "table":
            table_data = _extract_html_table(element)
            if table_data:
                table_index += 1
                content.append({
                    "page": None,
                    "type": "table",
                    "table_index": table_index,
                    "data": table_data,
                })

    if not content:
        logging.warning(f"{file_path} extracted no web content; check the HTML structure")

    return {
        "mode": "web",
        "content": content,
        "source": file_path,
    }


def _extract_html_table(table_tag) -> list[list[str]]:
    """
    Convert HTML table into rows so existing chunk_table can be reused.
    """
    rows = []

    for tr in table_tag.find_all("tr"):
        row = []
        for cell in tr.find_all(["th", "td"]):
            row.append(cell.get_text(" ", strip=True))

        if row:
            rows.append(row)

    return rows


def _is_inside_table(element) -> bool:
    """
    HTML table is parsed as structured data, so nested text nodes should be skipped.
    """
    return element.find_parent("table") is not None


if __name__ == "__main__":
    result = parse_web("data/raw/test_web.html")
    print(result)
