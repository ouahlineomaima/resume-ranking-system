from pikepdf import Pdf, Name, PdfImage  # used for extracting images only
import cv2
import numpy as np
import fitz  # used for text extraction


# Text extraction
document = fitz.open('data/Frensh/resume4.pdf')
page = document[0]
text = page.get_text()
# save the text in a file precise UTF-8 encoding
with open('data/Frensh/resume4.txt', 'w', encoding='utf-8') as f:
    f.write(text)


# face detection function
def detect_face(page):
    if page.images:
        # Load the Haar Cascade Classifier for face detection
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

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




