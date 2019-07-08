from nltk.tag import StanfordNERTagger
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
from nltk.tokenize import word_tokenize
from itertools import groupby
import os


def get_numerical_month(month):
    months = dict({'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8,
                   'September': 9, 'October': 10, 'November': 11, 'December': 12})
    return months.get(month)


def get_initials(name):
    name = name.replace('-', ' ')
    name = name.replace("'", ' ')
    strings = name.split(' ')
    initials = [string[0] for string in strings if string != '']
    return ''.join(initials).strip()


def get_stanford_ner_tagger():

    stanford_classifier = 'stanfordNER/classifiers/english.all.3class.distsim.crf.ser.gz'
    stanford_ner_path = 'stanfordNER/stanford-ner.jar'

    # Creating Tagger Object
    tagger = StanfordNERTagger(stanford_classifier, stanford_ner_path, encoding='utf-8')

    java_path = "C:/Program Files/Java/jdk-11.0.1/bin/java.exe"
    os.environ['JAVAHOME'] = java_path

    return tagger


def get_organizations_with_stanford(organizations):
    tagger = get_stanford_ner_tagger()
    stanford_organizations = []

    for org in organizations:

        if org is None:
            stanford_organizations.append(None)
            continue

        tokenized_text = word_tokenize(org)
        classified_text = tagger.tag(tokenized_text)

        possible_organizations = []
        for tag, chunk in groupby(classified_text, lambda x: x[1]):
            if tag == "ORGANIZATION":
                org_name = " ".join(w for w, t in chunk)
                possible_organizations.append(org_name)

        stanford_organizations.append(possible_organizations)

    return stanford_organizations


def get_organizations_with_spacy(organizations):
    nlp = en_core_web_sm.load()
    spacy_organizations = []

    for org in organizations:
        if org is None:
            spacy_organizations.append(None)
            continue
        doc = nlp(org.replace(';', ','))
        spacy_organizations.append([X.text for X in doc.ents if X.label_ == 'ORG'])

    return spacy_organizations
