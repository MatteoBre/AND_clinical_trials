import pandas as pd


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
