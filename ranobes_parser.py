from bs4 import BeautifulSoup
from unidecode import unidecode
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pickle
from selenium.webdriver.common.by import By

def selenium_firs_page(src):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"

    options = Options()
    options._ignore_local_proxy = True
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument('--headless=new')  # hide browser

    driver = webdriver.Chrome(options=options)
    driver.get(src)

    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

    time.sleep(0.2)
    try:
        driver.find_element(By.ID, "content").click()
    except:
        pass

    time.sleep(0.8)

    # pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
    content = driver.page_source.encode('utf-8').strip()
    # soup = BeautifulSoup(content, 'lxml')
    # return print(soup)

    return content


def request_page(url):
    return selenium_firs_page(url)


def chapter_pages(book):
    html_content = request_page(book)
    # print(html_content)

    soup = BeautifulSoup(html_content, 'lxml')
    # print(soup)

    number_of_pages = soup.find("div", class_="pages").find_all("a")

    if number_of_pages:
        last_number_of_pages = number_of_pages[-1]
        print("\n#\n#\n#\n#\n#\n" + last_number_of_pages.text + "\n#\n#\n#\n#\n#\n")
        return int(last_number_of_pages.text)
    else:
        return print("Error: Чомусь не можливо отримати кількість сторінок(chapter_pages)")


def parse_chapters_hrefs(book_url, number_of_pages):
    names_hrefs = {}

    for i in range(1, number_of_pages + 1):
        url = f"{book_url}page/{i}"
        html_content = request_page(url)
        soup = BeautifulSoup(html_content, 'lxml')

        chapter_divs = soup.find_all("div", class_="cat_block cat_line")
        print(chapter_divs)
        for div in chapter_divs:
            a_tag = div.find("a")
            if a_tag:
                chapter_title = a_tag.get('title')
                chapter_link = a_tag.get('href')
                names_hrefs[chapter_title] = chapter_link
            else:
                print("Warning: No chapter link found in div.")

    return names_hrefs


def extract_chapter(names_hrefs):
    for name, href in names_hrefs.items():
        html_content = request_page(href)
        soup = BeautifulSoup(html_content, 'lxml')

        # Extract text from elements with class 'text' that have 'p' elements
        paragraphs = soup.select('.text p')

        if paragraphs:
            # If paragraphs are found, extract and format them
            formatted_paragraphs = []
            for paragraph in paragraphs:
                # Remove any existing line breaks within the paragraph
                cleaned_paragraph = paragraph.get_text().replace('\n', ' ')
                formatted_paragraphs.append(cleaned_paragraph)

            # Join the paragraphs with a newline character after each </p>
            result = '\n'.join(formatted_paragraphs)
        else:
            # If there are no 'p' elements, extract and format the text directly from the '.text' element
            text_element = soup.select_one('.text')
            if text_element:
                result = text_element.get_text().replace('\n', ' ')
                result = result.replace('<br>', '\n')
            else:
                result = ""  # Handle the case where no text is found

        result = name + "\n\n" + result

        clean_chapter = clean_text(result)
        save_chapter(clean_chapter, name)


def clean_text(input_text):
    text = re.sub(r' +', ' ', input_text) # need tests on workability

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
    cleaned_text = cleaned_text.replace("<", "")
    cleaned_text = cleaned_text.replace(">", "")
    cleaned_text = cleaned_text.replace(" .", ".")
    cleaned_text = cleaned_text.replace(" !", "!")
    cleaned_text = cleaned_text.replace(" ?", "?")

    cleaned_text = '\n'.join(line.lstrip() for line in cleaned_text.split('\n'))

    return cleaned_text


def save_chapter(text, name):
    with open(f'{name}.txt', 'w', encoding='utf-8') as output_file:
        output_file.write(text)

    print("Chapter saved how:", name)


if __name__ == '__main__':
    book = "https://ranobes.com/chapters/the-novels-extra/"

    # selenium_firs_page(book)

    number_of_pages = chapter_pages(book)

    names_hrefs = parse_chapters_hrefs(book, number_of_pages)

    extract_chapter(names_hrefs)

    # clean_chapter = clean_text(text)
    #
    # save_chapter(clean_chapter, name)