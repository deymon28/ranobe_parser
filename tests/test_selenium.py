from selenium import webdriver
from bs4 import BeautifulSoup

def selenium_first_page(src):
    options = webdriver.ChromeOptions()
    options._ignore_local_proxy = True

    driver = webdriver.Chrome(options=options)
    driver.get(src)

    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content, 'lxml')

    return soup

if __name__ == "__main__":
    book = "https://www.example.com/book"

    soup = selenium_first_page(book)

    # Extract the title of the book
    title = soup.find('h1', class_='book-title').text

    # Extract the author of the book
    author = soup.find('span', class_='book-author').text

    # Print the title and author of the book
    print(f"Title: {title}")
    print(f"Author: {author}")
