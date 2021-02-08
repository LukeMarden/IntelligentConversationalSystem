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
            results['return'] = True
        if 'come back' in str(doc):
            results['return'] = True
        if 'go back' in str(doc):
            results['return'] = True
        if x:
            results['return'] = True
        if ent in {'single', 'singles'}:
            results['return'] = False
        if y:
            results['return'] = False

    # Extract locations
    locations = []
    for ent in doc:
        # if ent.label_ == 'GPE':
        #     locations.append(str(ent[0]))
        #     results['location'] = locations
        # else:
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
    for ent in doc:
        if ent.text == '0':
            integers.append(ent.text)
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

    if (question['question'] == 'origin') and ('location' in results):
        kb.knowledge['origin'] = results['location'][0]
        results = 1
    elif (question['question'] == 'destination') and ('location' in results):
        kb.knowledge['destination'] = results['location'][0]
        results = 1
    elif (question['question'] == 'delayStation') and ('location' in results):
        kb.knowledge['delayStation'] = results['location'][0]
        results = 1

    if (question['question'] == 'return') and ('return' in results):
        kb.knowledge['return'] = results['return']
        results = 1

    if (question['question'] == 'departDate') and ('dates' in results):
        kb.knowledge['departDate'] = results['dates'][0]
        results = 1
    elif (question['question'] == 'returnDate') and ('dates' in results):
        kb.knowledge['returnDate'] = results['dates'][0]
        results = 1
    elif (question['question'] == 'departTime') and ('times' in results):
        kb.knowledge['departTime'] = results['times'][0]
        results = 1
    elif (question['question'] == 'returnTime') and ('times' in results):
        kb.knowledge['returnTime'] = results['times'][0]
        results = 1
    elif (question['question'] == 'arrivalTime') and ('times' in results):
        kb.knowledge['arrivalTime'] = results['times'][0]
        results = 1

    if (question['question'] == 'numberOfStops') and ('integers' in results):
        kb.knowledge['numberOfStops'] = results['integers'][0]
        results = 1
    elif (question['question'] == 'delayTime') and ('integers' in results):
        kb.knowledge['delayTime'] = results['integers'][0]
        results = 1
    elif (question['question'] == 'delayCode') and ('integers' in results):
        kb.knowledge['delayCode'] = results['integers'][0]
        results = 1

    print(results)
    return results

