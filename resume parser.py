# used for extracting images only
# How to know exactly that the extracted image is
# the applicant image and not background image or icon ?????
from pikepdf import Pdf, Name, PdfImage
import cv2
import numpy as np

# Loading the resume
pdf = Pdf.open("./data/English/resume2.pdf")
# Extracting the first page
page = pdf.pages[0]

if page.images:
    # Load the Haar Cascade Classifier for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_default.xml')

    for key in page.images.keys():
        # Extract the raw image
        raw = page.images[key]

        # Convert it to pdf image
        pdf_image = PdfImage(raw)

        # Convert the pdf_image to a Pillow image
        image_data = pdf_image.as_pil_image()

        # Convert the Pillow image to an OpenCV format for face detection
        image = cv2.cvtColor(np.array(image_data), cv2.COLOR_BGR2RGB)

        # Detect faces in the image by adjusting scaleFactor and minNeighbors
        # to acheive the maximum possibile sensitivity and the minimum possible of True Negative
        faces = face_cascade.detectMultiScale(image, scaleFactor=1.30, minNeighbors=2)

        # If faces are detected, save the image as personal image
        if len(faces) > 0:
            pdf_image.extract_to(fileprefix='personal_image')





"""
# used for extracting the text
import fitz
doc = fitz.open('./data/Frensh/resume1.pdf')

page = doc[0]

text = page.get_text()
links = page.get_links()

print(links)
"""