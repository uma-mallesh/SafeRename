from collections import Counter


def detect_duplicates(names):

    counts = Counter(names)

    duplicates = []

    for name, count in counts.items():

        if count > 1:

            duplicates.append(name)

    return duplicates