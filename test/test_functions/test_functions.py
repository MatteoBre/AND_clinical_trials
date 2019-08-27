from src.clinical_trials.clinical_trial import ClinicalTrial
from src.lists.clinical_trial_list import ClinicalTrialList
from src.lists.article_list import ArticleList
from src.articles.article import Article
from bs4 import BeautifulSoup


def get_test_clinical_trials(clinical_trial_ids):
    clinical_trials = [ClinicalTrial(BeautifulSoup(open('test/test_clinical_trials/' + ct_id + '.xml', "r",
                                                        encoding="utf8").read(), "xml"))
                       for ct_id in clinical_trial_ids]
    clinical_trial_list = ClinicalTrialList(clinical_trials)
    return clinical_trial_list


def get_test_articles(article_ids):
    articles = [Article(BeautifulSoup(open('test/test_articles/' + ar_id + '.xml', "r",
                                           encoding="utf8").read(), "xml"))
                for ar_id in article_ids]
    article_list = ArticleList(articles)
    return article_list
