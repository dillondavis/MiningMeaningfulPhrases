import csv
from math import log, pow
from frequent_patterns import get_word_list


def print_formatted_purity_patterns(patterns, file_no):
    # Format results and write to file
    fil = '../results/pure_patterns/pure-{}.txt'.format(file_no)
    word_list = get_word_list()

    p = open(fil, 'w')
    sort_func = lambda x: x[1][0] * x[1][1]
    for pattern, sup in sorted(patterns.items(), key=sort_func, reverse=True):
        p.write('{}'.format(sup[0]))
        for word in pattern:
            p.write(' {}'.format(word_list[int(word)]))
        p.write('\n')

    p.close()


def get_pattern_frequency(pattern, frequent_patterns, single_patterns):
    if pattern in frequent_patterns:
        return frequent_patterns[pattern]

    freq = set()
    for i, word in enumerate(pattern):
        if word not in single_patterns:
            return 0
        if i == 0:
            freq = set(single_patterns[word])
        else:
            freq = freq.intersection(set(single_patterns[word]))

    return len(freq)



def mine_purities(num_files):
    files = []
    files_patterns = []
    single_patterns = []
    for i in range(num_files):
        with open('../data/topics/topic-{}.txt'.format(i), 'rb') as f:
            reader = csv.reader(f)
            lines = list(reader)
            lines = set([line[0] for line in lines])
            files.append(lines)

            single_freqs = {}
            for j, line in enumerate(lines):
                for word in line.split(' '):
                    if word in single_freqs:
                        single_freqs[word].append(j)
                    else:
                        single_freqs[word] = [j]
            single_patterns.append(single_freqs)
            f.close()

        with open('../results/frequent_patterns/pattern-{}.txt'.format(i), 'rb') as f:
            reader = csv.reader(f)
            lines = list(reader)
            lines = [line[0].split(' ') for line in lines]
            file_patterns = {}
            for line in lines:
                sup = int(line[0])
                pattern = frozenset(line[1:])
                file_patterns[pattern] = sup
            files_patterns.append(file_patterns)
            f.close()

    # Find all D(t, t')
    Ds = []
    for i, fil in enumerate(files):
        D = []
        for j, fil2 in enumerate(files):
            D.append(len(set(files[i]).union(set(fil2))))
        Ds.append(D)

    files_purities = []
    for i, file_patterns in enumerate(files_patterns):
        file_purities = {}
        for pattern, sup in file_patterns.items():
            # Find max of (f(t,p) + f(t',p))/|D(t,t')
            max_second_term = 0
            for j, file_patterns2 in enumerate(files_patterns):
                if i != j:
                    ftp = sup
                    ftprimep = get_pattern_frequency(pattern, file_patterns2, single_patterns[j])
                    dttprime = Ds[i][j]

                    term = float(ftp + ftprimep) / dttprime
                    max_second_term = max(term, max_second_term)

            purity_first_term = log(float(sup)/len(files[i]), 2)
            purity_second_term = log(max_second_term, 2)
            purity = purity_first_term - purity_second_term
            file_purities[pattern] = (purity, sup)

        files_purities.append(file_purities)
        print_formatted_purity_patterns(files_purities[i], i)
