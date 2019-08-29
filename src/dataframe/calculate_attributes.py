import requests
from bs4 import BeautifulSoup
from ..common_functions import common_functions
from ..oger.ctrl.router import Router, PipelineServer
import codecs
import math
import os


def get_arrays_equality(arr1, arr2):
    # This functions returns an array containing 0s and 1s
    # 0 when arr1[i] != arr2[i] and 1 if arr1[i] == arr2[i]
    equalities = []
    for i in range(len(arr1)):
        if arr1[i] is not None and arr2[i] is not None and arr1[i] == arr2[i]:
            equalities.append(1)
        else:
            equalities.append(0)
    return equalities


def levenshtein(s1, s2):
    # This is the levenshtein function
    # I use it to compare strings
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[
                             j + 1] + 1  # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1  # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def get_string_arrays_similarity(arr1, arr2):
    # The input is composed by 2 arrays of strings
    # I return an array containing numbers from 0.0 to 1.0
    # the number is obtained by comparing arr1[i] and arr2[i] using levenshtein
    similarities = []
    for i in range(len(arr1)):  # both arrays need to have the same length
        if arr1[i] is not None and arr2[i] is not None:
            max_length = len(max([arr1[i], arr2[i]], key=len))
            # the score is divided by the max length, so that it can have the 0.0 - 1.0 range
            score = levenshtein(arr1[i], arr2[i])/max_length
            # 0.0 means the strings are utterly different and 1.0 means the strings are identical
            similarities.append(1-score)
        else:
            similarities.append(0)
    return similarities


def get_best_similarity(arr1, arr2):
    # The input is composed by 2 arrays of strings
    # The result is the best possible score
    # The score is calculated using levenshtein, it has the 0.0 - 1.0 range
    max_score = 0
    for org1 in arr1:
        for org2 in arr2:
            max_length = len(max([org1, org2], key=len))
            # 0.0 means the strings are utterly different and 1.0 means the strings are identical
            score = 1-(levenshtein(org1, org2)/max_length)
            if score > max_score:
                max_score = score
    return max_score


def get_org_similarity(org1, org2, ct_sample, ar_sample):
    # We need to compare org1 and org2
    # Depending on the extraction method, org1/2 will be strings or arrays of strings
    # string if they use the standard extraction, arrays if they use spacy/stanford
    if ct_sample == 'standard' and ar_sample == 'standard':
        # If they are strings, I simply compare them using levenshtein
        max_length = len(max([org1, org2], key=len))
        return 1-(levenshtein(org1, org2)/max_length)
    # In case org1 or org2 are not spacy/stanford, I have to put the string org1/2 to an array
    # I do that to reuse the function "get_best_similarity" that needs 2 arrays of strings
    if ct_sample == 'standard' and ar_sample != 'standard':
        similarity = get_best_similarity([org1], org2)
    elif ct_sample != 'standard' and ar_sample == 'standard':
        similarity = get_best_similarity(org1, [org2])
    else:
        similarity = get_best_similarity(org1, org2)

    return similarity


def both_contain(phrase1, phrase2, word):
    # This function checks whether 2 strings contains a string called "word"
    return word in phrase1 and word in phrase2


def check_same_organization_type(phrase1, phrase2):
    # This function check if 2 strings contain one specific word
    # This word can be one of the following: university, hospital, school, institute
    phrase1 = phrase1.lower()
    phrase2 = phrase2.lower()

    university = both_contain(phrase1, phrase2, 'university')
    hospital = both_contain(phrase1, phrase2, 'hospital')
    school = both_contain(phrase1, phrase2, 'school')
    institute = both_contain(phrase1, phrase2, 'institute')

    # If only one criteria is matched, it returns True, False otherwise
    return university or hospital or school or institute


def get_type_equality(arr1, arr2):
    # I check whether a pair of words contains the same type of organization
    for org1 in arr1:
        for org2 in arr2:
            if check_same_organization_type(org1, org2):
                return 1
    return 0


def get_org_type_equality(org1, org2, ct_sample, ar_sample):
    # This function takes the organizations as input and, depending on the extraction method used,
    # it calls the right method to assess whether or not the type of the organization is the same
    if ct_sample == 'standard' and ar_sample == 'standard':
        # If both of them are single strings, I can call this function directly
        if check_same_organization_type(org1, org2):
            return 1
        else:
            return 0

    if ct_sample == 'standard' and ar_sample != 'standard':
        equality = get_type_equality([org1], org2)
    elif ct_sample != 'standard' and ar_sample == 'standard':
        equality = get_type_equality(org1, [org2])
    else:
        equality = get_type_equality(org1, org2)

    return equality


