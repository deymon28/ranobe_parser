import os


def process_files(directory):
    # Iterate over all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            process_file(filepath)


def process_file(filepath):
    with open(filepath, 'r+') as file:
        lines = file.readlines()

        # Find the line with "Volume X Chapter X"
        for i, line in enumerate(lines):
            if line.startswith("Том") and "Глава" in line:
                volume_line, chapter_line = line.strip().split("Глава")

                # Modify the line to move the content after the volume and chapter numbers to new lines
                new_volume_line = volume_line.strip() + "\n"
                new_chapter_line = "Глава " + chapter_line.strip() + "\n"
                lines[i] = new_volume_line + new_chapter_line

                # Rewrite the file with the modified contents
                file.seek(0)
                file.writelines(lines)
                file.truncate()


# Provide the directory path where your .txt files are located
if __name__ == '__main__':
    directory_path = r"D:\Python_projects\Htmlparse"
    process_files(directory_path)