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


def get_similarity(phrase1, phrase2):
    words1 = phrase1.split(" ")
    words2 = phrase2.split(" ")
    counter = 0
    for word1 in words1:
        for word2 in words2:
            if word1 == word2:
                counter += 1
                break
    return counter/len(words1)


def get_organization_similarity(ct_org, ar_org):
    similarities = []
    for i in range(len(ct_org)):
        if ct_org[i] is not None:
            ct_org[i] = ct_org[i].replace('.', '').replace(',', '').replace(';', '').replace('-', ' ')
        if ar_org[i] is not None:
            ar_org[i] = ar_org[i].replace('.', '').replace(',', '').replace(';', '').replace('-', ' ')

        if ct_org[i] is not None and ar_org[i] is not None:
            similarities.append(get_similarity(ct_org[i], ar_org[i]))
        else:
            similarities.append(0)
    return similarities
