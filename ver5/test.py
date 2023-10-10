import os
from docx import Document

def process_docx_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".docx"):
            filepath = os.path.join(directory, filename)
            process_docx_file(filepath)

def process_docx_file(filepath):
    doc = Document(filepath)
    
    for para in doc.paragraphs:
        text = para.text
        if text.startswith("Том") and "Глава" in text:
            volume_text, chapter_text = text.strip().split("Глава")
            new_volume_text = volume_text.strip() + "\n"
            new_chapter_text = "Глава " + chapter_text.strip() + "\n"
            para.text = new_volume_text + new_chapter_text
    
    doc.save(filepath)

# Provide the directory path where your .docx files are located
directory_path = r"C:\Users\dimag\Desktop\1"
process_docx_files(directory_path)
