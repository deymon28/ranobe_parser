import os
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

def extract_text_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    print(soup)
    return soup.get_text()

def split_epub_to_chapters(epub_file):
    book = epub.read_epub(epub_file)
    chapters = [item for item in book.items if isinstance(item, epub.EpubHtml)]

    for i, chapter in enumerate(chapters):
        chapter_content = chapter.content
        chapter_name = chapter.get_name() or "Chapter_"+ str(i + 1)
        chapter_file_name = chapter_name + ".txt"

        chapter_text = extract_text_from_html(chapter_content)
        
        with open(chapter_file_name, "w", encoding="utf-8") as chapter_file:
            chapter_file.write(chapter_text)

        print("Chapter '"+chapter_name+"' saved to '"+chapter_file_name+"'.")

    print("EPUB splitting completed.")

# Example usage
epub_file_path = r"C:\Users\dimag\Desktop\Yumemiru Danshi wa Genjitsushugisha Volume 4.epub"
split_epub_to_chapters(epub_file_path)
