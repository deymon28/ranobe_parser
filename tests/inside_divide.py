from unidecode import unidecode
import os


def clean_text(filepath):
    with open(filepath, 'r+', encoding='utf-8') as file:
        text = file.read()

        text = text.replace("  ", " ")
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

        # Rewrite the file with the modified contents
        file.seek(0)
        file.writelines(cleaned_text)
        file.truncate()



def process_files(directory):
    # Iterate over all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            clean_text(filepath)





if __name__ == '__main__':
    directory_path = r"C:\Users\dimag\Desktop\Лишний в своей же Истории"
    process_files(directory_path)