#!/usr/bin/env python3

import bz2
from collections import Counter
import json

class Comment:

    def __init__(self, content):
        self.content = content

    def from_string(comment):
        content = json.loads(comment)
        return Comment(content)

    def get_body(self):
        return self.content["body"]
    
    
class CommentReader:

    def from_file(opened_handle):
        for line in opened_handle:
            comment = Comment.from_string(line)
            yield comment


class Tokenizer:

    def __init__(self, text):
        self.text = text
        self.pad_token = "<padding>"
        self.end_token = "</C>"

    def get_text_tokens(self):
        return self.text.split()

    def get_padded_tokens(self, ngram_size):
        padding_amount = ngram_size - 1
        padding_tokens = [self.pad_token] * padding_amount
        text_tokens = self.get_text_tokens()
        return padding_tokens + text_tokens

    def get_tokens(self, ngram_size):
        padded_tokens = self.get_padded_tokens(ngram_size)
        return padded_tokens + [self.end_token]
    
class Ngram:

    def __init__(self, ngram_size):
        self.ngram_size = ngram_size
        self.ngrams = Counter()

    def add(self, text):
        tokenizer = Tokenizer(text)
        tokens = tokenizer.get_tokens(self.ngram_size)
        ngram_iterator = self.get_ngrams(tokens)
        self.ngrams.update(ngram_iterator)

    def get_tokens(self, text):
        tokens = self.tokenize(text)
        padded_tokens = self.pad_tokens(tokens)
        final_tokens = self.append_end_token(padded_tokens)
        return final_tokens

    def append_end_token(self, padded_tokens):
        return padded_tokens + [self.end_token]
    
    def get_ngrams(self, tokens):
        num_tokens = len(tokens)
        
        stop = num_tokens - (self.ngram_size - 1)
        for i in range(stop):
            yield tuple(tokens[i: i + self.ngram_size])

class NgramCollection:

    def __init__(self):
        #[Ngram(i) for i in range(max_ngram_size)]
        pass

    def add(self, text):
        pass
    
class MarkovModel:

    def __init__(self, max_ngram_size):
        self.reset_ngram_size(max_ngram_size)

    def reset_ngram_size(self, max_ngram_size):
        self.max_ngram_size = max_ngram_size
        self.reset_ngrams()
        
    def reset_ngrams(self):
        self.ngrams = NgramCollection(self.max_ngram_size)
        
    def train(self, file_handle):
        for comment in CommentReader.from_file(file_handle):
            self.add_comment(comment)

    def add_comment(self, comment):
        text = comment.get_body()
        NgramCollection.add(text)
