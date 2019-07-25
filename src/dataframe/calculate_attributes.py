import requests
from bs4 import BeautifulSoup
from ..common_functions import common_functions


def get_arrays_equality(arr1, arr2):
    equalities = []
    for i in range(len(arr1)):
        if arr1[i] is not None and arr2[i] is not None and arr1[i] == arr2[i]:
            equalities.append(1)
        else:
            equalities.append(0)
    return equalities


def levenshtein(s1, s2):
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
    similarities = []
    for i in range(len(arr1)):  # both arrays need to have the same length
        if arr1[i] is not None and arr2[i] is not None:
            max_length = len(max([arr1[i], arr2[i]], key=len))
            score = levenshtein(arr1[i], arr2[i])/max_length
            similarities.append(1-score)
        else:
            similarities.append(0)
    return similarities


def get_best_similarity(arr1, arr2):
    max_score = 0
    for org1 in arr1:
        for org2 in arr2:
            max_length = len(max([org1, org2], key=len))
            score = 1-(levenshtein(org1, org2)/max_length)

            if score > max_score:
                max_score = score
    return max_score


def get_org_similarity(org1, org2, ct_sample, ar_sample):

    if ct_sample == 'standard' and ar_sample == 'standard':
        max_length = len(max([org1, org2], key=len))
        return 1-(levenshtein(org1, org2)/max_length)

    if ct_sample == 'standard' and ar_sample != 'standard':
        similarity = get_best_similarity([org1], org2)
    else:
        similarity = get_best_similarity(org1, org2)

    return similarity


def both_contain(phrase1, phrase2, word):
    return word in phrase1 and word in phrase2


def check_same_organization_type(phrase1, phrase2):
    phrase1 = phrase1.lower()
    phrase2 = phrase2.lower()
    university = both_contain(phrase1, phrase2, 'university')
    hospital = both_contain(phrase1, phrase2, 'hospital')
    school = both_contain(phrase1, phrase2, 'school')
    institute = both_contain(phrase1, phrase2, 'institute')

    return university or hospital or school or institute


def get_type_equality(arr1, arr2):
    for org1 in arr1:
        for org2 in arr2:
            if check_same_organization_type(org1, org2):
                return 1
    return 0


def get_org_type_equality(org1, org2, ct_sample, ar_sample):
    if ct_sample == 'standard' and ar_sample == 'standard':
        return 1 if check_same_organization_type(org1, org2) else 0

    if ct_sample == 'standard' and ar_sample != 'standard':
        equality = get_type_equality([org1], org2)
    else:
        equality = get_type_equality(org1, org2)

    return equality


def get_organization_similarity_and_type_equality(ct_org, ar_org, ct_sample, ar_sample):
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
    differences = []
    for i in range(len(ct_years)):
        difference = abs(ct_years[i] - ar_years[i])
        differences.append(difference)
    return differences


def get_last_name_lengths(last_names):
    lengths = []
    for i in range(len(last_names)):
        lengths.append(len(last_names[i]))
    return lengths


def fetch_namespace_sizes(author_list):
    author_str_list = ''

    # I create the list of ID in a string, so that it can be usable in the HTTP request
    for el in author_list:
        author_str_list += el

    # I set up the HTTP request
    url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=' + author_str_list + '&rettype=xml'

    # I return the result of the request
    return requests.get(url)


def get_namespace_ambiguities(last_names, initials):
    names_array = []
    for i in range(len(last_names)):
        string = last_names[i] + '+' + initials[i] + '[author]'
        names_array.append(string)

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
        termSets = [termSet for termSet in namespaces.TranslationStack.findAll('TermSet')
                    if termSet.Term.text.split('[')[1][:-1].lower() == 'author']
        for termSet in termSets:
            namespace_sizes.append(int(termSet.Count.text))
    return namespace_sizes


def get_formatted(arr):
    arr = [word.lower() for word in arr]
    for i in range(len(arr)):
        if arr[i] == 'usa':
            arr[i] = 'united states'
        if arr[i] == 'uk':
            arr[i] = 'united kingdom'
    return arr


