#!/usr/bin/env python3

import bz2
import json

class Comment:

    def __init__(self, content):
        self.content = content
        self.pad_token = "<padding>"
        self.end_token = "</C>"

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
        padding = [self.pad_token] * (ngram_size - 1)
        padded_tokens = padding + tokens + [self.end_token]
        num_tokens = len(padded_tokens)
        
        stop = num_tokens - (ngram_size - 1)
        for i in range(stop):
            yield tuple(padded_tokens[i: i + ngram_size])
    
class CommentReader:

    def from_file(opened_handle):
        for line in opened_handle:
            comment = Comment.from_string(line)
            yield comment

class MarkovModel:

    def get_ngrams(text, size):
        pass