def get_organization_similarities_and_type_equalities(ct_org, ar_org, ct_sample, ar_sample):
    # This function returns all the organization similarities and the type equalities between 2 organizations
    # There are 3 ways to extract information from the string: 'standard', 'spacy', 'stanford'
    if ct_sample not in ['standard', 'spacy', 'stanford'] or ar_sample not in ['standard', 'spacy', 'stanford']:
        raise ValueError('ct_sample and ar_sample can assume only these values: standard, spacy, stanford')
    org_similarities = []
    org_type_equalities = []
    for i in range(len(ct_org)):
        if ct_org[i] is not None and ar_org[i] is not None:
            org_similarity = get_org_similarity(ct_org[i], ar_org[i], ct_sample, ar_sample)
            organization_type_equality = get_org_type_equality(ct_org[i], ar_org[i], ct_sample, ar_sample)
            org_similarities.append(org_similarity)
            if org_similarity >= 0.9:
                organization_type_equality = 1
            org_type_equalities.append(organization_type_equality)
        else:
            org_similarities.append(0)
            org_type_equalities.append(0)
    return org_similarities, org_type_equalities


def get_year_differences(ct_years, ar_years):
    # Here I return the list of the differences between the article and the clinical trials publication' years
    return [abs(ct_years[i] - ar_years[i]) for i in range(len(ct_years))]


def get_last_name_lengths(last_names):
    # Here I return a list with all the last name lengths
    return [len(last_name) for last_name in last_names]


def fetch_namespace_sizes(author_list):
    # Here I make a request to e-utils, I request the number of results found searching for each author in the list
    # using his last name and first name initial.
    author_str_list = ''
    # I create the list of ID in a string, so that it can be usable in the HTTP request
    for el in author_list:
        author_str_list += el

    # I set up the HTTP request
    url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term='\
          + author_str_list + '&rettype=xml'
    return requests.get(url)


def get_namespace_ambiguities(last_names, initials):
    # This function is used to get the namespace ambiguities
    # The ambiguity is found making requests to e-utils in order to get the number of results get for each author
    names_array = [last_names[i] + '+' + initials[i] + '[author]' for i in range(len(last_names))]

    begin = 0
    end = len(last_names)
    responses = []
    namespace_sizes = []

    while begin < end:
        responses.append(fetch_namespace_sizes(names_array[begin:(begin + 100)]))
        begin += 100

    # I check if all the requests has the desired output
    for response in responses:
        if response.status_code != 200:
            raise Exception('A response doesn\'t have 200 as status code, so something has gone wrong when making the '
                            'requests to https://eutils.ncbi.nlm.nih.gov')

    for response in responses:
        namespaces = BeautifulSoup(response.content, 'xml')
        # sometimes it splits into full author name, author and investigator (I only need the Author)
        term_sets = [termSet for termSet in namespaces.TranslationStack.findAll('TermSet')
                     if termSet.Term.text.split('[')[1][:-1].lower() == 'author']
        for termSet in term_sets:
            namespace_sizes.append(int(termSet.Count.text))
    return namespace_sizes


def get_formatted(arr):
    # some country names are different in clinical trials and in articles
    # In this function I uniform them and I get everything in lower case in order to be easily compared later
    arr = [word.lower() for word in arr]
    for i in range(len(arr)):
        if arr[i] == 'usa':
            arr[i] = 'united states'
        if arr[i] == 'uk':
            arr[i] = 'united kingdom'
    return arr


def get_location_equality(arr1, arr2):
    # I use this function to assess the equality of the arrays of countries and of cities
    if arr1 is None or arr2 is None or len(arr1) == 0 or len(arr2) == 0:
        return 0
    arr1 = get_formatted(arr1)
    arr2 = get_formatted(arr2)
    for word1 in arr1:
        for word2 in arr2:
            if word1 == word2:
                return 1
    return 0


def get_location_equalities(ct_countries, ct_cities, ar_locations):
    # Here I compare cities and countries and I get which pairs have the same cities and countries
    country_equalities = []
    city_equalities = []
    for i in range(len(ct_countries)):
        country_equality = get_location_equality(ct_countries[i], ar_locations[i])
        city_equality = get_location_equality(ct_cities[i], ar_locations[i])
        # If the cities have the same name, it might (not 100%, but high probability) be in the same country
        if city_equality == 1:
            country_equality = 1
        country_equalities.append(country_equality)
        city_equalities.append(city_equality)
    return country_equalities, city_equalities

