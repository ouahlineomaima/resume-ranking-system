import spacy
import json
import random
from spacy.language import Language
from spacy.training import Example


@Language.factory("mon_reconnaisseur_de_cv")
def create_mon_reconnaisseur_de_cv(nlp, name):
    return CustomComponent(nlp)


class CustomComponent:
    name = "mon_reconnaisseur_de_cv"

    def __init__(self, nlp):
        self.labels = []
        self.nlp = nlp

    def add_label(self, label):
        self.labels.append(label)

def load_data(file):
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def train_spacy(TRAIN_DATA, iterations, labels):
    nlp = spacy.blank("fr")
    # Add the custom pipeline to the model
    ner = nlp.add_pipe("mon_reconnaisseur_de_cv")
    #  Add custom labels
    for label in labels:
        ner.add_label(label)

    # Disable other pipelines
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "mon_reconnaisseur_de_cv"]
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()
        for itn in range(iterations):
            print("Starting iteration " + str(itn))
            random.shuffle(TRAIN_DATA)
            losses = {}
            examples = []
            for text, annotations in TRAIN_DATA:
                example = Example.from_dict(nlp.make_doc(text), annotations)
                examples.append(example)
            nlp.update(examples, losses=losses, drop=0.2)
            print(losses)
    return nlp

# Load the data and split it into training data and test data
labels = [
        "EDUCATION",
        "EXPERIENCE",
        "SKILL",
        "PROJECT_NAME",
        "ACTIVITY",
        "LANGUAGE",
        "TOOL",
        "PROGRAMMING_LANGUAGE",
        "CERTIFICATION",
        "SOFT_SKILL",
        "ADDRESS",
        "EMAIL",
        "PHONE_NUMBER",
        "COLLEGE_NAME",
        "DURATION",
        "COMPANY_NAME",
        "NAME",
        "EDUCATION_PART",
        "EXPERIENCE_PART",
        "PROJECT_PART",
        "ACTIVITY_PART",
        "PROGRAMMING_LANGUAGE_PART",
        "SKILL_PART",
        "SOFT_SKILL_PART"
    ]

ROW_DATA = load_data('data/Training data/annotations.json')
random.shuffle(ROW_DATA)
TRAIN_DATA = ROW_DATA[:int(len(ROW_DATA) * 0.8)]
TEST_DATA = ROW_DATA[int(len(ROW_DATA) * 0.8):]
TRAIN_TEXT_DATA = [text for text, annotation in TRAIN_DATA]
TRAIN_TEXT = ' '.join(TRAIN_TEXT_DATA)

trained = train_spacy(TRAIN_DATA, 20, labels)

doc = trained(TRAIN_TEXT)
print(TRAIN_TEXT)
print("*********************************************")
for ent in doc.ents:
    print(ent.text, ent.label_)






