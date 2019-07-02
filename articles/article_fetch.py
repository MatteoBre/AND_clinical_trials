import requests
from bs4 import BeautifulSoup
from articles.article import Article


# I get all the articles from an article list
def article_doms(fetch_result):
    root = BeautifulSoup(fetch_result, "xml")
    doms_list = []

    for child in root.findAll():
        if child.name == "PubmedArticle":
            doms_list.append(Article(child))

    return doms_list


# Download a list of full articles from PubMed
def fetch_articles(id_list):
    id_str_list = ''

    # I create the list of ID in a string, so that it can be usable in the HTTP request
    for el in id_list:
        id_str_list += el + ','

    # I set up the HTTP request
    url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=' + id_str_list + '&rettype=xml'

    # I return the result of the request
    return requests.get(url)


def fetch_local_articles(id_list):
    articles = []
    for ar_id in id_list:
        location = 'pubmed_articles_xml/'+ar_id+'.xml'

        try:
            article = BeautifulSoup(open(location, "r", encoding="utf8").read(), 'xml')
        except FileNotFoundError:
            continue

        articles.append(Article(article))
    return articles


def fetch_many_articles(id_list, local=False):  # To use only for >300 articles
    if local is True:
        return fetch_local_articles(id_list)
    begin = 0
    end = len(id_list)
    responses = []
    result = []

    # I make requests of 300 cinical trials each
    while begin < end:
        responses.append(fetch_articles(id_list[begin:(begin + 300)]))
        begin += 300
    # I check if all the requests has the desired output
    for response in responses:
        if response.status_code != 200:
            raise Exception('A response doesn\'t have 200 as status code, so something has gone wrong when making the '
                            'requests to https://eutils.ncbi.nlm.nih.gov')

    # I add all the articles into a single array
    for response in responses:
        for article in article_doms(response.content):  # I get all the articles for every response
            result.append(article)
    return result
