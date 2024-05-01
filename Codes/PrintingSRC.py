import win32print
import win32api
import os


printer_name = ""

def print_pdf(pdf_path, printer_name=None):
    """
    This is the main function that prints pdf documents with the specified pdf path and printer name (not optional)

    :param pdf_path: The file path of the pdf file
    :param printer_name: The printer name to be used to print (set to none by defualt)
    """

    if not printer_name or printer_name == "":
        # Get the default printer
        printer_name = win32print.GetDefaultPrinter()

    # Create a handle for the printer
    printer_handle = win32print.OpenPrinter(printer_name)

    # Prepare printing information
    file_name = os.path.abspath(pdf_path)
    data = open(file_name, "rb").read()

    # Start a printing job
    job_info = {"pDatatype": "RAW"}
    job_id = win32print.StartDocPrinter(printer_handle, 1, (file_name, None, "RAW"))
    win32print.StartPagePrinter(printer_handle)

    # Send the data to the printer
    win32api.ShellExecute(0, "print", file_name, None, ".", 0)

    # End the printing job
    win32print.EndPagePrinter(printer_handle)
    win32print.EndDocPrinter(printer_handle)
    win32print.ClosePrinter(printer_handle)


def get_printer_name():
    """
    This is the function to get all printer name
    """
    # Get a list of all printers installed on the system
    printers = [printer[2] for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)]
    return printers

def setprinter(name):
    """
    setter to set printer
    """
    global printer_name 
    printer_name = name

def calltoprint(path, user):
    """
    Public function to be called to print

    :param path: path of file to be printed
    :param user: User printing the document
    :type path: String
    :type user: String
    """
    global printer_name
    pdf_file = path
    filename = os.path.basename(path)
    if printer_name == "":
        print("[PRINT JOB] No printer specified!")
        print("[PRINTER] Printer is set to default....")
        print(f"[PRINT JOB] Printing the document --> [{filename}]  FROM [{user}]")
        print_pdf(pdf_file, printer_name)

    else:
        print(f"[PRINT JOB] Printer specified!")
        print(f"[PRINTER] Printer is set to {printer_name}")
        print(f"[PRINT JOB] Printing the document --> {filename}  FROM [{user}]")
        print_pdf(pdf_file, printer_name)
    
# Call the function to get the printer names
#printer_names = get_printer_name()

# Print the list of printer names
#print(printer_names)


# Path to your PDF file
#pdf_file = ""


# Specify the printer name if needed, otherwise let it default to the default printer
#printer_name = "EPSON L3110 Series"\


# Call the function to print the PDF
#print_pdf(pdf_file, printer_name)
