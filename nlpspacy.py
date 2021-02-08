import json
import re

import dateutil
import spacy
from spacy.lang.en import English as english
from knowledge_base import *

parser = english()
nlp = spacy.load("en_core_web_lg")


# for token in doc:
#     print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
#           token.shape_, token.is_alpha, token.is_stop)

def extract_info(question, message, kb):
    doc = nlp(message)
    stations = json.load(open('train_codes.json'))
    results = {}
    # print(doc)
    # true = re.compile(r'\b(?i)(true|yes|yeah|yh|correct)\b')
    true = r'.*(yes|correct|true|yeah|yh).*'
    false = r'.*(no|wrong|false|nah|nay).*'
    # time = r'^([0-1][0-9]|[2][0-3]):([0-5][0-9])$'
    time = re.compile(r'^(([01]\d|2[0-3]):([0-5]\d)|24:00)$')
    timeAM = r'/((1[0-2]|0?[1-9]):([0-5][0-9]) ?([AaPp][Mm]))/'

    # Extract return
    for ent in doc:
        ent = str(ent).lower()
        x = re.search(true, ent)
        y = re.search(false, ent)
        if ent in {'return', 'returns'}:
            results['return'] = 'true'
        if 'come back' in str(doc):
            results['return'] = 'true'
        if 'go back' in str(doc):
            results['return'] = 'true'
        if x:
            results['return'] = 'true'
        if ent in {'single', 'singles'}:
            results['return'] = 'false'
        if y:
            results['return'] = 'false'

    # Extract locations
    locations = []
    for ent in doc.ents:
        if ent.label_ == 'GPE':
            locations.append(str(ent[0]))
            results['location'] = locations
        else:
            for i in stations:
                # print(ent.text)
                if ent.text == i:
                    locations.append(i)
                    results['location'] = locations

    # minutes = []
    # times = []
    # for ent in doc.ents:
    #     print(ent.label_)
    #     if ent.text.isdigit():
    #         minutes.append(ent.text)
    #
    # if len(minutes) > 0:
    #     results['minutes'] = minutes

    minutes = []
    dates = []
    times = []
    integers = []
    for ent in doc.ents:
        if ent.label_ == 'CARDINAL':
            integers.append(ent.text)
            continue
        # Minutes
        if ent.text.isdigit():
            minutes.append(ent.text)

        # Dates
        if ent.label_ == 'DATE':
            date = dateutil.parser.parse(ent.text)
            date = str(date.day).zfill(2) + str(date.month).zfill(2) + (str(date.year)[2:])
            dates.append(date)

        # Times
        if ent.label_ == 'TIME':
            date = dateutil.parser.parse(ent.text)
            times.append(str(date.hour).zfill(2) + str(date.minute).zfill(2))

    if time.search(str(message)):
        date = dateutil.parser.parse(str(message))
        times.append(str(date.hour).zfill(2) + str(date.minute).zfill(2))

    if len(minutes) > 0:
        results['minutes'] = minutes
    if len(dates) > 0:
        results['dates'] = dates
    if len(times) > 0:
        results['times'] = times

    results['integers'] = integers

    print(results)

    if question['question'] == 'origin':
        print("origin")
        kb.knowledge['origin'] = results['location'][0]
    elif question['question'] == 'destination':
        print("destination")
        kb.knowledge['destination'] = results['location'][0]
    elif question['question'] == 'delayStation':
        print("delayStation")
        kb.knowledge['delayStation'] = results['location'][0]

    if question['question'] == 'return':
        print("return")
        kb.knowledge['return'] = results['return']

    if question['question'] == 'departDate':
        print("departDate")
        kb.knowledge['departDate'] = results['date']
        # kb['departDate'] = results['date']
    elif question['question'] == 'returnDate':
        print("returnDate")
        kb.knowledge['returnDate'] = results['date']
        # kb['returnDate'] == results['date']
    elif question['question'] == 'departTime':
        print("depart Time")
        kb.knowledge['returnDate'] = results['time']
        # kb['departTime'] = results['time']
    elif question['question'] == 'returnTime':
        print("return Time")
        kb.knowledge['returnTime'] = results['time']
        # kb['returnTime'] = results['time']
    elif question['question'] == 'arrivalTime':
        print("arrivalTime")
        kb.knowledge['arrivalTime'] = results['time']

        # kb['arrivalTime'] = results['time']

    if question['question'] == 'numberOfStops':
        print("numberOfStops")
        kb.knowledge['numberOfStops'] = results['integer']

        # kb['numberOfStops'] = results['integer']
    elif question['question'] == 'delayTime':
        print("delayTime")
        kb.knowledge['delayTime'] = results['integer']
        # kb['delayTime'] = results['integer']
    elif question['question'] == 'delayCode':
        print("delayCode")
        kb.knowledge['delayCode'] = results['integer']

        # kb['delayCode'] = results['integer']
