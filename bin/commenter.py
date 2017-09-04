#!/usr/bin/env python3

import argh
import bz2
from comment_generator.core import MarkovModel, CommentReader
import numpy




def run(comment_file, test_file, subreddit_counts, ngram_size):

    model = MarkovModel(ngram_size, subreddit_counts, max_size=2**30)

    num = 0
    with bz2.BZ2File(comment_file, "rb") as input_handle:
        with bz2.BZ2File(test_file, "rb") as test_handle:
            while input_handle.peek() and test_handle.peek():
                model.train(input_handle, subreddit_counts, num_batches=3, batch_size=50000)
                f1 = model.f1_macro(test_handle, subreddit_counts, num_batches=1, batch_size=10000)
                print("{} f1: {}".format(num, f1), flush=True)
                num += 1


def get_num_features(subreddits, max_size=2**30):
    num_subreddits = len(subreddits.keys())
    return int(max_size / num_subreddits)

def get_subreddit_counts(subreddit_file, top):
    subreddits = {}
    with open(subreddit_file) as handle:
        for line_num, line in enumerate(handle):
            subreddit = line.split()[0]
            count = int(line.split()[1])
            if line_num >= top:
                break
            subreddits[subreddit] = count
    return subreddits
        
def main(comment_file, test_file, subreddit_file, top=100, ngram_size=3):
    subreddit_counts = get_subreddit_counts(subreddit_file, top)
    run(comment_file, test_file, subreddit_counts, ngram_size)
        
if __name__ == "__main__":
    argh.dispatch_command(main)
