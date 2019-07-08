# We need to get the last name, first name initial, first name, e-mail and organization
# I start to get them for the clinical trials
from clinical_trials.clinical_trial import ClinicalTrial
from common_functions import common_functions
from nltk.tokenize import word_tokenize
from datetime import datetime
from itertools import groupby


# Here I get the NCT correspondency in the gold standard to the cell in my clinical_trials
def get_gold_standard_last_name(ct_id, gold_standard):
    index = gold_standard.index[gold_standard['CT'] == ct_id].tolist()[0]
    last_name = gold_standard.iloc[index]['LastName']
    return last_name.lower()


# I get the initial of the name from the gold standard
def get_gold_standard_initial(ct_id, gold_standard):
    index = gold_standard.index[gold_standard['CT'] == ct_id].tolist()[0]
    first_name = gold_standard.iloc[index]['FirstName']
    return first_name.lower()[0]


def extrapolate_last_name(name):
    name = name.split(',')[0].lower().replace('.', '').strip()
    name = name.split(' ')
    last_name = name[-1]
    return last_name.lower()


def get_all_name_parts(clinical_trials, gold_standard):
    last_names = []
    first_name_initials = []
    first_names = []

    for i in range(len(clinical_trials)):
        # Let's get the correct last name from he gold standard
        correct_last_name = get_gold_standard_last_name(clinical_trials[i].clinical_trial.id_info.nct_id.text,
                                                        gold_standard)
        correct_first_name_initial = get_gold_standard_initial(clinical_trials[i].clinical_trial.id_info.nct_id.text,
                                                               gold_standard)

        name = clinical_trials[i].get_name(correct_last_name, correct_first_name_initial)

        # If I can't get the right name, I save the node and I will delete it later (fortunately it happens only twice)
        if name is None:
            last_names.append(None)
            first_name_initials.append(None)
            first_names.append(None)
            continue

        # I get the last name, first name initial and the first name
        last_name_ct, first_name_initial_ct, first_name_ct = ClinicalTrial.extrapolate_name_parts(name.text)

        # I add them in their respective list
        last_names.append(last_name_ct)
        first_name_initials.append(first_name_initial_ct)
        first_names.append(first_name_ct)

    # I return the lists
    return last_names, first_name_initials, first_names


def get_all_organization_names(clinical_trials, last_names, initials):
    organizations = []
    # tagger = common_functions.get_stanford_ner_tagger()
    for i in range(len(clinical_trials)):
        organization_name = clinical_trials[i].get_organization_name(last_names[i], initials[i])
        '''
        # I apply the Stanford NER
        tokenized_text = word_tokenize(organization_name)
        classified_text = tagger.tag(tokenized_text)

        possible_organizations = []
        for tag, chunk in groupby(classified_text, lambda x: x[1]):
            if tag == "ORGANIZATION":
                org_name = ("%-12s" % tag, " ".join(w for w, t in chunk))
                possible_organizations.append(org_name)

        organizations.append(possible_organizations)
        '''
        organizations.append(organization_name)
    return organizations


def get_all_mails(clinical_trials, last_names, initials):
    mails = []
    for i in range(len(clinical_trials)):
        mail = clinical_trials[i].get_mail(last_names[i], initials[i])
        mails.append(mail)
    return mails


def get_all_years(clinical_trials):
    years = []
    for i in range(len(clinical_trials)):
        year = clinical_trials[i].get_year()
        if year is None:
            year = datetime.now().year
        years.append(int(year))
    return years


def get_all_initials(first_names):
    initials = []
    for i in range(len(first_names)):
        initials.append(common_functions.get_initials(first_names[i]))
    return initials


def get_all_countries(clinical_trials):
    countries = []
    for i in range(len(clinical_trials)):
        countries.append(clinical_trials[i].get_country())
    return countries
