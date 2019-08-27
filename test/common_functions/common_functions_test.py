import unittest
from unittest import mock
import pandas as pd
from src.common_functions import common_functions


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

    @mock.patch('src.common_functions.common_functions.get_initials')
    def test_get_all_initials(self, mock_get_initials):
        mock_get_initials.return_value = "random"
        first_names = ["George", "Robert", "Steve"]
        all_initials = common_functions.get_all_initials(first_names)
        self.assertEqual(mock_get_initials.call_count, 3)
        self.assertEqual(all_initials, ["random", "random", "random"])

    def test_get_src_path(self):
        src_path = common_functions.get_src_path()
        self.assertEqual('src', src_path[-3:])

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
        arr = [19, 23, 45, 100, 807]
        max_num = max(arr)
        min_num = min(arr)
        normalized_result = common_functions.normalize(pd.Series(arr))
        normalized_expected = [(num - min_num)/(max_num - min_num) for num in arr]
        self.assertEquals(normalized_expected, normalized_result.tolist())

    def test_get_java_gateway_server(self):
        server = common_functions.get_java_gateway_server()
        self.assertNotEqual(server, None)
        server.close_server()

    def test_get_info_from_jds_sts(self):
        text = ['--- JD scores (x 1) and rank based on word count ---\r', 'JD129|Neoplasms\r',
                '1|0,0587849|JD129|Neoplasms\r', '2|0,0224318|JD101|Radiotherapy\r',
                '3|0,0185469|JD100|Radiology\r', '--- JD scores (x 1) and rank based on document count ---\r',
                'JD129|Neoplasms\r', '1|0,1117369|JD129|Neoplasms\r', '2|0,0441393|JD101|Radiotherapy\r',
                '3|0,0394280|JD100|Radiology\r', '--- Overall JD rank ---\r', 'JD129|Neoplasms|dc\r']
        text_result = common_functions.get_info_from_jds_sts(text)
        text_expected = [(0.0587849, 'Neoplasms'), (0.0224318, 'Radiotherapy'), (0.0185469, 'Radiology')]
        self.assertEqual(text_expected, text_result)

    def test_get_java_path(self):
        java_path = common_functions.get_java_path()
        open(java_path)

    def test_get_gensim_doc2vec_model(self):
        model = common_functions.get_gensim_doc2vec_model()
        self.assertNotEqual(None, model)


if __name__ == '__main__':
    unittest.main()
