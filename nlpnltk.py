# import nltk
# from nltk.tokenize import word_tokenize
# from nltk.tag import pos_tag
# from nltk.chunk import conlltags2tree, tree2conlltags
# from pprint import pprint
#
# # nltk.download('averaged_perceptron_tagger')
#
# ex = 'European authorities fined Google a record $5.1 billion on Wednesday for abusing its power in the mobile phone market and ordered the company to alter its practices'
#
#
# def preprocess(sent):
#     sent = nltk.word_tokenize(sent)
#     sent = nltk.pos_tag(sent)
#     return sent
#
#
# sent = preprocess(ex)
# # print(sent)
#
# pattern = 'NP: {<DT>?<JJ>*<NN>}'
#
#
# cp = nltk.RegexpParser(pattern)
# cs = cp.parse(sent)
# # print(cs)
#
#
# iob_tagged = tree2conlltags(cs)
# pprint(iob_tagged)

import nltk
from nltk.tag.stanford import StanfordNERTagger

st = StanfordNERTagger('stanford-ner/all.3class.distsim.crf.ser.gz', 'stanford-ner/stanford-ner.jar')
text = "People, like Steve for example, have been a great influence in the Apple company."

for sent in nltk.sent_tokenize(text):
    tokens = nltk.tokenize.word_tokenize(sent)
    tags = st.tag(tokens)
    for tag in tags:
        if tag[1] == 'PERSON':
            print(tag)
