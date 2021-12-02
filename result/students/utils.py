import pdfkit
from PyPDF2 import PdfFileWriter, PdfFileReader
import os


def html_to_pdf(file, email, roll_no):
    pdfkit.from_string(file, "in.pdf")
    out = PdfFileWriter()
    file = PdfFileReader("in.pdf")
    num = file.numPages
    for idx in range(num):
        page = file.getPage(idx)
        out.addPage(page)
    enc = email.split('@')
    password = str(roll_no) + enc[0]
    out.encrypt(password)
    with open("out.pdf", "wb") as f:
        out.write(f)


def remove_resource():
    d1 = "in.pdf"
    d2 = "out.pdf"

# Parent Directory
    parent1 = ""

# Path
    path1 = os.path.join(parent1, d1)
    path2 = os.path.join(parent1, d2)
    os.remove(path1)
    os.remove(path2)
