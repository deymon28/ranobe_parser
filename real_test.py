import re
from bs4 import BeautifulSoup
import requests
from unidecode import unidecode

def copy_html_content(ranobe, chapter_number, tom, translate):

    url = f"https://ranobelib.me/{ranobe}/v{tom}/c{chapter_number}{translate}"

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html_content = response.content
        return html_content
    else:
        print(f"Failed to retrieve HTML content for chapter {chapter_number}. Status code: {response.status_code}")
        return None


def split_string(string):
  index = string.find("Глава")
  string = string[:index] + "\n" + string[index:]

  return string


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

    split_string_chapter_name = split_string(chapter_name)

    # Join the paragraphs with a newline character after each </p>
    result = '\n'.join(formatted_paragraphs)
    result = split_string_chapter_name + "\n\n" + result

    return result, chapter_name


def clean_text(input_text):
    text = "  ".join(input_text.split())
    cleaned_text = []
    for char in text:
        if ord('А') <= ord(char) <= ord('я') or char in "ёЁ":  # Preserve Russian letters
            cleaned_text.append(char)
        else:
            cleaned_text.append(unidecode(char))  # Replace non-ASCII characters
    return ''.join(cleaned_text)



if __name__ == '__main__':
    ranobe = "the-novels-extra"
    translate = ""
    tom = 1
    start = 466
    chapter_number = 533  # Specify the desired chapter number here

    for chapter in range(start, chapter_number+1):
        try:
            html_content = copy_html_content(ranobe, chapter, tom, translate)
            # print(html_content)
        except:
            tom += 1 - 1
            print("New Tom: ", tom)
            continue

        extracted_text, output_file_path = extract_summary(html_content)

        text = clean_text(extracted_text)

        with open(f'{output_file_path}.txt', 'w', encoding='utf-8') as output_file:
            output_file.write(text)

        print("Text extracted and saved to:", output_file_path)

