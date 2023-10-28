from bs4 import BeautifulSoup
import requests

def copy_html_content(ranobe, chapter_number, tom, translate):

    url = f"https://ranobelib.me/{ranobe}/v{tom}/c{chapter_number}{translate}"

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html_content = response.content
        return html_content
    else:
        print(f"Failed to retrieve HTML content for chapter {chapter_number}. Status code: {response.status_code}")
        return None

def extract_summary(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    return print(soup)


if __name__ == '__main__':
    ranobe = "the-novels-extra"
    translate = ""
    tom = 1
    start = 277
    chapter_number = 277  # Specify the desired chapter number here

    for chapter in range(start, chapter_number+1):
        try:
            html_content = copy_html_content(ranobe, chapter, tom, translate)
            # print(html_content)
        except:
            tom += 1-1
            print("New Tom: ", tom)
            continue

        if html_content == None:
            continue

        extract_summary(html_content)

