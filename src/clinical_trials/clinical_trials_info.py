# We need to get the last name, first name initial, first name, e-mail and organization
# I start to get them for the clinical trials
from ..clinical_trials.clinical_trial import ClinicalTrial
from ..common_functions import common_functions
from datetime import datetime


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


def get_all_organization_names(clinical_trials, last_names, initials, sample='standard'):
    if sample not in ['standard', 'spacy', 'stanford']:
        raise ValueError('sample can assume only these values: standard, spacy, stanford')
    organizations = []
    for i in range(len(clinical_trials)):
        organization_name = clinical_trials[i].get_organization_name(last_names[i], initials[i])
        organizations.append(organization_name)
    if sample == 'spacy':
        organizations = common_functions.get_organizations_locations_with_spacy(organizations)
    if sample == 'stanford':
        organizations = common_functions.get_organizations_locations_with_stanford(organizations)
    return organizations


def get_all_mails(clinical_trials, last_names, initials):
    return [clinical_trials[i].get_mail(last_names[i], initials[i]) for i in range(len(clinical_trials))]


def get_all_years(clinical_trials):
    return [int(ct.get_year() or datetime.now().year) for ct in clinical_trials]


def get_all_initials(first_names):
    return [common_functions.get_initials(first_name) for first_name in first_names]


def get_all_titles(clinical_trials):
    return [ct.get_title() for ct in clinical_trials]


def get_all_texts(clinical_trials):
    return [ct.get_text() for ct in clinical_trials]


def get_all_countries_and_cities(clinical_trials):
    countries_and_cities = [ct.get_country_and_city() for ct in clinical_trials]
    return [c_c[0] for c_c in countries_and_cities], [c_c[1] for c_c in countries_and_cities]