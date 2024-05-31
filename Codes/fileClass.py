import PrintingSRC as printer
import PyPDF2
import os


class filer:

    def __init__(self, sender, file):

        self.senderName = sender
        self.file = file


    def sendprintjob(self):
        printer.calltoprint(self.file, self.senderName)

    def sender(self):
        return self.sender
    
    def pagecount(self):
        # Open the PDF file
        with open(self.file, 'rb') as file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)
            # Get the number of pages
            num_pages = len(pdf_reader.pages)
            return num_pages
        
    def filename(self):
    # Get the base name of the file path
        file_name = os.path.basename(self.file)
        return file_name



        