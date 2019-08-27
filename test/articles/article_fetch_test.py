import unittest
from src.articles import article_fetch as ar_fetch


class TestArticleFetch(unittest.TestCase):
    def test_fetch_many_articles(self):
        result = ar_fetch.fetch_many_articles(['11762820'], True)
        self.assertNotEqual(result, None)


if __name__ == '__main__':
    unittest.main()
