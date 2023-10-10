import re
from bs4 import BeautifulSoup
import requests


def copy_html_content(chapter_number, tom):
    url = f"https://ranobelib.me/dou-luo-da-lu/v{tom}/c{chapter_number}"

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
    plain_text = soup.get_text(separator='\n')

    # Extract text between "Summary:" and "INDUSTRY CLASSIFICATION:"
    chapter = re.search(r'Оглавление(.*?)Настройки', plain_text, re.DOTALL)
    summary_text = re.search(r'Сообщить об ошибке(.*?)Реклама', plain_text, re.DOTALL)
    if summary_text:
        result = chapter.group(1).strip() + "\n" + summary_text.group(1).strip()
        return result
    else:
        return "Summary not found."


def extract_chapter(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    plain_text = soup.get_text(separator='\n')
    chapter = re.search(r'Оглавление(.*?)Настройки', plain_text, re.DOTALL)
    chapter_name = chapter.group(1).strip()
    return chapter_name


if __name__ == '__main__':
    start = 197
    chapter_number = 340  # Specify the desired chapter number here
    tom = 29
    for chapter in range(start, chapter_number+1):
        try:
            html_content = copy_html_content(chapter, tom)

            extracted_text = extract_summary(html_content)

            output_file_path = extract_chapter(html_content)
            with open(f'{output_file_path}.txt', 'w') as output_file:
                output_file.write(extracted_text)

            print("Text extracted and saved to:", output_file_path)
        except:
            tom += 1
            print("New Tom: ", tom)
            continue