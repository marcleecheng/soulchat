"""epub → 纯文本"""

from pathlib import Path

import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub


def parse_epub(file_path: Path) -> str:
    book = epub.read_epub(str(file_path))
    chapters = []
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        soup = BeautifulSoup(item.get_content(), "html.parser")
        text = soup.get_text(separator="\n", strip=True)
        if text.strip():
            chapters.append(text)
    return "\n\n---\n\n".join(chapters)
