import unittest
from dataframe import calculate_attributes


class TestCalculateAttributes(unittest.TestCase):

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
