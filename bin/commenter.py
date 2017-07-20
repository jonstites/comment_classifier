#!/usr/bin/env python3

import argh
import bz2
from comment_generator.core import MarkovModel

def main(comment_file, save=None):
    model = MarkovModel(3)
    with bz2.BZ2File(comment_file, "rb") as handle:
        model.train(handle)
    if save:
        model.save(save)

if __name__ == "__main__":
    argh.dispatch_command(main)
