import sys
sys.path.insert(0, 'src')

from preprocessing import *
from frequent_patterns import *
from closed_pattern import *
from max_pattern import *
from purity import *


def mine_all_patterns():
    preprocess_titles()
    num_topics = 5
    for topic in range(num_topics):
        mine_frequent_patterns(topic)
        mine_closed_patterns(topic)
        mine_max_patterns(topic)
    mine_purities(num_topics)

if __name__ == '__main__':
    mine_all_patterns()
