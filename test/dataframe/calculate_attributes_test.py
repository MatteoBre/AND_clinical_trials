import unittest
from unittest import mock
from src.dataframe import calculate_attributes


class TestCalculateAttributes(unittest.TestCase):

    def test_get_arrays_equality(self):
        arr1 = [1, 10, 12, 100]
        arr2 = [1, 9, 12, 111]
        equalities = calculate_attributes.get_arrays_equality(arr1, arr2)
        array_result = [1, 0, 1, 0]
        self.assertEqual(equalities, array_result)

    def test_levenshtein(self):
        s1 = "string_number_one"
        s2 = "string_asdfgh_ron"
        levenshtein_result = calculate_attributes.levenshtein(s1, s2)
        self.assertEqual(levenshtein_result, 8)

    def test_get_string_arrays_similarity(self):
        arr1 = ["str1", "str2", "str3"]
        arr2 = ["", "str2", "tr345"]
        similarity_result = calculate_attributes.get_string_arrays_similarity(arr1, arr2)
        expected_result = [0, 1, 0.4]
        self.assertEqual(similarity_result, expected_result)

    def test_get_best_similarity(self):
        arr1 = ["str1", "str2", "str3"]
        arr2 = ["", "str", "tr34567890"]
        best_similarity = calculate_attributes.get_best_similarity(arr1, arr2)
        best_expected = 0.75
        self.assertEqual(best_similarity, best_expected)

    def test_get_org_similarity_1(self):
        org_similarity = calculate_attributes.get_org_similarity("Organization", "Org", "standard", "standard")
        self.assertEqual(org_similarity, 0.25)

    @mock.patch('src.dataframe.calculate_attributes.get_best_similarity')
    def test_get_org_similarity_2(self, mock_best_similarity):
        mock_best_similarity.return_value = 0
        calculate_attributes.get_org_similarity(["Organization"], ["Org"], "spacy", "standard")
        mock_best_similarity.assert_called()

    @mock.patch('src.dataframe.calculate_attributes.get_best_similarity')
    def test_get_org_similarity_3(self, mock_best_similarity):
        mock_best_similarity.return_value = 0
        calculate_attributes.get_org_similarity(["Organization"], ["Org"], "standard", "stanford")
        mock_best_similarity.assert_called()

    @mock.patch('src.dataframe.calculate_attributes.get_best_similarity')
    def test_get_org_similarity_3(self, mock_best_similarity):
        mock_best_similarity.return_value = 0
        calculate_attributes.get_org_similarity("Organization", "Org", "standard", "standard")
        mock_best_similarity.assert_not_called()

    def test_both_contain(self):
        self.assertTrue(calculate_attributes.both_contain("phrase 1", "phrase 2", "phrase"))
        self.assertFalse(calculate_attributes.both_contain("phrase 1", "phrase 2", "word"))

    def test_check_same_organization_type(self):
        self.assertTrue(calculate_attributes.check_same_organization_type(
            "university of Ponte Tresa", "University of Puerto Rico"))
        self.assertTrue(calculate_attributes.check_same_organization_type(
            "school of Ponte Tresa", "SCHOOL of Puerto Rico"))
        self.assertTrue(calculate_attributes.check_same_organization_type(
            "hospital of Ponte Tresa", "HOSpiTal of Puerto Rico"))
        self.assertTrue(calculate_attributes.check_same_organization_type(
            "INSTITUTE of Ponte Tresa", "institute of Puerto Rico"))
        self.assertFalse(calculate_attributes.check_same_organization_type(
            "university of Ponte Tresa", "institute of Puerto Rico"))
        self.assertFalse(calculate_attributes.check_same_organization_type("yellow", "orange"))

    def test_get_type_equality(self):
        self.assertTrue(calculate_attributes.get_type_equality(
            ["university of X", "orange"], ["university of Y", "strawberry"]))
        self.assertFalse(calculate_attributes.get_type_equality(
            ["suitcase", "orange"], ["university of Y", "strawberry"]))

    @mock.patch('src.dataframe.calculate_attributes.get_type_equality')
    def test_get_org_type_equality_1(self, get_type_equality):
        get_type_equality.return_value = 0
        calculate_attributes.get_org_type_equality("s1", "s2", "standard", "standard")
        get_type_equality.assert_not_called()

    @mock.patch('src.dataframe.calculate_attributes.get_type_equality')
    def test_get_org_type_equality_2(self, get_type_equality):
        get_type_equality.return_value = 0
        calculate_attributes.get_org_type_equality(["s1"], "s2", "spacy", "standard")
        get_type_equality.assert_called_with(["s1"], ["s2"])

    @mock.patch('src.dataframe.calculate_attributes.get_type_equality')
    def test_get_org_type_equality_3(self, get_type_equality):
        get_type_equality.return_value = 0
        calculate_attributes.get_org_type_equality("s1", ["s2"], "standard", "stanford")
        get_type_equality.assert_called_with(["s1"], ["s2"])

    @mock.patch('src.dataframe.calculate_attributes.get_type_equality')
    def test_get_org_type_equality_4(self, get_type_equality):
        get_type_equality.return_value = 0
        calculate_attributes.get_org_type_equality(["s1"], ["s2"], "stanford", "stanford")
        get_type_equality.assert_called_with(["s1"], ["s2"])

    def test_get_organization_similarities_and_type_equalities_1(self):
        try:
            calculate_attributes.get_organization_similarities_and_type_equalities(
                [], [], "wrong_name", "wrong_name2")
            self.assertTrue(False)
        except ValueError:
            pass















    def test_calculate_max_similarity_1(self):
        max_similarity = calculate_attributes.calculate_max_similarity(1)
        self.assertEqual(max_similarity, 1)

    def test_calculate_max_similarity_2(self):
        max_similarity = calculate_attributes.calculate_max_similarity(4)
        expected_similarity = (4/1)**2 + (4/2)**2 + (4/3)**2 + (4/4)**2
        self.assertEqual(max_similarity, expected_similarity)

    def test_get_jds_sts_ranking_similarities(self):
        pass


if __name__ == '__main__':
    unittest.main()
