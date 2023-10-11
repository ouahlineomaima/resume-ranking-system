from pikepdf import Pdf, Name, PdfImage

pdf = Pdf.open("./data/English/resume1.pdf")
page = pdf.pages[0]
print(list(page.images.keys()))

raw = page.images['/X4']
pdf_image = PdfImage(raw)

print(page)

# How to know exactly that the extracted image is
# the applicant image and not background image or icon ?????





"""
import fitz
doc = fitz.open('./data/Frensh/resume1.pdf')

page = doc[0]

text = page.get_text()
links = page.get_links()

print(links)
"""