def get_equality(arr1, arr2):
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
    country_equalities = []
    city_equalities = []
    for i in range(len(ct_countries)):
        country_equality = get_equality(ct_countries[i], ar_locations[i])
        city_equality = get_equality(ct_cities[i], ar_locations[i])
        if city_equality == 1:
            country_equality = 1
        country_equalities.append(country_equality)
        city_equalities.append(city_equality)
    return country_equalities, city_equalities


def get_sum_jds_sts(jds):
    percentage_sum = 0
    for percentage, term in jds:
        percentage_sum += percentage
    return percentage_sum


def get_jds_sts_percentage_similarities(jds_1, jds_2):
    max_percentage_sum = max(get_sum_jds_sts(jds_1), get_sum_jds_sts(jds_2))
    percentage_difference_sum = 0
    for percentage_1, term_1 in jds_1:
        for percentage_2, term_2 in jds_2:
            if term_1 == term_2:
                current_max = max(percentage_1, percentage_2)
                absolute_difference = abs(percentage_2 - percentage_1)
                percentage_difference_sum += (current_max - absolute_difference)
    return percentage_difference_sum/max_percentage_sum


def get_jds_sts_basic_similarities(jds_1, jds_2):
    common_words = 0
    max_words = max(len(jds_1), len(jds_2))
    for percentage_1, term_1 in jds_1:
        for percentage_2, term_2 in jds_2:
            if term_1 == term_2:
                common_words += 1
    return common_words/max_words


def calculate_max_similarity(num):
    similarity = 0
    for i in range(num):
        similarity += (num/(i+1))**2
    return similarity


def get_jds_sts_ranking_similarities(jds_1, jds_2):
    similarity = 0
    jds_length = len(jds_1)
    max_similarity = calculate_max_similarity(jds_length)
    for i in range(len(jds_1)):
        for j in range(len(jds_2)):
            if jds_1[i][1] == jds_2[j][1]:
                similarity += (jds_length/(i+1)) * (jds_length/(j+1))
    return similarity/max_similarity


def get_sum_jds_sts_ranking(jds):
    percentage_sum = 0
    for i in range(len(jds)):
        percentage_sum += (jds[i][0] * len(jds)**2) / (i+1)
    return percentage_sum


def get_jds_sts_percentage_ranking_similarities(jds_1, jds_2):
    max_percentage_sum = max(get_sum_jds_sts_ranking(jds_1), get_sum_jds_sts_ranking(jds_2))
    percentage_difference_sum = 0
    for i in range(len(jds_1)):
        for j in range(len(jds_2)):
            if jds_1[i][1] == jds_2[j][1]:
                current_max = max(jds_1[i][0], jds_2[i][0])
                absolute_difference = abs(jds_1[i][0] - jds_2[i][0])
                percentage_similarity = current_max - absolute_difference
                score = percentage_similarity * (len(jds_1)/(i+1)) * (len(jds_2)/(j+1))
                percentage_difference_sum += score
    return percentage_difference_sum / max_percentage_sum


def get_all_jds_sts_similarities(clinical_trials, articles, max_jds, max_sts, mode_jds='basic', mode_sts='basic'):
    java_server = common_functions.get_java_gateway_server()
    jds_similarities = []
    sts_similarities = []

    for i in range(len(clinical_trials)):
        ct_texts = clinical_trials[i].get_text()
        ct_texts.append(clinical_trials[i].get_title())
        ct_texts = " ".join(ct_texts)

        ar_texts = articles[i].get_text()
        ar_texts.append(articles[i].get_title())
        ar_texts = " ".join(ar_texts)

        jds_comparator = globals()['get_jds_sts_' + mode_jds + '_similarities']
        sts_comparator = globals()['get_jds_sts_' + mode_sts + '_similarities']

        jds_similarity = jds_comparator(java_server.get_jds(ct_texts)[:max_jds],
                                        java_server.get_jds(ar_texts)[:max_jds])
        sts_similarity = sts_comparator(java_server.get_sts(ct_texts)[:max_sts],
                                        java_server.get_sts(ar_texts)[:max_sts])

        jds_similarities.append(jds_similarity)
        sts_similarities.append(sts_similarity)
    java_server.close_server()
    return jds_similarities, sts_similarities
