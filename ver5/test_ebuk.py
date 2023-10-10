import os
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import re

def extract_text_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    print(soup)
    chapter_name = soup.find("h2")
    if chapter_name:
        chapter_name = chapter_name.get_text()
    else:
        chapter_name = None

    # Find all <h2> elements in the soup
    h2_elements = soup.find_all("h2")

    # If there is more than one <h2>, remove the second one and its following <p> elements
    if len(h2_elements) > 1:
        for i, h2_element in enumerate(h2_elements):
            if i == 1:
                # Remove the second <h2> element and all elements that follow it
                for tag in h2_element.find_all_next():
                    tag.extract()

    # Extract the text from all remaining <p> elements
    paragraphs = soup.find_all("p")
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
        chapter_name, chapter_text = extract_text_from_html(chapter_content)
        chapter_name = chapter_name or "Chapter_" + str(i + 1)
        chapter_file_name = sanitize_filename("Том 2 " + chapter_name) + ".txt"

        chapter_text = clean_text(chapter_text)

        with open(chapter_file_name, "w", encoding="utf-8") as chapter_file:
            if chapter_name:
                chapter_file.write("Том 2\n" + chapter_name + "\n\n")
            chapter_file.write(chapter_text)

        print("Chapter '{}' saved to '{}'.".format(chapter_name, chapter_file_name))

    print("EPUB splitting completed.")

# Example usage
epub_file_path = r"C:\Users\dimag\Desktop\Suddenly Became A Princess One Day[2].epub"
split_epub_to_chapters(epub_file_path)
