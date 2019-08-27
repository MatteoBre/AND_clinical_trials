import unittest
from test.test_functions import test_functions
from src.clinical_trials.clinical_trial import ClinicalTrial


class TestClinicalTrial(unittest.TestCase):
    clinical_trial = test_functions.get_test_clinical_trials(['NCT02730130'])[0]
    last_name = 'barker'
    initial = 'c'
    text = 'The purpose of this study is to find out what effects, good and/or bad, pembrolizumab has on\n      ' \
           'the patient and areas of cancer in their body that did not receive radiation therapy.'

    def test_extrapolate_name_parts(self):
        last_name, first_name_initial, first_name = ClinicalTrial.extrapolate_name_parts('Christopher Barker, MD')
        self.assertEqual(last_name, 'barker')
        self.assertEqual(first_name_initial, 'c')
        self.assertEqual(first_name, 'christopher')

    def test_get_organization_name(self):
        organization = self.clinical_trial.get_organization_name(self.last_name, self.initial)
        self.assertEqual(organization, 'Memorial Sloan Kettering Cancer Center')

    def test_get_mail(self):
        clinical_trial = test_functions.get_test_clinical_trials(['NCT00070109'])[0]
        last_name = 'baruchel'
        initial = 's'
        email = clinical_trial.get_mail(last_name, initial)
        self.assertEqual(email, 'resultsreportingcoordinator@childrensoncologygroup.org')

    def test_get_all_name_tags(self):
        tags = self.clinical_trial.get_all_name_tags(self.last_name, self.initial)
        self.assertEqual(tags[0].last_name.text, 'Christopher Barker, MD')

    def test_get_name(self):
        name = self.clinical_trial.get_name(self.last_name, self.initial)
        self.assertEqual(name.text, 'Christopher Barker, MD')

    def test_get_year(self):
        year = self.clinical_trial.get_year()
        self.assertEqual(int(year), 2016)

    def test_get_title(self):
        title = self.clinical_trial.get_title()
        self.assertEqual(title, 'Study to Assess the Efficacy of Pembrolizumab Plus Radiotherapy in Metastatic '
                                'Triple Negative Breast Cancer Patients')

    def test_get_country_and_city(self):
        countries, cities = self.clinical_trial.get_country_and_city()
        self.assertEqual(countries, ['United States', 'United States', 'United States', 'United States',
                                     'United States', 'United States', 'United States'])
        self.assertEqual(cities, ['Los Angeles', 'Basking Ridge', 'Middletown', 'Commack', 'Harrison', 'New York',
                                  'Rockville Centre'])

    def test_get_text(self):
        text = self.clinical_trial.get_text(False, False)
        self.assertEqual(text[0], self.text)

    def test_get_all_texts(self):
        texts = self.clinical_trial.get_all_texts()
        self.assertEqual(texts, self.text + ' ' + self.clinical_trial.get_title())


if __name__ == '__main__':
    unittest.main()
