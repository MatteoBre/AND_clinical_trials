from ..common_functions import common_functions
from datetime import datetime


class ArticleList(list):
    def __init__(self, ar_list):
        [self.append(ar) for ar in ar_list]

    def get_ar_by_id(self, pmid):
        # I get the article with the specified pmid
        ars = [ar for ar in self if ar.article is not None and
               ar.article.MedlineCitation.PMID.text == pmid]
        ar = None if len(ars) == 0 else ars[0]

        if ar is None:
            print('article', pmid, ' not found.')
        return ar

    @staticmethod
    def get_all_formatted_words(string):
        if string is None:
            return None
        arr = string.lower().strip().replace(",", " ").replace(";", " ").replace(".", " ").replace("-", " ").split(" ")
        arr = [word for word in arr if word is not None and word != ""]
        return arr

    def get_organizations_locations(self, last_names, initials, sample='standard'):
        # I get the organizations and the locations for the articles
        if sample not in ['standard', 'spacy', 'stanford']:
            raise ValueError('sample can assume only these values: standard, spacy, stanford')
        organizations = []
        locations = []
        for i in range(len(self)):
            organization_name = self[i].get_organization_name(last_names[i], initials[i])
            organizations.append(organization_name)
            if sample == 'standard':
                locations.append(ArticleList.get_all_formatted_words(organization_name))
        if sample == 'spacy':
            organizations, locations = common_functions.get_organizations_locations_with_spacy(organizations)
        if sample == 'stanford':
            organizations, locations = common_functions.get_organizations_locations_with_stanford(organizations)
        return organizations, locations

    def get_mails(self, last_names, initials):
        # I get the mails for the articles
        return [self[i].get_mail(last_names[i], initials[i]) for i in range(len(self))]

    def get_years(self):
        # I get all the years of publication for the articles
        return [int(ar.get_year() or datetime.now().year) for ar in self]
