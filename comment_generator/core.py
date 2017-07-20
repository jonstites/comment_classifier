#!/usr/bin/env python3

from collections import Counter
import json
import pickle


class Comment:

    def __init__(self, content):
        self.content = content

    def from_string(text):
        if isinstance(text, bytes):
            text = text.decode("utf-8")
        content = json.loads(text)
        return Comment(content)

    def get_body(self):
        return self.content["body"]

    def __eq__(self, other):
        return self.content == other.content

    def __ne__(self, other):
        return not (self.content == other.content)
    
class CommentReader:

    def from_open_file(opened_handle):
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

    
class NgramCounter:

    def __init__(self, ngram_size):
        self.ngram_size = ngram_size
        self.counts = Counter()

    def add(self, text):
        tokenizer = Tokenizer(text)
        tokens = tokenizer.get_tokens(self.ngram_size)
        ngram_iterator = self.get_ngrams(tokens)
        self.counts.update(ngram_iterator)
    
    def get_ngrams(self, tokens):
        num_tokens = len(tokens)
        
        stop = num_tokens - (self.ngram_size - 1)
        for i in range(stop):
            yield tuple(tokens[i: i + self.ngram_size])

    def __eq__(self, other):
        return self.counts == other.counts

    def __ne__(self, other):
        return not (self.counts == other.counts)

    
class MultiNgramCounter:

    def __init__(self, max_ngram_size):
        self.max_ngram_size = max_ngram_size
        self.set_ngram_counters()

    def set_ngram_counters(self):
        ngram_counters = []
        for ngram_size in range(1, self.max_ngram_size + 1):
            ngram_counters.append(NgramCounter(ngram_size))
        self.ngram_counters = ngram_counters
        
    def add(self, text):
        for ngram_counter in self.ngram_counters:
            ngram_counter.add(text)

    def __eq__(self, other):
        if self.max_ngram_size != other.max_ngram_size:
            return False

        if len(self.ngram_counters) != len(other.ngram_counters):
            return False
        
        zipped_counters = zip(self.ngram_counters, other.ngram_counters)
        for counter_1, counter_2 in zipped_counters:
            if counter_1 != counter_2:
                return False
        return True
        
    def __neq__(self, other):
        return not (self == other)


class MarkovModel:

    def __init__(self, max_ngram_size):
        self.reset_ngram_size(max_ngram_size)

    def reset_ngram_size(self, max_ngram_size):
        self.max_ngram_size = max_ngram_size
        self.reset_ngrams()
        
    def reset_ngrams(self):
        self.ngram_counters = MultiNgramCounter(self.max_ngram_size)
        
    def train(self, file_handle):
        i = 0
        for comment in CommentReader.from_open_file(file_handle):
            self.add_comment(comment)
            i += 1
            if i % 100000 == 0:
                print(i)

    def add_comment(self, comment):
        text = comment.get_body()
        self.add(text)

    def add(self, text):
        self.ngram_counters.add(text)

    def save(self, file_handle):
        pickle.dump(self, file_handle)

    def load(file_handle):
        return pickle.load(file_handle)

    def __eq__(self, other):
        return self.ngram_counters == other.ngram_counters

    def __ne__(self, other):
        return not (self == other)
