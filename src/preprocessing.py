import csv
import os


def get_all_words():
    '''
    Creates a list of unique words from the titles of papers and returns the titles
    '''
    with open('../data/paper.txt', 'rb') as f:
        reader = csv.reader(f)
        titles = list(reader)
        f.close()
    titles = [title[0].split('\t') for title in titles]
    titles = [title[1].split(' ') for title in titles]

    vocab = open('../data/vocab.txt', 'w')
    words = set()
    for title in titles:
        for word in title:
            if word not in words:
                vocab.write("{}\n".format(word))
                words.add(word)
    vocab.close()

    return titles, list(words)


def tokenize_words(titles, words):
    '''
    Tokenizes the titles into the format
    <num unique words> <word1 index>:<freq in title> <word2 index>:<freq in title>...
    '''
    tokens = open('../data/title.txt', 'w')
    for title in titles:
        token = '{}'.format(len(set(title)))
        used = set()

        for word in title:
            if word not in used:
                token += ' {}:{}'.format(words.index(word), title.count(word))
                used.add(word)
        token += '\n'
        tokens.write(token)
    tokens.close()


def partition_words_by_topic():
    # Partition titles using lda
    os.system('.././lda-c-dist/lda est 0.001 5 .././lda-c-dist/settings.txt ../data/./title.txt random ../data/./lda-result')

    with open('../data/lda-result/word-assignments.dat', 'rb') as f:
        reader = csv.reader(f)
        lines = list(reader)
        f.close()

    topics = [open('../data/topics/topic-{}.txt'.format(i), 'w') for i in range(5)]

    for line in lines:
        data = line[0].split(' ')[1:]
        wrote_to = [0] * 5

        for tup in data:
            word_index, topic = tup.split(':')
            topic = int(topic)
            topics[topic].write("{} ".format(word_index))
            wrote_to[topic] = 1

        for file_num, wrote in enumerate(wrote_to):
            if wrote:
                topics[file_num].write('\n')

    for topic in topics:
        topic.close()


def preprocess_titles():
    titles, words = get_all_words()
    tokenize_words(titles, words)
    partition_words_by_topic()
