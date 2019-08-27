import unittest
from src.clinical_trials import clinical_trial_fetch as ct_fetch
from bs4 import BeautifulSoup


class TestClinicalTrialFetch(unittest.TestCase):
    def test_get_file_location(self):
        location = ct_fetch.get_file_location('NCT00120809.xml')
        self.assertEqual(location, 'src/AllPublicXML/NCT0012xxxx/NCT00120809.xml')

    def test_get_xml_dom_1(self):
        bs_xml = ct_fetch.get_xml_dom('NCT00120809.xml')
        self.assertEqual(type(bs_xml), BeautifulSoup)

    def test_get_xml_dom_2(self):
        # NCT00000000.xml does not exist
        bs_xml = ct_fetch.get_xml_dom('NCT00000000.xml')
        self.assertIsNone(bs_xml)

    def test_get_xml_doms(self):
        result = ct_fetch.get_xml_doms(['NCT00120809.xml', 'NCT00000000.xml'])
        self.assertEqual(len(result), 1)


if __name__ == '__main__':
    unittest.main()
