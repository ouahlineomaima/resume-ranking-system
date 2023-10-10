import PyPDF2

# Open the PDF file
with open('/data/English/resume1.pdf', 'rb') as pdf_file:
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    print(pdf_reader)
    """
    text = ""
    for page_num in range(pdf_reader.numPages):
        page = pdf_reader.getPage(page_num)
        text += page.extractText()
        """

# 'text' now contains the extracted text from the PDF
