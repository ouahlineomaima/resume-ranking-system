from pymongo import MongoClient
import base64
import schedule
import time
from ResumeParser import parse_resume
import io
import fitz

# MongoDB connection
client = MongoClient("mongodb+srv://talentscout559:o4Ucq5WLgrkKRW1m@cluster0.nb2bd7a.mongodb.net/TalentScout?retryWrites=true&w=majority")
db = client["TalentScout"]
applicants_collection = db["applicants"]
recruitment_collection = db["recruitments"]  # Assuming you have a collection named 'recruitment'

# Define constants
APPLICATION_STATUS_NOT_CHECKED = "NotChecked"
APPLICATION_STATUS_CHECKED = "Checked"


def process_applicants():
    try:
        # Get applicants with applicationStatus = APPLICATION_STATUS_NOT_CHECKED
        applicants = applicants_collection.find({"applicationStatus": APPLICATION_STATUS_NOT_CHECKED})

        for applicant in applicants:
            resume_base64 = applicant.get("resume", "")
            recruitment_id = applicant.get("idRecruitment")

            # Fetch the recruitment document
            recruitment = recruitment_collection.find_one({"_id": recruitment_id})

            if recruitment:
                descriptions = recruitment.get("descriptions")
                # Convert base64 resume to text
                resume_text = base64_to_text(resume_base64)
                # Process the resume text and description
                firstname, lastname, email, score, phone = parse_resume(resume_text, descriptions)
                # Update applicant with new data
                update_applicant(applicant["_id"], firstname, lastname, email, score, phone)

    except Exception as e:
        print(f"Error processing applicants: {e}")


def base64_to_text(base64_data):
    try:
        # Decode base64
        decoded_data = base64.b64decode(base64_data)
        f = open('file.pdf', 'wb')
        f.write(decoded_data)
        f.close()

        # If the document is a PDF, extract text using PyMuPDF (Fitz)
        pdf_text = extract_text_from_pdf('file.pdf')
        return pdf_text# Assuming PDF text is in UTF-8
    except Exception as e:
        print(f"Error decoding base64: {str(e)}")
        return ""


def extract_text_from_pdf(file_path):
    try:
        doc = fitz.open(file_path)
        text = ""
        for page_number in range(doc.page_count):
            page = doc[page_number]
            text += page.get_text("text")
        text = " ".join(text.split('\n'))
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""


def update_applicant(applicant_id, firstname=None, lastname=None, email=None, score=None, phone=None):
    update_data = {"applicationStatus": APPLICATION_STATUS_CHECKED}

    if firstname is not None:
        update_data["firstname"] = firstname
    if lastname is not None:
        update_data["lastname"] = lastname
    if email is not None:
        update_data["email"] = email
    if score is not None:
        update_data["score"] = score
    if phone is not None:
        update_data["phone"] = phone

    try:
        applicants_collection.update_one({"_id": applicant_id}, {"$set": update_data})
    except Exception as e:
        print(f"Error updating applicant {applicant_id}: {str(e)}")


# Schedule the job to run every day at 6:00 AM
schedule.every().day.at("07:00").do(process_applicants)

while True:
    schedule.run_pending()
    time.sleep(1)
