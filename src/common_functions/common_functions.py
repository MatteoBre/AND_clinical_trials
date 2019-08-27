from nltk.tag import StanfordNERTagger
import en_core_web_sm
from nltk.tokenize import word_tokenize
from itertools import groupby
import os
from ..java_libraries import java_server
from gensim.models.doc2vec import Doc2Vec


def get_initials(name):
    name = name.replace('-', ' ')
    name = name.replace("'", ' ')
    strings = name.split(' ')
    initials = [string[0] for string in strings if string != '']
    return ''.join(initials).strip()


def get_all_initials(first_names):
    return [get_initials(first_name) for first_name in first_names]


def get_src_path():
    file_path = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.abspath(os.path.join(file_path, os.pardir))
    return src_path


def get_stanford_ner_tagger():
    src_path = get_src_path()

    stanford_classifier = src_path + '/stanfordNER/classifiers/english.all.3class.distsim.crf.ser.gz'
    stanford_ner_path = src_path + '/stanfordNER/stanford-ner.jar'

    # Creating Tagger Object
    tagger = StanfordNERTagger(stanford_classifier, stanford_ner_path, encoding='utf-8')

    java_path = get_java_path()
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
    if os.name == 'nt':
        src_parent_path = os.path.abspath(os.path.join(get_src_path(), os.pardir))
        path = open(src_parent_path + "/java_path.txt", "r")
        return path.read()
    return 'java'


def get_gensim_doc2vec_model():
    model_path = get_src_path() + "/gensim/enwiki_dbow/doc2vec.bin"
    return Doc2Vec.load(model_path)
