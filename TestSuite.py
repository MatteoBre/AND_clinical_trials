import unittest
from test.common_functions.common_functions_test import TestCommonFunctions
from test.dataframe.calculate_attributes_test import TestCalculateAttributes
from test.articles.article_test import TestArticle
from test.articles.article_fetch_test import TestArticleFetch
from test.clinical_trials.clinical_trial_test import TestClinicalTrial
from test.clinical_trials.clinical_trial_fetch_test import TestClinicalTrialFetch
from test.lists.article_list_test import TestArticleList
from test.lists.clinical_trial_list_test import TestClinicalTrialList
from test.classifiers.classifiers_test import TestClassifiers
from test.csv_data.csv_test import TestCSV


def create_suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestCommonFunctions))
    test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestCalculateAttributes))
    test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestArticle))
    test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestArticleFetch))
    test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestArticleList))
    test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestClinicalTrial))
    test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestClinicalTrialFetch))
    test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestClinicalTrialList))
    test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestClassifiers))
    test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestCSV))
    return test_suite


if __name__ == '__main__':
    suite = create_suite()
    runner = unittest.TextTestRunner()
    runner.run(suite)
