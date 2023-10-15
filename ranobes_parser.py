from bs4 import BeautifulSoup
import requests
from unidecode import unidecode
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pickle
from selenium.webdriver.common.by import By

def selenium_firs_page(src):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"

    options = Options()
    options._ignore_local_proxy = True
    options.add_argument(f"user-agent={user_agent}")
    #options.add_argument('--headless=new')  # hide browser

    driver = webdriver.Chrome(options=options)
    driver.get(src)
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    time.sleep(1)
    driver.find_element(By.ID, "content").click()
    time.sleep(1)
    # pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
    content = driver.page_source.encode('utf-8').strip()
    # soup = BeautifulSoup(content, 'lxml')
    # return print(soup)

    return content




def request_page(url):
    return selenium_firs_page(url)
    #
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}
    # response = requests.get(url, headers=headers, cookies=load_cookies())
    #
    # if response.status_code == 200:
    #     html_content = response.content
    #     return html_content
    # else:
    #     print(f"Failed to retrieve HTML content for page {url}. Status code: {response.status_code}")
    #     return None


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

    for i in range(2, number_of_pages + 1):
        url = book_url + f"page/{i}"


        html_content = request_page(url)
        soup = BeautifulSoup(html_content, 'lxml')

        # y = 1
        # while y <= 30:
        divs = soup.find_all("div", class_="cat_block cat_line")
        for div in divs:
            a_tag = div.find("a")
            if a_tag:
                temporarily = {a_tag.get('title'): a_tag.get('href')}
                names_hrefs.update(temporarily)

            # print(divs)
            # temporarily = {divs.get('title'): divs.get('href')}
            # names_hrefs.update(temporarily)
            # y += 1

    print(names_hrefs)
    return names_hrefs


def extrakt_chapter(names_hrefs):

    for name, href in names_hrefs.items():
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

        return name, result #завершує цикл після 1 операції, потрібно виправити



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
    cleaned_text = cleaned_text.replace(" .", ".")

    return cleaned_text


if __name__ == '__main__':
    book = "https://ranobes.com/chapters/second-life-ranker/"

    selenium_firs_page(book)

    number_of_pages = chapter_pages(book)

    names_hrefs = parse_chapters_hrefs(book, number_of_pages)

    name, text = extrakt_chapter(names_hrefs)

    clean_chapter = clean_text(text)

    save_chapter(clean_chapter, name)