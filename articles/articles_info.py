# We need to get the last name, first name initial, first name, e-mail and organization
# Now let's do that for the PubMed articles
from articles.article import Article


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


def get_all_organizations(articles, last_names, initials):
    organizations = []
    for i in range(len(articles)):
        organization_name = articles[i].get_organization_name(last_names[i], initials[i])
        organizations.append(organization_name)
    return organizations


def get_all_mails(articles, last_names, initials):
    mails = []
    for i in range(len(articles)):
        mail = articles[i].get_mail(last_names[i], initials[i])
        mails.append(mail)
    return mails
