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


def get_similarity(org1, org2, ct_sample, ar_sample):

    if ct_sample == 'standard' and ar_sample == 'standard':
        max_length = len(max([org1, org2], key=len))
        return 1-(levenshtein(org1, org2)/max_length)

    if ct_sample == 'standard' and ar_sample != 'standard':
        similarity = get_best_similarity([org1], org2)
    else:
        similarity = get_best_similarity(org1, org2)

    return similarity


def get_organization_similarity(ct_org, ar_org, ct_sample, ar_sample):
    if ct_sample not in ['standard', 'spacy', 'stanford'] or ar_sample not in ['standard', 'spacy', 'stanford']:
        raise ValueError('ct_sample and ar_sample can assume only these values: standard, spacy, stanford')
    similarities = []
    for i in range(len(ct_org)):
        if ct_org[i] is not None and ar_org[i] is not None:
            similarities.append(get_similarity(ct_org[i], ar_org[i], ct_sample, ar_sample))
        else:
            similarities.append(0)
    return similarities


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
