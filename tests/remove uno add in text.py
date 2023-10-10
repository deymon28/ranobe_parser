import os
import re

# Define the regular expression pattern to match the CSS code
# pattern = r'.*?{.*?}'

pattern = r'•OTM'

# Specify the directory where your text files are located
directory = r"C:\Users\dimag\Desktop\test1"

# Loop through all files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        file_path = os.path.join(directory, filename)

        # Read the file into a list of lines
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Remove CSS code from each line
        cleaned_lines = [re.sub(pattern, '', line) for line in lines]

        # Write the cleaned content back to the file
        with open(file_path, 'w') as file:
            file.writelines(cleaned_lines)
