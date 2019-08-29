from ..common_functions import common_functions
from datetime import datetime


class ClinicalTrialList(list):
    def __init__(self, ct_list):
        [self.append(ct) for ct in ct_list]

    def get_ct_by_id(self, ct_id):
        # I get the clinical trial from the list with the ct_id specified
        cts = [ct for ct in self if ct.clinical_trial is not None and
               ct.clinical_trial.id_info.nct_id.text == ct_id]
        ct = None if len(cts) == 0 else cts[0]

        if ct is None:
            print('clinical trial', ct_id, ' not found.')
        return ct

    def get_organization_names(self, last_names, initials, sample='standard'):
        # Here I get all the organization names for the clinical trials
        if sample not in ['standard', 'spacy', 'stanford']:
            raise ValueError('sample can assume only these values: standard, spacy, stanford')
        organizations = []
        for i in range(len(self)):
            organization_name = self[i].get_organization_name(last_names[i], initials[i])
            organizations.append(organization_name)
        if sample == 'spacy':
            organizations = common_functions.get_organizations_locations_with_spacy(organizations)[0]
        if sample == 'stanford':
            organizations = common_functions.get_organizations_locations_with_stanford(organizations)[0]
        return organizations

    def get_mails(self, last_names, initials):
        # I get all the mails in the clinical trials
        return [self[i].get_mail(last_names[i], initials[i]) for i in range(len(self))]

    def get_years(self):
        # I get all the years of publication for the clinical trials
        return [int(ct.get_year() or datetime.now().year) for ct in self]

    def get_countries_and_cities(self):
        # I get all the countries and cities for the clinical trials
        countries_and_cities = [ct.get_country_and_city() for ct in self]
        return [c_c[0] for c_c in countries_and_cities], [c_c[1] for c_c in countries_and_cities]
