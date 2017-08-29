#!/usr/bin/env python3

from collections import Counter
import json
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.linear_model import SGDClassifier

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

    def get_subreddit(self):
        return self.content["subreddit"]

    def __eq__(self, other):
        return self.content == other.content

    def __ne__(self, other):
        return not (self.content == other.content)

    
class CommentReader:

    def from_open_file(opened_handle):
        for line in opened_handle:
            comment = Comment.from_string(line)
            yield comment

    def get_batch(opened_handle, batch_size, use_subreddits=None):
        comments = []
        for comment in CommentReader.from_open_file(opened_handle):
            if use_subreddits:
                subreddit = comment.get_subreddit()
                if subreddit not in use_subreddits:
                    continue
            comments.append(comment)
            if len(comments) == batch_size:
                yield comments

    def get_subreddit_counts(opened_handle):
        counts = Counter()
        for comment in CommentReader.from_open_file(opened_handle):
            subreddit = comment.get_subreddit()
            counts[subreddit] += 1
        return counts
                
class MarkovModel:

    def __init__(self, max_ngram, feature_num):
        self.classifier = SGDClassifier(n_jobs=-1)
        self.vectorizer = HashingVectorizer(n_features=feature_num, ngram_range=(1, max_ngram))
        
    def train(self, file_handle, use_subreddits, batch_size=1000000):
        for number, batch_comments in enumerate(CommentReader.get_text_batch(file_handle, use_subreddits=use_subreddits, batch_size=batch_size)):
            texts, subreddits = batch_comments
            feature_matrix = self.vectorizer.transform(texts)
            self.classifier.partial_fit(feature_matrix, subreddits, classes=classes)
            print("completed batch {0}".format(number))

    def score(self, file_handle, use_subreddits, batch_size=1000000):
        for number, batch_comments in enumerate(CommentReader.get_text_batch(file_handle, use_subreddits=use_subreddits, batch_size=batch_size)):
            texts, subreddits = batch_comments
            feature_matrix = self.vectorizer.transform(texts)
            mean_accuracy = self.classifier.score(feature_matrix, subreddits)
            print("batch {0} accuracy: {1}".format(number, mean_accuracy))
            
            
    def get_vocabulary(file_handle):
        pass

    def save(self, file_handle):
        pass

    def load(file_handle):
        pass