# Here there are all the functions used to compare the jds and sts


def get_sum_jds_sts(jds):
    percentage_sum = 0
    for percentage, term in jds:
        percentage_sum += percentage
    return percentage_sum


def get_jds_sts_confidence_similarities(jds_1, jds_2):
    max_confidence_sum = max(get_sum_jds_sts(jds_1), get_sum_jds_sts(jds_2))
    confidence_difference_sum = 0
    for confidence_1, term_1 in jds_1:
        for confidence_2, term_2 in jds_2:
            if term_1 == term_2:
                current_max = max(confidence_1, confidence_2)
                absolute_difference = abs(confidence_2 - confidence_1)
                confidence_difference_sum += (current_max - absolute_difference)
    return confidence_difference_sum/max_confidence_sum


def get_jds_sts_basic_similarities(jds_1, jds_2):
    common_words = 0
    max_words = max(len(jds_1), len(jds_2))
    for confidence_1, term_1 in jds_1:
        for confidence_2, term_2 in jds_2:
            if confidence_1 == 0 or confidence_2 == 0:
                continue
            if term_1 == term_2:
                common_words += 1
    return common_words/max_words


def calculate_max_similarity(num):
    similarity = 0
    for i in range(num):
        similarity += (1/(i+1))**2
    return similarity


def get_jds_sts_ranking_similarities(jds_1, jds_2):
    similarity = 0
    max_similarity = calculate_max_similarity(len(jds_1))
    for i in range(len(jds_1)):
        for j in range(len(jds_2)):
            if jds_1[i][0] == 0 or jds_2[i][0] == 0:
                continue
            if jds_1[i][1] == jds_2[j][1]:
                similarity += (1/(i+1)) * (1/(j+1))
    return similarity/max_similarity


def get_sum_jds_sts_ranking(jds):
    confidence_sum = 0
    for i in range(len(jds)):
        confidence_sum += (jds[i][0]**2) / ((i+1)**2)
    return confidence_sum


def get_jds_sts_confidence_ranking_similarities(jds_1, jds_2):
    max_confidence_sum = max(get_sum_jds_sts_ranking(jds_1), get_sum_jds_sts_ranking(jds_2))
    confidence_difference_sum = 0
    for i in range(len(jds_1)):
        for j in range(len(jds_2)):
            if jds_1[i][1] == jds_2[j][1]:
                current_max = max(jds_1[i][0], jds_2[i][0])
                absolute_difference = abs(jds_1[i][0] - jds_2[i][0])
                confidence_similarity = current_max - absolute_difference
                score = confidence_similarity * (1/(i+1)) * (1/(j+1))
                confidence_difference_sum += score
    return confidence_difference_sum / max_confidence_sum


def get_all_jds_sts(clinical_trials, articles):
    # In this function I interrogate the java server to get the jds and sts
    server = common_functions.get_java_gateway_server()

    jds = []
    sts = []
    for i in range(len(articles)):
        ct_texts = clinical_trials[i].get_all_texts()
        ar_texts = articles[i].get_all_texts()

        jd = [server.get_jds(ct_texts), server.get_jds(ar_texts)]
        jds.append(jd)

        st = [server.get_sts(ct_texts), server.get_sts(ar_texts)]
        sts.append(st)
    server.close_server()
    return jds, sts


def get_all_jds_sts_similarities(jds, sts, max_jds, max_sts, mode_jds='basic', mode_sts='basic'):
    # Given the jds, sts and the methods to compare them, I compare and return the results of jds and sts
    possible_modes = ['basic', 'confidence', 'ranking', 'confidence_ranking']
    if mode_jds not in possible_modes or mode_sts not in possible_modes:
        raise ValueError("Use a valid mode to compare jds and sts")
    jds_similarities = []
    sts_similarities = []

    for i in range(len(jds)):
        jds_comparator = globals()['get_jds_sts_' + mode_jds + '_similarities']
        sts_comparator = globals()['get_jds_sts_' + mode_sts + '_similarities']

        jds_similarity = jds_comparator(jds[i][0][:max_jds], jds[i][1][:max_jds])
        sts_similarity = sts_comparator(sts[i][0][:max_sts], sts[i][1][:max_sts])

        jds_similarities.append(jds_similarity)
        sts_similarities.append(sts_similarity)
    return jds_similarities, sts_similarities


