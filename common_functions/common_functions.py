from sklearn.preprocessing import StandardScaler
from nltk.tag import StanfordNERTagger
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
from nltk.tokenize import word_tokenize
from itertools import groupby
import os
from java_libraries import java_server


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

    java_path = get_java_path()+"\\java.exe"
    os.environ['JAVAHOME'] = java_path

    return tagger


def get_organizations_locations_with_stanford(organizations):
    tagger = get_stanford_ner_tagger()
    stanford_organizations = []
    stanford_locations = []

    for org in organizations:

        if org is None:
            stanford_organizations.append(None)
            stanford_locations.append(None)
            continue

        tokenized_text = word_tokenize(org)
        classified_text = tagger.tag(tokenized_text)

        possible_organizations = []
        possible_locations = []
        for tag, chunk in groupby(classified_text, lambda x: x[1]):
            if tag == "ORGANIZATION":
                org_name = " ".join(w for w, t in chunk)
                possible_organizations.append(org_name)
            if tag == "LOCATION":
                loc_name = " ".join(w for w, t in chunk)
                possible_locations.append(loc_name)
        stanford_organizations.append(possible_organizations)
        stanford_locations.append(possible_locations)

    return stanford_organizations, stanford_locations


def get_organizations_locations_with_spacy(organizations):
    nlp = en_core_web_sm.load()
    spacy_organizations = []
    spacy_locations = []

    for org in organizations:
        if org is None:
            spacy_organizations.append(None)
            spacy_locations.append(None)
            continue
        doc = nlp(org.replace(';', ','))
        spacy_organizations.append([X.text for X in doc.ents if X.label_ == 'ORG'])
        spacy_locations.append([X.text for X in doc.ents if X.label_ == 'GPE'])

    return spacy_organizations, spacy_locations


def normalize(values):
    normalized = (values - values.min()) / (values.max() - values.min())
    return normalized


def get_java_gateway_server():
    server = java_server.JavaServer()
    return server


def get_info_from_jds_sts(texts):
    results = []
    for i in range(1, len(texts)):
        if texts[i][0] == '-':
            break
        try:
            strings = texts[i].split("|")
            percentage = float(strings[1].replace(',', '.'))
            term = strings[-1][:-1]
            results.append((percentage, term))
        except ValueError:
            pass

    return results


def get_java_path():
    path = open("java_path.txt", "r")
    return path.read()
