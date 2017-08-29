#!/usr/bin/env python3

import argh
import bz2
from comment_generator.core import MarkovModel, CommentReader
import numpy


def run(comment_file, test_file, ngram_size, num_subreddits):
    print("performing on: {}".format(ngram_size))
    feature_size = (2**30 / num_subreddits)
    model = MarkovModel(ngram_size, feature_size)

    subreddits_set = set()
    train_total = 0
    with bz2.BZ2File(comment_file, "rb") as input_handle:
        for comment in CommentReader.from_open_file(input_handle):
            subreddit = comment.get_subreddit()
            subreddits_set.add(subreddit)
            train_total += 1
            
    with bz2.BZ2File(test_file, "rb") as test_handle:
        for comment in CommentReader.from_open_file(test_handle):
            subreddit = comment.get_subreddit()
            subreddits_set.add(subreddit)


    subreddits = numpy.array(list(subreddits_set))
    print("classifying {} subreddits".format(len(subreddits)))
    with bz2.BZ2File(comment_file, "rb") as input_handle:
        print("total training comments: ", train_total)
        model.train(input_handle, subreddits)


    with bz2.BZ2File(test_file, "rb") as test_handle:
        model.score(test_handle, subreddits)


def main(comment_file, test_file):
    for ngram_size in range(1, 6):
        run(comment_file, test_file, ngram_size)
        
if __name__ == "__main__":
    argh.dispatch_command(main)
