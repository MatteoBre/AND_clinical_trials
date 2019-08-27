import unittest
import pandas as pd
import numpy
import src.csv_data.csv as csv_data


# csv_data.correct_data(gold_standard)


class TestCSV(unittest.TestCase):

    def test_numerical_answers(self):
        gold_standard = pd.read_csv('src/ClinicalPmidsALL.csv', encoding='ISO-8859-1', sep=';')
        csv_data.numerical_answers(gold_standard)
        common_answers = gold_standard['CommonAnswer'].values
        for answer in common_answers:
            if type(answer) != numpy.int64:
                self.assertTrue(False)

    def test_correct_data(self):
        gold_standard = pd.read_csv('src/ClinicalPmidsALL.csv', encoding='ISO-8859-1', sep=';')
        csv_data.numerical_answers(gold_standard)
        csv_data.correct_data(gold_standard)
        for i in range(len(gold_standard)):
            check_sum = gold_standard.loc[i, '1'] + gold_standard.loc[i, '2'] + gold_standard.loc[i, '3']
            if gold_standard.loc[i, 'CommonAnswer'] != 0 and gold_standard.loc[i, 'CommonAnswer'] != 1:
                self.assertTrue(False)
            if check_sum >= 2 and gold_standard.loc[i, 'CommonAnswer'] == 0:
                self.assertTrue(False)
            if check_sum <= 1 and gold_standard.loc[i, 'CommonAnswer'] == 1:
                self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
