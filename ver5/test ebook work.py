import os
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import re

def extract_text_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    print(soup)
        
    chapter_name = soup.find("div", id='a2UV')
    if chapter_name:
        chapter_name = chapter_name.get_text()
    else:
        chapter_name = None
    paragraphs = soup.find_all("div", _class="class_s2e")
    chapter_text = "\n".join([p.get_text() for p in paragraphs])
    return chapter_name, chapter_text

def clean_text(text):
    # Remove leading/trailing whitespaces
    text = text.strip()

    # Format the text properly
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r"\n\s+", "\n", text)

    return text

def sanitize_filename(filename):
    # Remove invalid characters from the filename
    return re.sub(r"[\/:*?\"<>|]", "", filename)

def split_epub_to_chapters(epub_file):
    book = epub.read_epub(epub_file)
    chapters = [item for item in book.items if isinstance(item, epub.EpubHtml)]
    

    for i, chapter in enumerate(chapters):
        chapter_content = chapter.content
        name = 'html' + str(i) + '.txt'
        with open(name, "w", encoding="utf-8") as file:
                file.write(str(chapter_content))

        chapter_name, chapter_text = extract_text_from_html(chapter_content)
        chapter_name = chapter_name or "Chapter_" + str(i + 1)
        chapter_file_name = sanitize_filename(chapter_name) + ".txt"

        chapter_text = clean_text(chapter_text)

        with open(chapter_file_name, "w", encoding="utf-8") as chapter_file:
            if chapter_name:
                chapter_file.write(chapter_name + "\n\n")
            chapter_file.write(chapter_text)

        print("Chapter '{}' saved to '{}'.".format(chapter_name, chapter_file_name))

    print("EPUB splitting completed.")

# Example usage
epub_file_path = r"C:\Users\dimag\Desktop\A Love Comedy about First Love, Supported by a Childhood Friend[1].epub"
split_epub_to_chapters(epub_file_path)
