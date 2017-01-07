import itertools
import csv


def add_frequent_patterns(patterns, frequent_patterns, minsup):
    for pattern, val in patterns.items():
        if len(val) >= minsup:
            frequent_patterns[pattern] = len(val)


def find_possible_new_patterns(curr_patterns, curr_length):
    patterns = curr_patterns.keys()
    new_patterns = []
    new_length = curr_length + 1
    if len(patterns) < new_length:
        return []
    all_perms = itertools.combinations(patterns, new_length)

    for perm in all_perms:
        new_pattern = []
        for pattern in perm:
            new_pattern += list(pattern)

        new_pattern = list(set(new_pattern))
        if len(new_pattern) == new_length:
            new_patterns.append(new_pattern)

    return new_patterns


def get_first_frequency_dict(patterns, lines):
    pattern_dict = {}
    for i,line in enumerate(lines):
        for pattern in patterns:
            if set(pattern).issubset(set(line)):
                pattern_set = frozenset(pattern)
                if pattern_set in pattern_dict:
                    pattern_dict[pattern_set].append(i)
                else:
                    pattern_dict[pattern_set] = [i]

    return pattern_dict


def get_add_frequent_patterns(patterns, old_freq_dict, frequent_patterns, minsup):
    pattern_dict = {}
    for pattern in patterns:
        combos = itertools.combinations(pattern, len(pattern) - 1)

        for i, combo in enumerate(combos):
            if i == 0:
                pattern_freq = set(old_freq_dict[frozenset(combo)])
            else:
                pattern_freq = pattern_freq.intersection(set(old_freq_dict[frozenset(combo)]))

        pattern_freq = list(pattern_freq)
        if len(pattern_freq) >= minsup:
            froze = frozenset(pattern)
            frequent_patterns[froze] = len(pattern_freq)
            pattern_dict[froze] = pattern_freq

    return pattern_dict


def get_word_list():
    with open('../data/vocab.txt', 'rb') as f:
        reader = csv.reader(f)
        lines = list(reader)
        words = [line[0] for line in lines if line]
        f.close()
    return words


def print_formatted_patterns(patterns, directory, file_name, file_no, words=False):
    # Format results and write to file
    fil = '{}/{}-{}.txt'.format(directory, file_name, file_no)
    if words:
        word_list = get_word_list()
        fil += '.phrase'

    p = open(fil, 'w')
    for pattern, sup in sorted(patterns.items(), key=lambda x: x[1], reverse=True):
        p.write('{}'.format(sup))
        for word in pattern:
            if words:
                p.write(' {}'.format(word_list[int(word)]))
            else:
                p.write(' {}'.format(word))
        p.write('\n')

    p.close()


def mine_frequent_patterns(file_no):
    with open('../data/topics/topic-{}.txt'.format(file_no), 'rb') as f:
        reader = csv.reader(f)
        lines = list(reader)
        f.close()
    lines = [line[0].split(' ') for line in lines]
    minsup = int(len(lines) * 0.01)

    # Get all words
    new_patterns = []
    for line in lines:
        for word in line:
            if len(word) and [word] not in new_patterns:
                new_patterns.append([word])

    # Mine patterns
    frequent_patterns = {}
    i = 0
    while len(new_patterns):
        if i == 0:
            freq_dict = get_first_frequency_dict(new_patterns, lines)
            add_frequent_patterns(freq_dict, frequent_patterns, minsup)

        else:
            freq_dict = get_add_frequent_patterns(new_patterns, old_freq_dict,
                                                     frequent_patterns, minsup)

        i += 1
        new_patterns = find_possible_new_patterns(freq_dict, i)
        old_freq_dict = freq_dict

    print_formatted_patterns(frequent_patterns, '../results/frequent_patterns', 'pattern', file_no)
    print_formatted_patterns(frequent_patterns, '../results/frequent_patterns', 'pattern', file_no, words=True)
