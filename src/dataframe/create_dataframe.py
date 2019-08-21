import pandas as pd
import numpy as np
from ..lists.article_list import ArticleList
from ..lists.clinical_trial_list import ClinicalTrialList
from ..articles.article import Article
from ..clinical_trials.clinical_trial import ClinicalTrial


def get_article_by_id(article_list, pm_id):
    for i in range(len(article_list)):
        if article_list[i].article is not None and article_list[i].article.MedlineCitation.PMID.text == pm_id:
            return article_list[i]
    print('article', pm_id, ' not found.')
    return None


def get_clinical_trial_by_id(clinical_trials_list, ct):
    for i in range(len(clinical_trials_list)):
        if(clinical_trials_list[i].clinical_trial is not None and
                clinical_trials_list[i].clinical_trial.id_info.nct_id.text == ct):
            return clinical_trials_list[i]
    print('clinical trial', ct, ' not found.')
    return None


def get_base_dataframe(gold_standard, clinical_trials, articles):
    # Now let's map them
    pair_matrix = []
    for i in range(len(gold_standard)):
        row = gold_standard.iloc[i]
        article = get_article_by_id(articles, str(row['PMID']))
        clinical_trial = get_clinical_trial_by_id(clinical_trials, row['CT'])
        common_answer = gold_standard['CommonAnswer'][i]
        if article is not None and clinical_trial is not None:
            pair_matrix.append([clinical_trial, article, common_answer])
    df = pd.DataFrame(pair_matrix)
    df.columns = ['CT', 'PubMed', 'common_answer']
    return df


def get_lists_and_dataframe(gold_standard, clinical_trials, articles):
    pair_matrix = []

    for i in range(len(gold_standard)):
        row = gold_standard.iloc[i]
        article = articles.get_ar_by_id(str(row['PMID']))
        clinical_trial = clinical_trials.get_ct_by_id(row['CT'])
        common_answer = gold_standard['CommonAnswer'][i]

        if article is None or clinical_trial is None:
            continue

        last_name, first_initial, ar_first_name, ct_first_name = get_all_name_parts(clinical_trial, article,
                                                                                    gold_standard)

        if last_name is None or first_initial is None:
            print('required author not present either in the article ', row['PMID'],
                  ' or in the clinical trial ', row['CT'])
            continue

        if article is not None and clinical_trial is not None:
            pair_matrix.append([clinical_trial, article, common_answer, last_name,
                                first_initial, ar_first_name, ct_first_name])
    df = pd.DataFrame(np.array(pair_matrix)[:, 2].tolist())
    df.columns = ['common_answer']

    clinical_trial_list = ClinicalTrialList(np.array(pair_matrix)[:, 0].tolist())
    article_list = ArticleList(np.array(pair_matrix)[:, 1].tolist())
    last_names = np.array(pair_matrix)[:, 3].tolist()
    first_name_initials = np.array(pair_matrix)[:, 4].tolist()
    ar_first_names = np.array(pair_matrix)[:, 5].tolist()
    ct_first_names = np.array(pair_matrix)[:, 6].tolist()

    return clinical_trial_list, article_list, df, last_names, first_name_initials, ar_first_names, ct_first_names


def get_index(ct_id, pmid, gold_standard):
    indices_ct = gold_standard.index[gold_standard['CT'] == ct_id].tolist()
    indices_ar = gold_standard.index[gold_standard['PMID'] == int(pmid)].tolist()
    return np.intersect1d(indices_ct, indices_ar)[0]


# Here I get the NCT correspondency in the gold standard to the cell in my clinical_trials
def get_gold_standard_last_name(ct_id, pmid, gold_standard):
    index = get_index(ct_id, pmid, gold_standard)
    last_name = gold_standard.iloc[index]['LastName']
    return last_name.lower()


# I get the initial of the name from the gold standard
def get_gold_standard_initial(ct_id, pmid, gold_standard):
    index = get_index(ct_id, pmid, gold_standard)
    first_name = gold_standard.iloc[index]['FirstName']
    return first_name.lower()[0]


def extrapolate_last_name(name):
    name = name.split(',')[0].lower().replace('.', '').strip()
    name = name.split(' ')
    last_name = name[-1]
    return last_name.lower()


def get_all_name_parts(clinical_trial, article, gold_standard):
    # Let's get the correct last name from he gold standard
    correct_last_name = get_gold_standard_last_name(clinical_trial.clinical_trial.id_info.nct_id.text,
                                                    article.article.MedlineCitation.PMID.text,
                                                    gold_standard)
    correct_first_name_initial = get_gold_standard_initial(clinical_trial.clinical_trial.id_info.nct_id.text,
                                                           article.article.MedlineCitation.PMID.text,
                                                           gold_standard)

    ct_name = clinical_trial.get_name(correct_last_name, correct_first_name_initial)
    ar_name = article.get_name(correct_last_name, correct_first_name_initial)

    # If I can't get the right name, I save the node and I will delete it later (fortunately it happens only twice)
    if ct_name is None or ar_name is None:
        return None, None, None, None

    # I get the last name, first name initial and the first name
    last_name, first_name_initial, ct_first_name = ClinicalTrial.extrapolate_name_parts(ct_name.text)
    last_name, first_name_initial, ar_first_name = Article.extrapolate_name(ar_name)

    # I return the lists
    return last_name, first_name_initial, ar_first_name, ct_first_name
