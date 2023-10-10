import os
from docx import Document

def convert_txt_to_docx(txt_folder, docx_folder):
    txt_files = [f for f in os.listdir(txt_folder) if f.endswith('.txt')]
    
    for txt_file in txt_files:
        txt_path = os.path.join(txt_folder, txt_file)
        docx_file = os.path.splitext(txt_file)[0] + '.docx'
        docx_path = os.path.join(docx_folder, docx_file)
        
        doc = Document()
        
        with open(txt_path, 'r') as txt_content:
            doc.add_paragraph(txt_content.read())
        
        doc.save(docx_path)
        # print(f'Converted {txt_file} to {docx_file}')
        print('Converted ' + str(txt_file) + ' to ' + str(docx_file))

if __name__ == "__main__":
    txt_folder = r"C:\Users\dimag\Desktop\chapters"
    docx_folder = r"C:\Users\dimag\Desktop\docx"
    
    if not os.path.exists(docx_folder):
        os.makedirs(docx_folder)
    
    convert_txt_to_docx(txt_folder, docx_folder)
