#!/usr/bin/env python3

from collections import Counter
import json
import itertools
import pickle
import sqlite3


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

    pad_token = "<padding>"
    end_token = "</C>"
    
    def tokens(text):
        return text.split()

    def padded_tokens(text, ngram_size):
        pad_amount = ngram_size - 1
        pad_tokens = [Tokenizer.pad_token] * pad_amount
        text_tokens = Tokenizer.tokens(text)
        return pad_tokens + text_tokens

    def padded_tokens_with_end(text, ngram_size):
        return Tokenizer.padded_tokens(text, ngram_size) + [Tokenizer.end_token]


class Smoothing:

    def unkify_if_needed():
        pass


class NgramEnumerator:

    def enumerate_ngrams(tokens, ngram_size):
        ngram_start = 0
        ngram_stop = ngram_size
        while ngram_stop <= len(tokens):
            ngram_tokens = tokens[ngram_start: ngram_stop]
            ngram_start += 1
            ngram_stop += 1
            yield tuple(ngram_tokens)
            
    def comment_to_ngrams(comment, ngram_size):
        comment_tokens = Tokenizer.padded_tokens_with_end(text, ngram_size)
        for ngram in NgramEnumerator.enumerate_ngrams(comment_tokens, ngram_size):
            yield ngram

    def comment_to_ngram_range(comment, min_ngram, max_ngram):
        for ngram_size in range(min_ngram, max_ngram + 1):
            for ngram in NgramEnumerator.comment_to_ngrams(comment, ngram_size):
                yield ngram


class NgramBuffer:

    def __init__(self):
        pass

    def fill(self, file_handle):
        pass

    
class NgramDatabase:

    def __init__(self, database_name):
        self.database_name = database_name
        self.connection = self.connect_to_db()

    def connect_to_db(self):
        return sqlite3.connect(self.database_name)
    
    def create_table(self):
        command = "CREATE TABLE 'ngrams' (ngram text primary key, count integer)"
        self.connection.execute(command)
        
    def buffered_store(self, ngrams):
        pass

    def update_counts_from_db(self, ngram_counter):
        pass

    def lookup_count(self, ngram):
        pass
        
    def set_count(self):
        pass

    
class MarkovModel:

    def __init__(self, max_ngram_size):
        self.max_ngram_size = max_ngram_size
    
    def train(self, file_handle):
        pass

    def add_comment(self, comment):
        pass

    def add(self, text):
        pass

    def save(self, file_handle):
        pass

    def load(file_handle):
        pass
