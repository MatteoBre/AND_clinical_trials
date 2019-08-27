import unittest
from test.test_functions import test_functions


class TestArticleList(unittest.TestCase):
    articles = test_functions.get_test_articles(['12195305', '11754709', '11759784', '11845650'])
    last_names = ['garrett', 'avants', 'massoudi', 'nock']
    initials = ['k', 's', 'b', 'm']

    def test_get_ar_by_id(self):
        article = self.articles.get_ar_by_id('11845650')
        self.assertEqual(article.article.PMID.text, '11845650')

    def test_get_organizations_locations(self):
        organizations, locations = self.articles.get_organizations_locations(self.last_names, self.initials, 'spacy')
        self.assertEqual(organizations, [['Department of Diagnostic Imaging', "St. Jude Children's Research Hospital"],
                                         None, None, ['Department of Psychology', 'Yale University', 'CT']])
        self.assertEqual(locations, [['Memphis', 'USA'], None, None, ['New Haven', 'USA']])

    def test_get_mails(self):
        mails = self.articles.get_mails(self.last_names, self.initials)
        self.assertEqual(mails, [None, None, None, 'matthew.nock@yale.edu'])

    def test_get_years(self):
        years = self.articles.get_years()
        self.assertEqual(years, [2002, 2002, 2001, 2002])


if __name__ == '__main__':
    unittest.main()
