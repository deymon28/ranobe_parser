from bs4 import BeautifulSoup
import requests
from unidecode import unidecode


def request_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html_content = response.content
        return html_content
    else:
        print(f"Failed to retrieve HTML content for page {url}. Status code: {response.status_code}")
        return None


def chapter_pages(book):
    html_content = request_page(book)

    soup = BeautifulSoup(html_content, 'lxml')

    number_of_pages = soup.find("<div>", _class="pages").find_all("a")

    if number_of_pages:
        last_number_of_pages = number_of_pages[-1]
        return int(last_number_of_pages.text)
    else:
        return print("Error: Чомусь не можливо отримати кількість сторінок(chapter_pages)")


def parse_chapters_hrefs(number_of_pages):
    names_hrefs = {}

    for i in range(1, number_of_pages + 1):
        url = f"https://ranobes.com/chapters/second-life-ranker/page/{i}"

        html_content = request_page(url)
        soup = BeautifulSoup(html_content, 'lxml')

        y = 1
        while y <= 30:
            divs = soup.find_next("div", _class="cat_block cat_line").find("a")
            temporarily = {divs.get('title'): divs.get('href')}
            names_hrefs.update(temporarily)
            y += 1

    return names_hrefs


def extrakt_chapter(names_hrefs):

    for name, href in names_hrefs:
        html_content = request_page(href)
        soup = BeautifulSoup(html_content, 'lxml')

        paragraphs = soup.select('.text p')

        # Extract and format the paragraphs
        formatted_paragraphs = []
        for paragraph in paragraphs:
            # Remove any existing line breaks within the paragraph
            cleaned_paragraph = paragraph.get_text().replace('\n', ' ')
            formatted_paragraphs.append(cleaned_paragraph)

        # Join the paragraphs with a newline character after each </p>
        result = '\n'.join(formatted_paragraphs)
        result = name + "\n\n" + result

        return name, result



def save_chapter(text, name):
    with open(f'{name}.txt', 'w', encoding='utf-8') as output_file:
        output_file.write(text)

    print("Text extracted and saved to:", name)


def clean_text(input_text):
    text = input_text.replace("  ", " ")
    text = text.replace("   ", " ")

    cleaned_text = []
    for char in text:
        if ord('А') <= ord(char) <= ord('я') or char in "ёЁ":  # Preserve Russian letters
            cleaned_text.append(char)
        else:
            cleaned_text.append(unidecode(char))  # Replace non-ASCII characters
    cleaned_text = ''.join(cleaned_text)

    cleaned_text = cleaned_text.replace("--", "-")
    cleaned_text = cleaned_text.replace("<<", "\"")
    cleaned_text = cleaned_text.replace(">>", "\"")

    return cleaned_text


if __name__ == '__main__':
    book = "https://ranobes.com/chapters/second-life-ranker/"

    number_of_pages = chapter_pages(book)

    names_hrefs = parse_chapters_hrefs(number_of_pages)

    name, text = extrakt_chapter(names_hrefs)

    clean_chapter = clean_text(text)

    save_chapter = save_chapter(clean_chapter, name)