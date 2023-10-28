'''The updated code you provided has fixed several issues, and it looks better than the previous version. However, there are still a few improvements that can be made for better functionality and readability:

Error Handling: Add proper error handling to your code. Handle exceptions that might occur during web scraping, file operations, and other critical parts of your script.

Function Naming: It's a good practice to use descriptive function names. For example, selenium_firs_page can be renamed to something like get_page_source_with_selenium to make it clear what the function does.

Variable Naming: Avoid using variable names like y. Use descriptive names that convey the purpose of the variable.

Loop Logic: In the parse_chapters_hrefs function, the while loop has a hardcoded limit of 30 iterations. Consider using a for loop with a fixed range instead of a while loop.

Return Values: Ensure that your functions return the appropriate values. For example, extrakt_chapter currently returns after the first iteration. If you want to collect all chapters, consider using a list to store them and return the list after the loop.

Code Comments: Add comments to explain complex logic or non-trivial operations in your code. This will make it easier for others (and your future self) to understand the code.

Code Organization: Consider breaking down your code into smaller functions with specific responsibilities. This will make your code modular and easier to maintain.

Here's an example of how you could structure your code with some of these improvements:

python
Copy code

# Import statements

def get_page_source_with_selenium(url):
    # Your Selenium logic here
    pass

def get_page_content_with_requests(url):
    # Your requests logic here
    pass

def extract_chapters_info(html_content):
    # Extract chapter names and URLs from the HTML content
    pass

def extract_chapter_text(html_content):
    # Extract and format chapter text from the HTML content
    pass

def clean_text(input_text):
    # Your text cleaning logic here
    pass

def save_chapter_to_file(text, name):
    # Save chapter text to a file
    pass

def main():
    book_url = "https://ranobes.com/chapters/second-life-ranker/"
    html_content = get_page_content_with_requests(book_url)
    chapters_info = extract_chapters_info(html_content)

    for chapter_name, chapter_url in chapters_info.items():
        chapter_html = get_page_content_with_requests(chapter_url)
        chapter_text = extract_chapter_text(chapter_html)
        cleaned_text = clean_text(chapter_text)
        save_chapter_to_file(cleaned_text, chapter_name)

if __name__ == '__main__':
    main()
Please note that the functions extract_chapters_info, extract_chapter_text, and others are placeholders. You should implement the logic inside these functions based on your specific requirements.


how to implement the 4th and 5th points you suggested
ChatGPT

2 / 2

Certainly! Let me guide you through implementing the 4th and 5th points, which involve improving the loop logic and ensuring proper return values in your code.

4. Loop Logic:
In the parse_chapters_hrefs function, you had a while loop with a hardcoded limit of 30 iterations. It's better to use a for loop with a fixed range for more control and readability. Here's how you can do it:

python
Copy code

def parse_chapters_hrefs(book_url, number_of_pages):
    names_hrefs = {}

    for i in range(1, number_of_pages + 1):
        url = f"{book_url}page/{i}"
        html_content = request_page(url)
        soup = BeautifulSoup(html_content, 'lxml')

        chapter_divs = soup.find_all("div", class_="cat_block cat_line")
        for div in chapter_divs:
            a_tag = div.find("a")
            chapter_title = a_tag.get('title')
            chapter_link = a_tag.get('href')
            names_hrefs[chapter_title] = chapter_link

    return names_hrefs

In this code, the loop iterates through each page and finds all the chapter links on that page. It adds each chapter's title and link to the names_hrefs dictionary.

5. Return Values:
In the extrakt_chapter function, you were returning after processing the first chapter. To collect all chapters, you can use a list to store the chapter data and return that list after the loop. Here's how you can modify the function:

python
Copy code

def extract_chapters(chapters_data):
    extracted_chapters = []

    for name, href in chapters_data.items():
        html_content = request_page(href)
        soup = BeautifulSoup(html_content, 'lxml')

        paragraphs = soup.select('.text p')
        formatted_paragraphs = []

        for paragraph in paragraphs:
            cleaned_paragraph = paragraph.get_text().replace('\n', ' ')
            formatted_paragraphs.append(cleaned_paragraph)

        chapter_text = '\n'.join(formatted_paragraphs)
        cleaned_text = clean_text(chapter_text)

        extracted_chapters.append((name, cleaned_text))

    return extracted_chapters

In this modified function, extracted_chapters is a list of tuples, where each tuple contains the chapter title and its cleaned text. The function loops through all chapters, processes them, and adds them to the list. Finally, the list of extracted chapters is returned.

These modifications ensure that your loops are efficient and that you collect and return all the necessary data from your functions. Remember to handle errors and edge cases appropriately for a robust implementation.

def parse_chapters_hrefs(book_url, number_of_pages):
    names_hrefs = {}

    for i in range(1, number_of_pages + 1):
        url = f"{book_url}page/{i}"
        html_content = request_page(url)
        soup = BeautifulSoup(html_content, 'lxml')

        chapter_divs = soup.find_all("div", class_="cat_block cat_line")
        for div in chapter_divs:
            a_tag = div.find("a")
            if a_tag:
                chapter_title = a_tag.get('title')
                chapter_link = a_tag.get('href')
                names_hrefs[chapter_title] = chapter_link
            else:
                print("Warning: No chapter link found in div.")

    return names_hrefs

'''


import re
from bs4 import BeautifulSoup
import requests
from unidecode import unidecode

def copy_html_content(ranobe, chapter_number, tom, translate):

    url = f"https://ranobelib.me/{ranobe}/v{tom}/c{float(chapter_number)}{translate}"
    print(url)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)

    html_content = response.content

    if response.status_code == 200:
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
    cleaned_text = cleaned_text.replace("<", "")
    cleaned_text = cleaned_text.replace(">", "")
    cleaned_text = cleaned_text.replace(" .", ".")
    cleaned_text = cleaned_text.replace(" !", "!")
    cleaned_text = cleaned_text.replace(" ?", "?")

    return cleaned_text



if __name__ == '__main__':
    ranobe = "trash-of-the-counts-family-novel"
    translate = ""
    tom = 2
    start = 1.1
    chapter_number = 8  # Specify the desired chapter number here

    for chapter_float in range(int(start * 10), int((chapter_number + 1) * 10)):
        chapter = float(chapter_float / 10)


        try:
            html_content = copy_html_content(ranobe, chapter, tom, translate)
            # print(html_content)
        except:
            tom += 1-1
            print("New Tom: ", tom)
            continue

        if html_content == None:
            continue

        try:
            extracted_text, output_file_path = extract_summary(html_content)
        except:
            continue

        text = clean_text(extracted_text)

        with open(f'{output_file_path}.txt', 'w', encoding='utf-8') as output_file:
            output_file.write(text)

        print("Text extracted and saved to:", output_file_path)




'''
from unidecode import unidecode
import os

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
    cleaned_text = cleaned_text.replace("<", "")
    cleaned_text = cleaned_text.replace(">", "")
    cleaned_text = cleaned_text.replace(" .", ".")
    cleaned_text = cleaned_text.replace(" !", "!")
    cleaned_text = cleaned_text.replace(" ?", "?")

    return cleaned_text


def clean_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)

            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()

            cleaned_text = clean_text(text)

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(cleaned_text)

if __name__ == "__main__":
    folder_path = r"E:\in work\Лишний в своей же Истории"  # Replace with the path to your folder containing .txt files
    clean_files_in_folder(folder_path)
'''