import unittest
from test.test_functions import test_functions


class TestClinicalTrialList(unittest.TestCase):
    clinical_trials = test_functions.get_test_clinical_trials(['NCT00070109', 'NCT00120744', 'NCT00120796',
                                                               'NCT02730130'])
    last_names = ['baruchel', 'freedman', 'mbaye', 'barker']
    initials = ['s', 's', 'p', 'c']

    def test_get_ct_by_id(self):
        clinical_trial = self.clinical_trials.get_ct_by_id('NCT00070109')
        self.assertEqual(clinical_trial.clinical_trial.id_info.nct_id.text, 'NCT00070109')

    def test_get_organization_names(self):
        organizations = self.clinical_trials.get_organization_names(self.last_names, self.initials, 'spacy')
        self.assertEqual(organizations, [["Children's Oncology Group"], ['The Hospital for Sick Children'], [], []])

    def test_get_mails(self):
        mails = self.clinical_trials.get_mails(self.last_names, self.initials)
        self.assertEqual(mails, ['resultsreportingcoordinator@childrensoncologygroup.org', None, None, None])

    def test_get_years(self):
        years = self.clinical_trials.get_years()
        self.assertEqual(years, [2003, 2005, 2005, 2016])

    def test_get_countries_and_cities(self):
        countries, cities = self.clinical_trials.get_countries_and_cities()
        self.assertEqual(countries, [['United States', 'United States', 'United States', 'United States',
                                      'United States', 'United States', 'United States', 'United States',
                                      'United States', 'United States', 'United States', 'Canada', 'Canada',
                                      'Canada'], [], ['Senegal'], ['United States', 'United States', 'United States',
                                                                   'United States', 'United States', 'United States',
                                                                   'United States']])
        self.assertEqual(cities, [['Little Rock', 'Madera', 'Chicago', 'Buffalo', 'New York', 'New York',
                                   'Winston-Salem', 'Columbus', 'Memphis', 'Burlington', 'Seattle', 'Hamilton',
                                   'Toronto', 'Montreal'], [], ['Dakar'], ['Los Angeles', 'Basking Ridge', 'Middletown',
                                                                           'Commack', 'Harrison', 'New York',
                                                                           'Rockville Centre']])


if __name__ == '__main__':
    unittest.main()
