import unittest
from unittest import mock
from src.dataframe import calculate_attributes
from src.common_functions import common_functions
from test.test_functions import test_functions
import os
import numpy


class TestCalculateAttributes(unittest.TestCase):
    clinical_trials = test_functions.get_test_clinical_trials(['NCT00120731', 'NCT02730130'])
    articles = test_functions.get_test_articles(['12078146', '12143843'])
    jds_1 = [(0.3, 'term_1'), (0.2, 'term_2'), (0.1, 'term_3')]
    jds_2 = [(0.5, 'term_1'), (0.4, 'term_3'), (0.2, 'term_4')]

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

    def test_get_organization_similarities_and_type_equalities_2(self):
        similarity_results, type_equality_results = calculate_attributes.\
            get_organization_similarities_and_type_equalities(['university of edinburgh', 'university of X', None],
                                                              ['university of edinburgh', 'University of YYYYYY', 'K'],
                                                              "standard", "standard")
        expected_similarity_results = [1, 0.65, 0]
        expected_type_equality_results = [1, 1, 0]
        self.assertEqual(expected_similarity_results, similarity_results)
        self.assertEqual(expected_type_equality_results, type_equality_results)

    def test_year_differences(self):
        years_1 = [1997, 2011]
        years_2 = [2019, 2001]
        year_differences_results = calculate_attributes.get_year_differences(years_1, years_2)
        expected_year_differences = [22, 10]
        self.assertEqual(year_differences_results, expected_year_differences)

    def test_get_last_name_lengths(self):
        last_names = ["Lee", "Smith"]
        last_name_lengths_results = calculate_attributes.get_last_name_lengths(last_names)
        expected_last_name_lengths = [3, 5]
        self.assertEqual(last_name_lengths_results, expected_last_name_lengths)

    def test_fetch_namespace_sizes(self):
        author_names = ["Smith+R[author]", "Lee+Y[author]"]
        response = calculate_attributes.fetch_namespace_sizes(author_names)
        self.assertEqual(response.status_code, 200)

    def test_get_namespace_ambiguities(self):
        last_names = ["Smith", "Lee"]
        initials = ["R", "A"]
        results = calculate_attributes.get_namespace_ambiguities(last_names, initials)
        self.assertEqual(type(results[0]), int)

    def test_get_formatted(self):
        countries = ["Italy", "Switzerland", "Uk", "USA", "United Kingdom"]
        formatted_result = calculate_attributes.get_formatted(countries)
        expected_result = ["italy", "switzerland", "united kingdom", "united states", "united kingdom"]
        self.assertEqual(formatted_result, expected_result)

    @mock.patch('src.dataframe.calculate_attributes.get_formatted')
    def test_get_location_equality_1(self, get_formatted):
        self.assertEqual(0, calculate_attributes.get_location_equality([], ['italy']))
        self.assertEqual(0, calculate_attributes.get_location_equality(['italy'], []))
        self.assertEqual(0, calculate_attributes.get_location_equality(None, ['italy']))
        self.assertEqual(0, calculate_attributes.get_location_equality(['italy'], None))
        get_formatted.assert_not_called()

    def test_get_location_equality_2(self):
        locations_1 = ['ohio', 'united states']
        locations_2 = ['basel', 'switzerland']
        self.assertEqual(calculate_attributes.get_location_equality(locations_1, locations_2), 0)

    def test_get_location_equality_3(self):
        locations_1 = ['switzerland', 'united states']
        locations_2 = ['basel', 'switzerland']
        self.assertEqual(calculate_attributes.get_location_equality(locations_1, locations_2), 1)

    def test_get_location_equalities(self):
        ct_countries = [['Italy'], ['UK']]
        ct_cities = [['Rome'], ['Edinburgh']]
        ar_locations = [['Italy', 'Florence'], ['edinburgh']]
        country_equalities_result, city_equalities_result = calculate_attributes.\
            get_location_equalities(ct_countries, ct_cities, ar_locations)
        expected_country_equalities = [1, 1]
        expected_city_equalities = [0, 1]
        self.assertEqual(expected_country_equalities, country_equalities_result)
        self.assertEqual(expected_city_equalities, city_equalities_result)

    def test_get_all_jds(self):
        jds, sts = calculate_attributes.get_all_jds_sts(self.clinical_trials, self.articles)
        self.assertEqual(len(jds[0][0]), len(jds[0][1]))
        self.assertEqual(len(sts[0][0]), len(sts[0][1]))
        # Structure of single jd -> (0.002, name)
        self.assertEqual(type(jds[0][0][0][0]), float)
        self.assertEqual(type(jds[0][0][0][1]), str)

    def test_basic_jds_sts_similarity(self):
        similarity = calculate_attributes.get_jds_sts_basic_similarities(self.jds_1, self.jds_2)
        # I round them to the 10th decimal in order to avoid float errors
        self.assertEqual(round(similarity,10), round(2/3, 10))

    def test_confidence_jds_sts_similarity(self):
        similarity = calculate_attributes.get_jds_sts_confidence_similarities(self.jds_1, self.jds_2)
        # 0.3 + 0.1 = 0.4 confidence on shared terms
        # 0.5 + 0.4 + 0.2 = 1.1 max possible confidence (jds_2)
        self.assertEqual(round(similarity, 10), round(0.4/1.1, 10))

    def test_ranking_jds_sts_similarity(self):
        similarity = calculate_attributes.get_jds_sts_ranking_similarities(self.jds_1, self.jds_2)
        # term_1 score = 1*1 = 1
        # term_3 score = 1/3 * 1/2 = 1/6
        max_similarity = 1 + 1/4 + 1/9
        self.assertEqual(round(similarity, 10), round((1 + 1/3 * 1/2)/max_similarity, 10))

    def test_confidence_ranking_jds_sts_similarity(self):
        similarity = calculate_attributes.get_jds_sts_confidence_ranking_similarities(self.jds_1, self.jds_2)
        # max confidence = (0.5*0.5)/(1*1) + (0.4*0.4)/(2*2) + (0.2*0.2)/(3*3) = 0.29 + 0.04/9 (jds_2)
        # term_1 similarity = 0.3 * 1/1 * 1/1 = 0.3
        # term_3 similarity = 0.1 * 1/3 * 1/2 = 1/60
        max_confidence = 0.29 + 0.04/9
        self.assertEqual(round(similarity, 10), round((0.3 + 1/60)/max_confidence, 10))

    def test_create_required_folders(self):
        calculate_attributes.create_required_folders()
        self.assertEqual(os.path.isdir(common_functions.get_src_path()+"/tmp_txt_ct"), True)
        self.assertEqual(os.path.isdir(common_functions.get_src_path() + "/tmp_txt_ar"), True)

    def test_get_oger_similarity(self):
        oger_1 = ['word_1', 'word_2', 'word_3', 'word_4']
        oger_2 = ['word_1', 'word_3', 'word_4']
        oger_similarity_result = calculate_attributes.get_oger_similarity(oger_1, oger_2)
        expected_result = 0.75
        self.assertEqual(expected_result, oger_similarity_result)

    def test_get_oger_similarities(self):
        oger_similarities_result = calculate_attributes.get_oger_similarities(self.clinical_trials, self.articles)
        expected_oger_similarities = [15/26, 0]
        self.assertEqual(expected_oger_similarities, oger_similarities_result)

    def test_get_doc2vec_vectors(self):
        ct_vectors, ar_vectors = calculate_attributes.get_doc2vec_vectors(self.clinical_trials, self.articles)
        self.assertEqual(len(ct_vectors), len(ar_vectors))
        self.assertEqual(len(ct_vectors[0]), len(ar_vectors[0]))
        self.assertEqual(type(ct_vectors[0][0]), numpy.float32)

    def test_get_vectors_similarity_1(self):
        vector_1 = numpy.array([1.0, 0.0])
        vector_2 = numpy.array([0.0, 1.0])
        vector_similarity_result = calculate_attributes.get_vectors_similarity(vector_1, vector_2)
        # cos(pi/2) = 0
        self.assertEqual(vector_similarity_result, 0.0)

    def test_get_vectors_similarity_2(self):
        vector_1 = numpy.array([0.0, 1.0])
        vector_2 = numpy.array([0.0, 1.0])
        vector_similarity_result = calculate_attributes.get_vectors_similarity(vector_1, vector_2)
        # cos(0) = 1
        self.assertEqual(vector_similarity_result, 1.0)

    def test_get_doc2vec_vectors_similarities(self):
        vector_similarities_result = calculate_attributes.get_doc2vec_vectors_similarities(self.clinical_trials, self.articles)
        for similarity in vector_similarities_result:
            self.assertLessEqual(similarity, 1.0)
            self.assertGreaterEqual(similarity, -1.0)


if __name__ == '__main__':
    unittest.main()
