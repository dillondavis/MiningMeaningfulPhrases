import csv
from frequent_patterns import print_formatted_patterns


def mine_closed_patterns(file_no):
    with open('../results/frequent_patterns/pattern-{}.txt'.format(file_no), 'rb') as f:
        reader = csv.reader(f)
        lines = list(reader)
        lines = [line[0].split(' ') for line in lines]
        for line in lines:
            line[0] = int(line[0])
        f.close()

    closed_patterns = {}
    for line in lines:
        pattern = set(line[1:])

        # Check other patterns for super pattern with same support
        closed = 1
        for line2 in lines:
            pattern2 = set(line[1:])
            if len(pattern) < len(pattern2) and pattern.issubset(pattern2) and line[0] == line2[0]:
                closed = 0

        if closed:
            closed_patterns[frozenset(line[1:])] = line[0]

    print_formatted_patterns(closed_patterns, '../results/closed_patterns', 'closed', file_no)
    print_formatted_patterns(closed_patterns, '../results/closed_patterns', 'closed', file_no, words=True)
