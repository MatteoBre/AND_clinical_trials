from nltk.tag import StanfordNERTagger
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
