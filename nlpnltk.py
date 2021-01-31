import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import conlltags2tree, tree2conlltags
from pprint import pprint

# nltk.download('averaged_perceptron_tagger')

ex = 'European authorities fined Google a record $5.1 billion on Wednesday for abusing its power in the mobile phone market and ordered the company to alter its practices'


def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent


sent = preprocess(ex)
# print(sent)

pattern = 'NP: {<DT>?<JJ>*<NN>}'


cp = nltk.RegexpParser(pattern)
cs = cp.parse(sent)
# print(cs)


iob_tagged = tree2conlltags(cs)
pprint(iob_tagged)
