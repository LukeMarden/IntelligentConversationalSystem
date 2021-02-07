import re
from pprint import pprint
from spacy.matcher import Matcher

import dateutil
import spacy

# from DiscordUI import on_message

# sentence detection, tokenizer, POS model

# categorize --> regex
# greet = re.compile(r'\b(?i)(hello|hey|hi|yo)\b')
greeting = r'.*(hi|hello|yo|hey|).*'

# true = re.compile(r'\b(?i)(true|yes|yeah|yh|ya)\b')
# time = re.compile(r'^(([01]\d|2[0-3]):([0-5]\d)|24:00)$')

nlp = spacy.load("en_core_web_md")
ner = nlp.get_pipe('ner')

# message = nlp(text)

doc = nlp("hello Harry Apple is looking hey at buying U.K. startup for $1 billion at 3 o'clock on the 31/01/2021 from "
          "Anderston correct")
# doc = MESSAGE
# pprint([(X.text, X.label_) for X in doc.ents])

results = {}


for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
          token.shape_, token.is_alpha, token.is_stop)


# if greet.search(str(doc)):
#     results['greet'] = 'true'
#
# print(results)

# Trying regex method search...
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


# Locations
locations = []

for entity in doc.ents:
    if entity.label_ == 'GPE':
        locations.append(entity[0])
    if len(locations) > 0:
        results['location'] = locations


# Time

minutes = []
dates = []
times = []

for entity in doc.ents:
    if entity.text.isdigit():
        # Minutes
        minutes.append(entity.text)

print(minutes)
#
#     if entity.label_ == 'TIME':
#         date = dateutil.parse.parse(entity.text)
#         times.append(str(date.hour).zfill(2) + str(date.minute).zfill(2))
#
#     if entity.label_ == 'DATE':
#         try:
#             date = dateutil.parser.parse(entity.text)
#             date = str(date.day).zfill(2) + str(date.month).zfill(2) + (str(date.year)[2:])
#             dates.append(date)
#         except:
#             doc.emit_feedback('display received message', 'wrong_date')

# if time.search(str(doc)):
#     date = dateutil.parser.parse(str(doc))
#     times.append(str(date.hour).zfill(2) + str(date.minute).zfill(2))
#
# if len(minutes) > 0:
#     results['minutes'] = minutes
# if len(dates) > 0:
#     results['dates'] = dates
# if len(times) > 0:
#     results['times'] = times

# print(minutes)


for token in doc:
    token = str(token).lower()

    if token in {'predict', 'prediction', 'delay', 'delays'}:
        results['service'] = 'predict'

    if token in {'travel', 'travels', 'book', 'booking', 'bookings'}:
        results['service'] = 'book'

    if token in {'return', 'returns'}:
        results['return'] = 'true'

    if 'come back' in str(doc):
        results['return'] = 'true'

print(results)