def create_required_folders():
    # I create this folders in case they weren't present (they will be used in the oger similarity function)
    # This function is used to create support folders, the folders will be used to calculate oger similarities
    if not os.path.exists(common_functions.get_src_path() + '/tmp_txt_ct/'):
        os.makedirs(common_functions.get_src_path() + '/tmp_txt_ct/')
    if not os.path.exists(common_functions.get_src_path() + '/tmp_txt_ar/'):
        os.makedirs(common_functions.get_src_path() + '/tmp_txt_ar/')


def get_oger_similarity(oger_1, oger_2):
    # This function takes 2 string arrays and returns the number of common words between the 2 divided by
    # the maximum number of common words possible
    common_words = 0
    max_words = max(len(oger_1), len(oger_2))
    for term_1 in oger_1:
        for term_2 in oger_2:
            if term_1 == term_2:
                common_words += 1
    if max_words == 0:
        max_words = 1
    return common_words/max_words


def get_oger_similarities(clinical_trials, articles):
    # This function finds medical terms in the texts of clinical trials and articles, this procedure yields as a result
    # 2 arrays of strings that are then passed to the oger_similarity function that gives the similarity between the
    # 2 texts according to the number of common words/max number of possible common words
    conf = Router(termlist_path='src/oger/test/testfiles/test_terms.tsv')
    pl = PipelineServer(conf)
    create_required_folders()
    similarities = []

    for i in range(len(articles)):
        ct_entities = []
        ar_entities = []

        # The oger library works on files, I need to create them first
        # The files will contain the content of the texts of the clinical trials and of the articles
        ct_texts = clinical_trials[i].get_all_texts()
        ar_texts = articles[i].get_all_texts()

        ct_id = clinical_trials[i].clinical_trial.find('nct_id').text.strip()
        ar_id = articles[i].article.PMID.text.strip()

        ct_file = codecs.open(common_functions.get_src_path()+'/tmp_txt_ct/' + ct_id + '.txt', 'w', 'utf-8')
        ct_file.write(ct_texts)
        ct_file.close()

        ar_file = codecs.open(common_functions.get_src_path()+'/tmp_txt_ar/' + ar_id + '.txt', 'w', 'utf-8')
        ar_file.write(ar_texts)
        ar_file.close()

        # Oger library usage with clinical trials
        doc = pl.load_one(common_functions.get_src_path()+'/tmp_txt_ct/' + ct_id + ".txt", 'txt')
        pl.process(doc)

        entity_iter = doc[0].iter_entities()

        for entity in entity_iter:
            ct_entities.append(entity.info[3])

        # Oger library usage with articles
        doc = pl.load_one(common_functions.get_src_path()+'/tmp_txt_ar/' + ar_id + ".txt", 'txt')
        pl.process(doc)

        entity_iter = doc[0].iter_entities()

        for entity in entity_iter:
            ar_entities.append(entity.info[3])

        similarities.append(get_oger_similarity(ct_entities, ar_entities))
    return similarities


def get_doc2vec_vectors(clinical_trials, articles):
    # I get the doc2vec for each article and clinical trial
    model = common_functions.get_gensim_doc2vec_model()

    ct_vectors = []
    ar_vectors = []
    for i in range(len(articles)):
        ct_texts = clinical_trials[i].get_all_texts().replace(",", " ").replace(";", " ").replace(".", " ")
        ct_texts = ct_texts.split(" ")

        ar_texts = articles[i].get_all_texts().replace(",", " ").replace(";", " ").replace(".", " ")
        ar_texts = ar_texts.split(" ")

        ct_vector = model.infer_vector(ct_texts)
        ct_vectors.append(ct_vector)

        ar_vector = model.infer_vector(ar_texts)
        ar_vectors.append(ar_vector)

    return ct_vectors, ar_vectors


def get_vectors_similarity(vec_1, vec_2):
    # I get the similarity of the vector with the formula scalar_rpoduce(vec_1, vec_2)/(||vec_1||*||vec_2||)
    vec_1_length = math.sqrt(sum([el**2 for el in vec_1]))
    vec_2_length = math.sqrt(sum([el**2 for el in vec_2]))
    scalar_product = sum(el[0] * el[1] for el in zip(vec_1, vec_2))
    return scalar_product/(vec_1_length * vec_2_length)


def get_doc2vec_vectors_similarities(clinical_trials, articles):
    # I get all the vector similarities
    ct_vectors, ar_vectors = get_doc2vec_vectors(clinical_trials, articles)
    return [get_vectors_similarity(ct_vectors[i], ar_vectors[i]) for i in range(len(ct_vectors))]
