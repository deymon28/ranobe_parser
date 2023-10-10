import re
from bs4 import BeautifulSoup
import requests


def copy_html_content(chapter_number, tom, translate):

    url = f"https://ranobelib.me/the-novels-extra/v{tom}/c{chapter_number}{translate}"

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html_content = response.content
        return html_content
    else:
        print(f"Failed to retrieve HTML content for chapter {chapter_number}. Status code: {response.status_code}")
        return None


def extract_summary(html_content):
    # Convert HTML to plain text while preserving formatting
    soup = BeautifulSoup(html_content, 'lxml')

    # Find all paragraph elements within the reader-container
    paragraphs = soup.select('.reader-container p')
    plain_text = soup.get_text(separator='\n')

    chapter = re.search(r'Оглавление(.*?)Настройки', plain_text, re.DOTALL)
    chapter_name = chapter.group(1).strip()

    # Extract and format the paragraphs
    formatted_paragraphs = []
    for paragraph in paragraphs:
        # Remove any existing line breaks within the paragraph
        cleaned_paragraph = paragraph.get_text().replace('\n', ' ')
        formatted_paragraphs.append(cleaned_paragraph)

    # Join the paragraphs with a newline character after each </p>
    result = '\n'.join(formatted_paragraphs)
    result = chapter_name + "\n\n" + result

    return result, chapter_name


def extract_chapter(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    plain_text = soup.get_text(separator='\n')
    chapter = re.search(r'Оглавление(.*?)Настройки', plain_text, re.DOTALL)
    chapter_name = chapter.group(1).strip()
    return chapter_name


def clean_text(text):
    pass

if __name__ == '__main__':
    translate = ""
    start = 466
    chapter_number = 533  # Specify the desired chapter number here
    tom = 1
    for chapter in range(start, chapter_number+1):
        try:
            html_content = copy_html_content(chapter, tom, translate)
            # print(html_content)
        except:
            tom += 1 - 1
            print("New Tom: ", tom)
            continue

        extracted_text, output_file_path = extract_summary(html_content)

        # output_file_path = extract_chapter(html_content)

        with open(f'{output_file_path}.txt', 'w', encoding='utf-8') as output_file:
            output_file.write(extracted_text)

        print("Text extracted and saved to:", output_file_path)

