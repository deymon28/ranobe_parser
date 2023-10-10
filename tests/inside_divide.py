from unidecode import unidecode

# Input string with potentially non-Windows encoding characters
input_string = "「Безмолвие высокого уровня」"

# Define a function to clean the text, preserving Russian letters
def clean_text(input_text):
    cleaned_text = []
    for char in input_text:
        if ord('А') <= ord(char) <= ord('я') or char in "ёЁ":  # Preserve Russian letters
            cleaned_text.append(char)
        else:
            cleaned_text.append(unidecode(char))  # Replace non-ASCII characters
    return ''.join(cleaned_text)

# Clean the text while preserving Russian letters
cleaned_string = clean_text(input_string)

# Print the cleaned string
print(cleaned_string)







