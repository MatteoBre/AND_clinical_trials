import src.articles.article_fetch as article_fetch
import src.clinical_trials.clinical_trial_fetch as ct_fetch
import src.csv_data.csv as csv_data
from src.dataframe import create_dataframe
from src.dataframe import calculate_attributes
from src.common_functions import common_functions
from src.lists.clinical_trial_list import ClinicalTrialList
from src.lists.article_list import ArticleList

import pandas as pd
import codecs

# I get the gold standard
gold_standard = pd.read_csv('src/ClinicalPmidsALL.csv', encoding='ISO-8859-1', sep=';')

# Now I change the common answer from string to numerical
csv_data.numerical_answers(gold_standard)

# Let's correct data on csv (common answer sometimes is not correct)
csv_data.correct_data(gold_standard)

# I get all the clinical trials ID and I get the articles in xml
clinical_trials = ClinicalTrialList(ct_fetch.get_xml_doms(gold_standard['CT'].tolist()))

# I get all the PMID and I get the articles in xml
pubMed_id_string = list(map(str, gold_standard['PMID'].tolist()))  # I get the PMID as list of strings
articles = ArticleList(article_fetch.fetch_many_articles(pubMed_id_string, local=True))

# standard, spacy or stanford
ct_org_sample = 'standard'
ar_org_sample = 'spacy'

clinical_trial_list, article_list, df, last_names, first_name_initials, ar_first_names, ct_first_names = \
    create_dataframe.get_lists_and_dataframe(gold_standard, clinical_trials, articles)

ar_organization_names, ar_locations = article_list.get_organizations_locations(last_names, first_name_initials,
                                                                               sample=ar_org_sample)
ct_countries, ct_cities = clinical_trial_list.get_countries_and_cities()

# I now calculate useful attributes for the classifiers
first_name_equalities = calculate_attributes.get_string_arrays_similarity(ct_first_names, ar_first_names)

organization_similarities, organization_type_equalities = calculate_attributes.\
    get_organization_similarities_and_type_equalities(clinical_trial_list.
                                                      get_organization_names(last_names, first_name_initials,
                                                                             sample=ct_org_sample),
                                                      ar_organization_names, ct_org_sample, ar_org_sample)

email_equalities = calculate_attributes.get_arrays_equality(clinical_trial_list.get_mails(last_names,
                                                                                          first_name_initials),
                                                            article_list.get_mails(last_names, first_name_initials))

year_differences = calculate_attributes.get_year_differences(clinical_trial_list.get_years(), article_list.get_years())
last_name_lengths = calculate_attributes.get_last_name_lengths(last_names)
initials_equality = calculate_attributes.get_arrays_equality(common_functions.get_all_initials(ct_first_names),
                                                             common_functions.get_all_initials(ar_first_names))
namespace_sizes = calculate_attributes.get_namespace_ambiguities(last_names, first_name_initials)
country_equalities, city_equalities = calculate_attributes.get_location_equalities(ct_countries, ct_cities,
                                                                                   ar_locations)
jds, sts = calculate_attributes.get_all_jds_sts(clinical_trial_list, article_list)
jds_similarities, sts_similarities = calculate_attributes.\
        get_all_jds_sts_similarities(jds, sts, 4, 1, 'confidence', 'ranking')

doc2vec_similarities = calculate_attributes.get_doc2vec_vectors_similarities(clinical_trial_list, article_list)
oger_similarities = calculate_attributes.get_oger_similarities(clinical_trial_list, article_list)

# Let's add the attributes to the data frame
df['first_name_equality'], df['organization_similarity'] = [first_name_equalities, organization_similarities]
df['email_equality'], df['year_difference'] = [email_equalities, year_differences]
df['last_name_length'], df['initials_equality'] = [last_name_lengths, initials_equality]
df['namespace_size'], df ['country_equality'] = [namespace_sizes, country_equalities]
df['city_equality'], df['organization_type_equality'] = [city_equalities, organization_type_equalities]
df['jds_similarity'], df['sts_similarity'] = [jds_similarities, sts_similarities]
df['vector_difference'], df['oger_similarity'] = [doc2vec_similarities, oger_similarities]

# Now let's normalize and/or standardize the attributes that need this
df['namespace_size'] = common_functions.normalize(df['namespace_size'])
df['last_name_length'] = common_functions.normalize(df['last_name_length'])
df['year_difference'] = common_functions.normalize(df['year_difference'])
df['vector_difference'] = common_functions.normalize(df['vector_difference'])
df['oger_similarity'] = common_functions.normalize(df['oger_similarity'])

# Writing the dataframe to file
csv = df.to_csv(index=False)

file = codecs.open("src\\dataframe.csv", "w", "utf-8")
file.write(csv)
file.close()

print('dataframe created successfully')
