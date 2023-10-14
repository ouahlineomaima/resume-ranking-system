import spacy  # used for NLP
from spacy import displacy
import json


labels = ["PROFILE", "EDUCATION", "EXPERIENCE", "SKILL", "PROJECT_NAME", "ACTIVITY",
          "LANGUAGE", "TOOL", "PROGRAMMING_LANGUAGE",
          "CERTIFICATION", "ADDRESS", "EMAIL", "PHONE_NUMBER", "SOFT_SKILL", "COLLEGE_NAME", "DURATION", "COMPANY_NAME"]
nlp = spacy.blank("fr")

ner = nlp.create_pipe("ner")
for label in labels:
    ner.add_label(label)

nlp.add_pipe(ner, name="custom_resume_ner")

nlp.to_disk("custom_resume_ner")


