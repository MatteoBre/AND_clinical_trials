# We need to get the last name, first name initial, first name, e-mail and organization
# Now let's do that for the PubMed articles
from ..articles.article import Article
from ..common_functions import common_functions
from datetime import datetime


def get_gold_standard_last_name(pm_id, gold_standard):
    index = gold_standard.index[gold_standard['PMID'] == int(pm_id)].tolist()[0]
    last_name = gold_standard.iloc[index]['LastName']
    return last_name.lower()


# I get the initial of the name from the gold standard
def get_gold_standard_initial(pm_id, gold_standard):
    index = gold_standard.index[gold_standard['PMID'] == int(pm_id)].tolist()[0]
    first_name = gold_standard.iloc[index]['FirstName']
    return first_name.lower()[0]


def get_all_name_parts(articles, gold_standard):

    last_names = []
    first_name_initials = []
    first_names = []

    for i in range(len(articles)):

        # I get the correct last_name and first initial
        correct_last_name = get_gold_standard_last_name(articles[i].article.MedlineCitation.PMID.text, gold_standard)
        correct_first_name_initial = get_gold_standard_initial(articles[i].article.MedlineCitation.PMID.text, gold_standard)

        author = articles[i].get_name(correct_last_name, correct_first_name_initial)

        if author is None:
            print('not found:', i)
            last_names.append(None)
            first_name_initials.append(None)
            first_names.append(None)
            continue

        ar_last_name, ar_first_name_initials, ar_first_name = Article.extrapolate_name(author)

        last_names.append(ar_last_name)
        first_name_initials.append(ar_first_name_initials)
        first_names.append(ar_first_name)

    return last_names, first_name_initials, first_names


def get_all_formatted_words(string):
    if string is None:
        return None
    arr = string.lower().strip().replace(",", " ").replace(";", " ").replace(".", " "). replace("-", " ").split(" ")
    arr = [word for word in arr if word is not None and word != ""]
    return arr


def get_all_organizations_locations(articles, last_names, initials, sample='standard'):
    if sample not in ['standard', 'spacy', 'stanford']:
        raise ValueError('sample can assume only these values: standard, spacy, stanford')
    organizations = []
    locations = []
    for i in range(len(articles)):
        organization_name = articles[i].get_organization_name(last_names[i], initials[i])
        organizations.append(organization_name)
        if sample == 'standard':
            locations.append(get_all_formatted_words(organization_name))
    if sample == 'spacy':
        organizations, locations = common_functions.get_organizations_locations_with_spacy(organizations)
    if sample == 'stanford':
        organizations, locations = common_functions.get_organizations_locations_with_stanford(organizations)
    return organizations, locations


def get_all_mails(articles, last_names, initials):
    return [articles[i].get_mail(last_names[i], initials[i]) for i in range(len(articles))]


def get_all_years(articles):
    return [int(ar.get_year() or datetime.now().year) for ar in articles]


def get_all_initials(first_names):
    return [common_functions.get_initials(first_name) for first_name in first_names]


def get_all_titles(articles):
    return [ar.get_title() for ar in articles]


def get_all_texts(articles):
    return [ar.get_text() for ar in articles]
