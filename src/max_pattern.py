import csv
from frequent_patterns import print_formatted_patterns


def mine_max_patterns(file_no):
    with open('../results/closed_patterns/closed-{}.txt'.format(file_no), 'rb') as f:
        reader = csv.reader(f)
        lines = list(reader)
        lines = [line[0].split(' ') for line in lines]
        for line in lines:
            line[0] = int(line[0])
        f.close()
    max_patterns = {}

    for line in lines:
        pattern = set(line[1:])

        # Check if there are any frequent super patterns
        is_max = 1
        for line2 in lines:
            pattern2 = set(line2[1:])
            if len(pattern) < len(pattern2) and pattern.issubset(pattern2):
                is_max = 0

        if is_max:
            max_patterns[frozenset(line[1:])] = line[0]

    print_formatted_patterns(max_patterns, '../results/max_patterns', 'max', file_no)
    print_formatted_patterns(max_patterns, '../results/max_patterns', 'max', file_no, words=True)
