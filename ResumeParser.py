import spacy


def parse_resume(text, descriptions):
    nlp_model = spacy.load('nlp_model')
    doc = nlp_model(text)
    # Create a dictionary to store entities grouped by label
    entities_by_label = {}

    for ent in doc.ents:
        label = ent.label_
        text = ent.text

        # Check if the label is already a key in the dictionary
        if label in entities_by_label:
            entities_by_label[label].append(text)
        else:
            entities_by_label[label] = [text]
    print(entities_by_label)
    # Extract the firstname and lastname from the entities_by_label dictionary
    firstname = entities_by_label.get("NAME", [""])[0].split(" ")[0]
    lastname = entities_by_label.get("NAME", [""])[0].split(" ")[1]
    # Extract the email from the entities_by_label dictionary
    email = entities_by_label.get("EMAIL", [""])[0]
    # Extract the score from the entities_by_label dictionary
    score = 0
    # Extract the technologies from the description
    technologies = descriptions["technologies"]
    # Extract the programming languages from the entities_by_label dictionary
    programming_languages = entities_by_label.get("PROGRAMMING_LANGUAGE", [])
    # Extract the tools from the entities_by_label dictionary
    tools = entities_by_label.get("TOOL", [])
    # Extract the skills from the entities_by_label dictionary
    skills = entities_by_label.get("SKILL", [])
    phones = entities_by_label.get("PHONE_NUMBER", [])
    phone = None
    if len(phones) > 0:
        phone = "|".join(phones)
    # Loop through the technologies
    for technology in technologies:
        # Check if the technology is in the programming_languages
        if technology in programming_languages:
            score += 1
        # Check if the technology is in the tools
        if technology in tools:
            score += 1
        # Check if the technology is in the skills
        if technology in skills:
            score += 1
    # return the firstname, lastname, email and score
    return firstname, lastname, email, score, phone

