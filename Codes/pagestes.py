import PyPDF2

def get_pdf_page_count(pdf_path):
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)
        # Get the number of pages
        num_pages = len(pdf_reader.pages)
        return num_pages

# Example usage
pdf_path = 'C:/Programming/Server/air-printer/Codes/received/192.168.1.12/Untitled document.pdf'  # Replace with the path to your PDF file
print(f"The number of pages in the PDF is: {get_pdf_page_count(pdf_path)}")

import os

def get_file_name(file_path):
    # Get the base name of the file path
    file_name = os.path.basename(file_path)
    return file_name

# Example usage
full_file_path = '/path/to/your/file/example.pdf'
print(f"The file name is: {get_file_name(pdf_path)}")
