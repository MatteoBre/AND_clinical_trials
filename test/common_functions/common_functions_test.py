import unittest
from common_functions import common_functions


class TestCommonFunctions(unittest.TestCase):

    @staticmethod
    def get_test_organizations_locations():
        organizations = ['University of Milan, Italy, University of Zurich, Zurich', 'University of Oxford',
                         'bottle', None]
        organizations_expected = [['University of Milan', 'University of Zurich'], ['University of Oxford'], [], None]
        locations_expected = [['Italy', 'Zurich'], [], [], None]
        return organizations, organizations_expected, locations_expected

    def test_get_initials_1(self):
        initials = common_functions.get_initials('George   george')
        self.assertEqual(initials, 'Gg')

    def test_get_initials_2(self):
        initials = common_functions.get_initials('george-george')
        self.assertEqual(initials, 'gg')

    def test_get_initials_3(self):
        initials = common_functions.get_initials('larry\'george')
        self.assertEqual(initials, 'lg')

    def test_get_stanford_ner_tagger(self):
        tagger = common_functions.get_stanford_ner_tagger()
        self.assertNotEqual(tagger, None)

    def test_get_organizations_locations_with_stanford(self):
        organizations, organizations_expected, locations_expected = self.get_test_organizations_locations()
        organizations_res, locations_res = common_functions.get_organizations_locations_with_stanford(organizations)
        self.assertEquals(organizations_expected, organizations_res)
        self.assertEquals(locations_expected, locations_res)

    def test_get_organizations_locations_with_spacy(self):
        organizations, organizations_expected, locations_expected = self.get_test_organizations_locations()
        organizations_res, locations_res = common_functions.get_organizations_locations_with_spacy(organizations)
        self.assertEquals(organizations_expected, organizations_res)
        self.assertEquals(locations_expected, locations_res)

    def test_normalize(self):
        pass

    def test_get_java_gateway_server(self):
        pass

    def test_get_info_from_jds_sts(self):
        pass

    def test_get_java_path(self):
        pass


if __name__ == '__main__':
    unittest.main()
