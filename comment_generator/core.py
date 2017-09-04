#!/usr/bin/env python3

from collections import Counter
import json
import numpy
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import f1_score

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
                comments = []
        yield comments

    def split_comments(comments):
        texts = []
        subreddits = []
        for comment in comments:
            texts.append(comment.get_body())
            subreddits.append(comment.get_subreddit())
        return texts, subreddits
            
    def get_subreddit_counts(opened_handle):
        counts = Counter()
        for comment in CommentReader.from_open_file(opened_handle):
            subreddit = comment.get_subreddit()
            counts[subreddit] += 1
        return counts
                
class MarkovModel:

    def __init__(self, max_ngram, subreddit_counts, max_size):
        num_features = self.get_num_features(subreddit_counts, max_size)
        self.vectorizer = HashingVectorizer(n_features=num_features, ngram_range=(1, max_ngram))

        self.classes = numpy.array(list(subreddit_counts.keys()))
        class_weights = self.get_balanced_class_weights(subreddit_counts)
        
        self.classifier = SGDClassifier(n_jobs=-1, class_weight=class_weights)
        
    def train(self, file_handle, use_subreddits, batch_size=1000000, num_batches=None):
        for batch_number, batch_comments in enumerate(CommentReader.get_batch(file_handle, use_subreddits=use_subreddits, batch_size=batch_size)):
            texts, subreddits = CommentReader.split_comments(batch_comments)
            feature_matrix = self.vectorizer.transform(texts)

            self.classifier.partial_fit(feature_matrix, subreddits, classes=self.classes)

            if num_batches:
                about_to_go_over = batch_number >= (num_batches - 1)
                if about_to_go_over:
                    return

    def f1_macro(self, file_handle, use_subreddits, batch_size=1000000, num_batches=None):
        for batch_number, batch_comments in enumerate(CommentReader.get_batch(file_handle, use_subreddits=use_subreddits, batch_size=batch_size)):
            texts, subreddits = CommentReader.split_comments(batch_comments)
            feature_matrix = self.vectorizer.transform(texts)

            predicted_subreddits = self.classifier.predict(feature_matrix)

            f1 = f1_score(subreddits, predicted_subreddits, average="macro")
            return f1
            
    def get_num_features(self, subreddit_counts, max_size=2**30):
        num_subreddits = len(subreddit_counts.keys())
        return int(max_size / num_subreddits)

    def get_balanced_class_weights(self, subreddit_counts):
        weights = {}
        total = sum(subreddit_counts.values())
        num_classes = len(subreddit_counts.keys())
        
        for subreddit, count in subreddit_counts.items():
            weights[subreddit] = total / (num_classes * count)
            
        return weights
    
    def get_vocabulary(file_handle):
        pass

    def save(self, file_handle):
        pass

    def load(file_handle):
        pass
