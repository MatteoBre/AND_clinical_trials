import unittest
from test.common_functions.common_functions_test import TestCommonFunctions
from test.dataframe.calculate_attributes_test import TestCalculateAttributes


def create_suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestCommonFunctions))
    test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestCalculateAttributes))
    return test_suite


if __name__ == '__main__':
    suite = create_suite()
    runner = unittest.TextTestRunner()
    runner.run(suite)
