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

    def from_open_file(opened_handle, end_token=False):
        for line in opened_handle:
            comment = Comment.from_string(line)

            if end_token:
                comment.add_end_token()

            yield comment


class Tokenizer:

    pad_token = "<padding>"
    end_token = "</C>"
    
    def tokens(text):
        return text.split()

    def padded_tokens(text, ngram_size):
        padding_amount = ngram_size - 1
        padding_tokens = [Tokenizer.pad_token] * padding_amount
        text_tokens = Tokenizer.tokens(text)
        return padding_tokens + text_tokens

    def padded_tokens_with_end(text, ngram_size):
        return Tokenizer.padded_tokens(text, ngram_size) + [Tokenizer.end_token]

class NgramCounter:

    def __init__(self, ngram_size):
        self.ngram_size = ngram_size
        self.counts = Counter()

    def add(self, text):
        tokens = Tokenizer.padded_tokens_with_end(text, self.ngram_size)
        ngram_iterator = self.ngrams_from_tokens(tokens)
        self.counts.update(ngram_iterator)
    
    def ngrams_from_tokens(self, tokens):
        num_tokens = len(tokens)
        
        stop = num_tokens - (self.ngram_size - 1)
        for i in range(stop):
            yield tuple(tokens[i: i + self.ngram_size])

    def get_ngrams(self):
        return self.counts.items()
        
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

    def get_ngrams(self):
        all_ngrams = (ngram_counter.get_ngrams() for ngram_counter in self.ngram_counters)
        return itertools.chain(*all_ngrams)
            
    def __eq__(self, other):
        if self.max_ngram_size != other.max_ngram_size:
            return False

        if len(self.ngram_counters) != len(other.ngram_counters):
            return False
        
        zipped_counters = zip(self.ngram_counters, other.ngram_counters)
        for self_counter, other_counter in zipped_counters:
            if self_counter != other_counter:
                return False
        return True
        
    def __neq__(self, other):
        return not (self == other)


class NgramDatabase:

    def __init__(self, database_name):
        self.database_name = database_name
        self.connect_to_db()

    def connect_to_db(self):
        self.connection = sqlite3.connect(self.database_name)
    
    def create_table(self):
        command = "CREATE TABLE 'ngrams' (ngram text primary key, count integer)"
        self.connection.execute(command)
        
    def add_to_db(self, ngram_counter):
        pass

    def update_counts_from_db(self, ngram_counter):
        for ngram, count in ngram_counter.get_ngrams():
            database_count = self.lookup_count(ngram)
            updated_count = count + database_count
            self.set_count(ngram, updated_count)

    def lookup_count(self, ngram):
        pass
        
    def set_count(self):
        pass

    
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

            if self.ngrams_too_large():
                self.save_to_database()

            i += 1
            if i % 100000 == 0:
                print(i)

    def add_comment(self, comment):
        text = comment.get_body()
        self.add(text)

    def add(self, text):
        self.ngram_counters.add(text)

    def ngrams_too_large(self):
        pass
        
    def save_to_database(self):
        pass
        
    def save(self, file_handle):
        pickle.dump(self, file_handle)

    def load(file_handle):
        return pickle.load(file_handle)

    def __eq__(self, other):
        return self.ngram_counters == other.ngram_counters

    def __ne__(self, other):
        return not (self == other)
