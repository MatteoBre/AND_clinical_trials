import unittest
from test.test_functions import test_functions
from src.articles.article import Article


class TestArticle(unittest.TestCase):
    article = test_functions.get_test_articles(['12432318'])[0]
    last_name = 'wray'
    initial = 'c'
    text = 'Severe burn injury results in profound metabolic derangements. Recently, we have shown that vitamin D metabolism is disturbed after burn injury. Vitamin D is essential for calcium and phosphorus homeostasis and skeletal bone integrity. The role of vitamin D on magnesium homeostasis is not well understood. The purpose of this study was to assess the effects of vitamin D deficiency on serum electrolytes. Forty-one pediatric burn patients with a mean (+/- SEM) total body surface area burn of 53.1 +/- 2.9% and full-thickness injury of 44.2 +/- 4.1% were studied from July 1996 to December 2000. The mean age of the patients was 6.5 +/- 0.8 years. Patients were studied for 6 weeks after admission to the hospital. Blood samples were obtained weekly for serum 25-hydroxycholecalciferol (25D), 1,25-dihydroxycholecalciferol (1,25D), and daily for calcium, magnesium, and phosphorus. Total intravenous (IV) replacement of calcium, magnesium, and phosphorus was also quantitated retrospectively. Bivariate and multivariate correlational analysis was used for statistical comparison. For the study duration, multivariate analysis demonstrated a positive correlation between 25D and serum calcium (r =.47, P <.05) and 1,25D and calcium (r =.27, P <.05). Overall, calcium had a positive correlation with phosphorus and a negative correlation with IV calcium replacement (ie, patients with lower calcium received more IV replacement). During the initial week of hospitalization (week 0), decreased 25D (mean 11.6 ng/ml; normal range 15-57 ng/ml) and 1,25D (mean 13.9 pg/ml; normal range 15-75 pg/ml) did not correlate with any other measured variable. In week 1, 1,25D (mean 15.2 ng/ml) had a positive correlation (r =.410, P <.05) with calcium (mean 7.70 mg/dl). Hypovitaminosis D observed in burn injury correlates with serum calcium and phosphorus abnormalities. Early after injury (<1 week) there was no observed correlation between vitamin D and other variables possibly because of the effects of burn shock. After 1 week, vitamin D appears to significantly effect phosphorus homeostasis. The relationship between vitamin D and magnesium is not well established. These results may indicate a role for vitamin D replacement therapy during the initial phase of burn resuscitation.'

    def test_get_affiliation_tag(self):
        affiliation_result = self.article.get_affiliation_tag(self.last_name, self.initial).text
        expected_affiliation = 'Shriners Hospitals for Children, Cincinnati, Ohio 45229, USA.'
        self.assertEqual(affiliation_result, expected_affiliation)

    def test_extrapolate_name(self):
        author_tag = self.article.get_author_tag(self.last_name, self.initial)
        last_name, first_name_initial, first_name = Article.extrapolate_name(author_tag)
        self.assertEqual(last_name, 'wray')
        self.assertEqual(first_name_initial, 'c')
        self.assertEqual(first_name, 'curtis j')

    def test_get_author_tag(self):
        author_tag_result = self.article.get_author_tag(self.last_name, self.initial)
        self.assertEqual(author_tag_result.LastName.text.lower(), self.last_name)
        self.assertEqual(author_tag_result.ForeName.text.lower()[0], self.initial)

    def test_get_organization_name(self):
        organization_name = self.article.get_organization_name(self.last_name, self.initial)
        self.assertEqual(organization_name, 'Shriners Hospitals for Children, Cincinnati, Ohio 45229, USA.')

    def test_get_mail(self):
        article = test_functions.get_test_articles(['11845650'])[0]
        last_name = 'nock'
        initial = 'm'
        mail_result = article.get_mail(last_name, initial)
        expected_mail = 'matthew.nock@yale.edu'
        self.assertEqual(mail_result, expected_mail)

    def test_get_year(self):
        year = self.article.get_year()
        self.assertEqual(int(year), 2002)

    def test_get_title(self):
        title = self.article.get_title()
        self.assertEqual(title, 'The 2002 Moyer Award. Metabolic effects of vitamin D on serum calcium, magnesium, '
                                'and phosphorus in pediatric burn patients.')

    def test_get_text(self):
        text = self.article.get_text(False, False)
        self.assertEqual(text[0], self.text)

    def test_get_all_texts(self):
        texts = self.article.get_all_texts()
        self.assertEqual(texts, self.text + ' ' + self.article.get_title())


if __name__ == '__main__':
    unittest.main()
