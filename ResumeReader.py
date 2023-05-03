import re
import os
import logging
import PyPDF2
import pdfplumber
import fitz

class ResumeReader:

    def convert_pdf_to_txt(self, pdf_file):

        with open(pdf_file, mode='rb') as file:
            reader = PyPDF2.PdfReader(file)
            raw_text = ''
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                raw_text += page.extract_text()    
      
        try:
            full_string = re.sub(r'\n+', '\n', raw_text)
            full_string = full_string.replace("\r", "\n")
            full_string = full_string.replace("\t", " ")

            # Remove awkward LaTeX bullet characters
            full_string = re.sub(r"\uf0b7", " ", full_string)
            full_string = re.sub(r"\(cid:\d{0,3}\)", " ", full_string)
            full_string = re.sub(r'• ', " ", full_string)

            # Split text blob into individual lines
            resume_lines = full_string.splitlines(True)

            # Remove empty strings and whitespaces
            resume_lines = [re.sub('\s+', ' ', line.strip()) for line in resume_lines if line.strip()]
           
            print(resume_lines, raw_text)
            return resume_lines, raw_text 
        except Exception as e:
            logging.error('Error in pdf file:: ' + str(e))
            return [], " "

    def read_file(self, file,docx_parser = "tika"):
        file = os.path.join(file)
        if file.endswith('pdf'):
            resume_lines, raw_text = self.convert_pdf_to_txt(file)
        elif file.endswith('txt'):
            with open(file, 'r', encoding='utf-8') as f:
                resume_lines = f.readlines()

        else:
            resume_lines = None
        
      
        return resume_lines 