import os
from ebooklib import epub
from bs4 import BeautifulSoup

def split_epub_to_chapters(epub_file):
    book = epub.read_epub(epub_file)

    for item_id, item in enumerate(book.get_items_of_type(epub.EpubHtml)):
        chapter_title = item.title if item.title else f"Chapter_{item_id}"
        chapter_content = item.content.decode('utf-8') if item.content else ""

        # Parse HTML and extract chapter content
        soup = BeautifulSoup(chapter_content, 'html.parser')
        body_content = soup.find('body').get_text()

        # Remove leading/trailing white spaces
        body_content = body_content.strip()

        # Create a new text file for each chapter
        chapter_file_name = f"{chapter_title}.txt"
        with open(chapter_file_name, "w", encoding="utf-8") as file:
            file.write(body_content)

        print(f"Chapter '{chapter_title}' saved as '{chapter_file_name}'.")

# Specify the path to your EPUB file
epub_path = r"C:\Users\dimag\Desktop\test\Seoul Station’s Necromancer.epub"

# Call the function to split the EPUB file into chapters
split_epub_to_chapters(epub_path)
