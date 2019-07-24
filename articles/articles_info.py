# We need to get the last name, first name initial, first name, e-mail and organization
# Now let's do that for the PubMed articles
from articles.article import Article
from common_functions import common_functions
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
    mails = []
    for i in range(len(articles)):
        mail = articles[i].get_mail(last_names[i], initials[i])
        mails.append(mail)
    return mails


def get_all_years(articles):
    years = []
    for i in range(len(articles)):
        year = articles[i].get_year()
        if year is None:
            year = datetime.now().year
        years.append(int(year))
    return years


def get_all_initials(first_names):
    initials = []
    for i in range(len(first_names)):
        initials.append(common_functions.get_initials(first_names[i]))
    return initials


def get_all_titles(articles):
    titles = []
    for i in range(len(articles)):
        titles.append(articles[i].get_title())
    return titles


def get_all_texts(articles):
    texts = []
    for i in range(len(articles)):
        texts.append(articles[i].get_text())
    return texts
