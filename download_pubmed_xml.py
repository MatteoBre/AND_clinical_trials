import src.articles.article_fetch as article_fetch
import src.clinical_trials.clinical_trial_fetch as ct_fetch
import src.csv_data.csv as csv_data

import pandas as pd
import codecs
import os

# I get the gold standard
gold_standard = pd.read_csv('src/ClinicalPmidsALL.csv', encoding = 'ISO-8859-1', sep = ';')

# Now I change the common answer from string to numerical
csv_data.numerical_answers(gold_standard)

# Let's correct data on csv (common answer sometimes is not correct)
csv_data.correct_data(gold_standard)

# I get all the clinical trials ID and I get the articles in xml
Clinical_trials = ct_fetch.get_xml_doms(gold_standard['CT'].tolist())

# I get all the PMID and I get the articles in xml
PubMed_id_string = list(map(str, gold_standard['PMID'].tolist())) # I get the PMID as list of strings
PubMed_articles = article_fetch.fetch_many_articles(PubMed_id_string) # It takes time to fetch the articles

if not os.path.exists('src/pubmed_articles_xml'):
    os.makedirs('src/pubmed_articles_xml')

for i in range(len(PubMed_articles)):
    file = codecs.open('src/pubmed_articles_xml/' + PubMed_articles[i].article.PMID.text + '.xml', 'w', 'utf-8')
    file.write(str(PubMed_articles[i].article))
    file.close()
