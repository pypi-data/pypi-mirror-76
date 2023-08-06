from itertools import repeat
from typing import Optional


def levenshtein(s, t):
    """
    Calculate the Levenshtein distance between two strings. From Wikipedia article: Iterative with two matrix rows.

    :param s: string 1
    :type s: str
    :param t: string 2
    :type s: str
    :return: Levenshtein distance
    :rtype: float
    """

    if s == t:
        return 0
    elif len(s) == 0:
        return len(t)
    elif len(t) == 0:
        return len(s)

    v0 = list(repeat(0, len(t) + 1))
    v1 = list(repeat(0, len(t) + 1))
    for i in range(len(v0)):
        v0[i] = i
    for i in range(len(s)):
        v1[0] = i + 1
        for j in range(len(t)):
            cost = 0 if s[i] == t[j] else 1
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
        for j in range(len(v0)):
            v0[j] = v1[j]

    return v1[len(t)]


def hamming(s, t):
    """
    Calculate the Hamming distance between two strings. From Wikipedia article: Iterative with two matrix rows.

    :param s: string 1
    :type s: str
    :param t: string 2
    :type s: str
    :return: Hamming distance
    :rtype: float
    """
    if len(s) != len(t):
        raise ValueError('Hamming distance needs strings of equal length.')
    return sum(s_ != t_ for s_, t_ in zip(s, t))


def get_index_of_approximate_match(query: str, template: str, allowed_mismatches=1) -> Optional[int]:
    """ Find the index of a substring with mismatches. """
    # TODO: Change this to bitap algorithm (https://en.wikipedia.org/wiki/Bitap_algorithm)
    for index in range(-allowed_mismatches, len(template) - len(query) + allowed_mismatches + 1):
        mismatches = max(0, -index)
        for i in range(mismatches, min(len(query), len(template) - index)):
            if query[i] != template[index + i]:
                mismatches += 1
                if mismatches > allowed_mismatches:
                    break
        if mismatches <= allowed_mismatches:
            return index
    return None
