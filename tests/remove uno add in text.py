import re

def clean_text(input_text):
    # Use a regular expression to replace multiple spaces with a single space
    cleaned_text = re.sub(r' +', ' ', input_text)
    return cleaned_text

# Example usage:
input_text = "This   is   an   example   with   multiple   spaces. \n колись  мри арпп   араоп аи  оаи ата  "
cleaned_text = clean_text(input_text)
print(cleaned_text)

