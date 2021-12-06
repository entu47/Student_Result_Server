import pdfkit
from PyPDF2 import PdfFileWriter, PdfFileReader
import os


def html_to_pdf(file, email, roll_no):
    pdfkit.from_string(file, "in.pdf")
    out = PdfFileWriter()
    file = PdfFileReader("in.pdf")
    num_of_pages = file.numPages
    for index in range(num_of_pages):
        page = file.getPage(index)
        out.addPage(page)

    password = generate_pass(email, roll_no)
    out.encrypt(password)
    with open("out.pdf", "wb") as f:
        out.write(f)

# Password is roll_no followed by characters of email before @


def generate_pass(email, roll_no):
    email_chars = email.split('@')
    password = str(roll_no) + email_chars[0]
    return password


def remove_resource():
    resource1 = "in.pdf"
    resource2 = "out.pdf"

# Parent Directory
    parent = ""

# Path
    path1 = os.path.join(parent, resource1)
    path2 = os.path.join(parent, resource2)
    os.remove(path1)
    os.remove(path2)
