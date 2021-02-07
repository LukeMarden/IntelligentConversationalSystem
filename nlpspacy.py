import re
from pprint import pprint
from spacy.lang.en import English as english

from spacy.matcher import Matcher
import json
import dateutil.parser
import spacy

parser = english()

# from DiscordUI import on_message

# sentence detection, tokenizer, POS model

# categorize --> regex
# greet = re.compile(r'\b(?i)(hello|hey|hi|yo)\b')

# true = re.compile(r'\b(?i)(true|yes|yeah|yh|ya)\b')
# time = re.compile(r'^(([01]\d|2[0-3]):([0-5]\d)|24:00)$')

nlp = spacy.load("en_core_web_md")
ner = nlp.get_pipe('ner')

# message = nlp(text)

doc = nlp(
    "Hello Harry Apple is looking at buying U.K. on the 4 of September 2015 startup Acle for $1 billion at on the "
    "31/01/2021 "
    "from "
    "Anderston correct Bagshot return 25/05/2021 in 55 minutes. It will take about 5 stops")
# doc = MESSAGE
pprint([(X.text, X.label_) for X in doc.ents])

results = {}

# for token in doc:
#     print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
#           token.shape_, token.is_alpha, token.is_stop)


# if greet.search(str(doc)):
#     results['greet'] = 'true'
#
# print(results)

# Trying regex method search...
greeting = r'.*(hi|hello|yo|hey|).*'


# greeting
def greet(txt):
    x = re.search(greeting, txt.text)
    if x:
        results['greet'] = 'true'
    else:
        results['greet'] = 'false'


greet(doc)

# responses
true = r'.*(yes|correct|true).*'


def trueAnswer(txt):
    x = re.search(true, txt.text)
    if x:
        results['answer'] = 'true'


trueAnswer(doc)

false = r'.*(no|wrong|false).*'


def falseAnswer(txt):
    x = re.search(false, txt.text)
    if x:
        results['answer'] = 'false'


stations = json.load(open('train_codes.json'))

# for i in stations:
#     print(i)

# Locations
locations = []

for entity in doc.ents:
    if entity.label_ == 'GPE':
        locations.append(str(entity[0]))
        results['location'] = locations
    else:
        for i in stations:
            if entity.text == i:
                locations.append(i)
                results['location'] = locations


# Time


extracted_entities = [(i.text, i.label_) for i in doc.ents]

relevant_labels = ["DATE", "CARDINAL"]

for relevant_label in relevant_labels:
    print("Extracted for label: " + relevant_label)
    for entity, label in extracted_entities:
        if label == relevant_label:
            print("- " + entity)

# time = re.compile(r'^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]|(?:Jan|Mar|May|Jul|Aug|Oct|Dec)))\1|(?:(?:29|30)(\/|-|\.)('
#                   r'?:0?[1,3-9]|1[0-2]|(?:Jan|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))\2))(?:(?:1[6-9]|[2-9]\d)?\d{'
#                   r'2})$|^(?:29(\/|-|\.)(?:0?2|(?:Feb))\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|('
#                   r'?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9]|('
#                   r'?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep))|(?:1[0-2]|(?:Oct|Nov|Dec)))\4(?:(?:1[6-9]|[2-9]\d)?\d{'
#                   r'2}|24:00)$')
# minutes = []
# dates = []
# times = []
# for entity in doc.ents:
#     if entity.text.isdigit():
#         minutes.append(entity.text)
#         results['minutes'] = minutes
#
#     if entity.label_ == 'DATE':
#         date = dateutil.parser.parse(entity.text)
#         date = str(date.day).zfill(2) + str(date.month).zfill(2) + (str(date.year)[2:])
#         dates.append(date)
#         results['dates'] = dates
#     #
#
#     if entity.label_ == 'TIME':
#         date = dateutil.parser.parse(entity.text)
#         times.append(str(date.hour).zfill(2) + str(date.minute).zfill(2))
#
#
# if len(times) > 0:
#     results['times'] = times
#
# print(minutes)

for token in doc:
    token = str(token).lower()

    if token in {'return', 'returns'}:
        results['return'] = 'true'

    if 'come back' in str(doc):
        results['return'] = 'true'

print(results)
