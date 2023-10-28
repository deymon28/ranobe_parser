from bs4 import BeautifulSoup
import requests

def parse_urls():
    url = 'https://tl.rulate.ru/book/26523'

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html_content = response.content
        soup = BeautifulSoup(html_content, 'lxml')

        name = "Пошук.txt"
        data = open(name, "w", encoding="utf-8")

        for titles in soup.find_all("td", class_="t"):
            title = titles.find_next('a').get('href')

            data.write('https://tl.rulate.ru' + title + '\n')
            print(title)
        data.close()
    else:
        print(f"Failed to retrieve HTML content for chapter {url}. Status code: {response.status_code}")


def copy_html_content(chapter_number):
    url = chapter_number
    print(url)

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=headers)
    #print(response)

    if response.status_code == 200:
        html_content = response.content
        #print(html_content)
        return html_content
    else:
        print(f"Failed to retrieve HTML content for chapter {chapter_number}. Status code: {response.status_code}")
        return None


def extract_summary(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    summary_text = soup.find('div', class_="content-text").get_text(separator='\n')

    return summary_text


if __name__ == '__main__':
    # parse_urls()

    with open('Пошук.txt', 'r') as chapter_urls:
        urls = chapter_urls.read()

    for chapter in urls.split('\n'):

        html_content = copy_html_content(chapter)

        extracted_text = extract_summary(html_content).replace(' ', ' ')

        lines = extracted_text.strip().split('\n')
        updated_lines = lines[:-1]
        extracted_text = '\n'.join(updated_lines)

        output_file_path = urls.split('\n').index(chapter)
        print(output_file_path+1)

        with open(f'{output_file_path+1}.txt', 'w') as output_file:
            output_file.write(extracted_text)

        print("Text extracted and saved to:", output_file_path)
