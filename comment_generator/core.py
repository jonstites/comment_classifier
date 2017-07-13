#!/usr/bin/env python3

import bz2
import json

class Comment:

    def __init__(self, content):
        self.content = content
        self.comment_start = "<C>"
        self.comment_end = "</C>"

    def from_string(comment):
        content = json.loads(comment)
        return Comment(content)

    def get_body(self):
        return self.content["body"]
    
    def get_tokenization(self):
        body = self.get_body()
        return body.split()

    def get_ngrams(self, ngram_size):
        tokens = self.get_tokenization()
        num_tokens = len(tokens)
        
        stop = num_tokens - (ngram_size - 1)
        for i in range(stop):
            yield tuple(tokens[i: i + ngram_size])
    
class CommentReader:

    def from_file(opened_handle):
        for line in opened_handle:
            comment = Comment.from_string(line)
            yield comment

class MarkovModel:

    def get_ngrams(text, size):
        pass
