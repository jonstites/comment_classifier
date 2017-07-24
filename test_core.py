from comment_generator.core import Comment, CommentReader, NgramCounter, MultiNgramCounter, Tokenizer, MarkovModel, NgramDatabase
from collections import Counter
import json
import io
import itertools
import os


def get_test_content():
    content = {
        "body": "my test comment",
        "subreddit": "my_test_subreddit"
    }
    return content

def get_test_comment():
    content = get_test_content()
    return Comment(content)

def test_comment_from_string():
    test_comment = get_test_comment()
    content_string = json.dumps(test_comment.content)
    
    comment = Comment.from_string(content_string)

    for key, value in test_comment.content.items():
        assert value == comment.content[key]

def test_comment_get_body():
    comment = get_test_comment()
    text = get_test_content()["body"]

    body = comment.get_body()

    assert body == text

def test_comment_eq():
    same_comment = get_test_comment()

    comment = get_test_comment()

    assert comment == same_comment
    assert not (comment != same_comment)

def test_comment_eq_diff():
    diff_comment = get_test_comment()
    diff_comment.content["subreddit"] = "all"

    comment = get_test_comment()

    assert comment != diff_comment
    assert not (comment == diff_comment)
    
def test_comment_reader_from_open_file():
    test_comment = get_test_comment()
    content = test_comment.content
    content_string = json.dumps(content)

    handle = io.StringIO(content_string)    

    count = 0
    for comment in CommentReader.from_open_file(handle):
        assert comment.content == content
        count += 1

    assert count == 1

def test_tokenizer_text_tokens():
    text = "A test text"
    test_tokens = ["A", "test", "text"]

    tokens = Tokenizer(text).get_text_tokens()
    
    assert tokens == test_tokens

def test_tokenizer_padded_tokens():
    tokenizer = Tokenizer("A test text")
    pad_token = tokenizer.pad_token
    ngram_size = 3
    expected_tokens = [pad_token, pad_token, "A", "test", "text"]
    
    tokens = tokenizer.get_padded_tokens(ngram_size)

    assert tokens == expected_tokens

def test_tokenizer_padded_tokens_unigram():
    tokenizer = Tokenizer("A test text")
    ngram_size = 1
    expected_tokens = ["A", "test", "text"]

    tokens = tokenizer.get_padded_tokens(1)

    assert tokens == expected_tokens

def test_tokenizer_tokens():
    tokenizer = Tokenizer("A test text")
    pad_token = tokenizer.pad_token
    end_token = tokenizer.end_token
    ngram_size = 2
    expected_tokens = [pad_token, "A", "test", "text", end_token]

    tokens = tokenizer.get_tokens(ngram_size)

    assert tokens == expected_tokens

def test_ngram_counter_ngrams_from_tokens():
    tokens = ["A", "test", "ngram"]
    ngram_counter = NgramCounter(2)
    expected_ngrams = [
        ("A", "test"),
        ("test", "ngram")
        ]

    ngrams = list(ngram_counter.ngrams_from_tokens(tokens))

    assert ngrams == expected_ngrams

def test_ngram_counter_add():
    text = "A text ngram text"
    ngram = NgramCounter(2)
    pad_token = Tokenizer("").pad_token
    end_token = Tokenizer("").end_token
    expected_ngrams = Counter(
        [(pad_token, "A"),
         ("A", "text"),
         ("text", "ngram"),
         ("ngram", "text"),
         ("text", end_token)
         ])

    ngram.add(text)
    ngrams = ngram.counts

    assert ngrams == expected_ngrams

    
def test_ngram_counter_get_ngrams():
    text = "More testing testing"
    end_token = Tokenizer("").end_token
    ngram_counter = NgramCounter(1)
    ngram_counter.add(text)
    expected_ngrams = Counter([("More",), ("testing",), ("testing",), (end_token,)]).items()

    ngrams = ngram_counter.get_ngrams()

    assert ngrams == expected_ngrams
    
def test_ngram_counter_eq():
    text = "A test ngram"
    expected_ngram = NgramCounter(2)
    expected_ngram.add(text)
    
    ngram = NgramCounter(2)
    ngram.add(text)

    assert ngram == expected_ngram
    assert not (ngram != expected_ngram)

def test_ngram_counter_eq_diff():
    text = "A test ngram"
    expected_ngram = NgramCounter(2)
    expected_ngram.add("A test ngram differs")
    
    ngram = NgramCounter(2)
    ngram.add(text)

    assert ngram != expected_ngram
    assert not (ngram == expected_ngram)

def test_ngram_counter_eq_diff_sizes():
    text = "A test ngram"
    expected_ngram = NgramCounter(1)
    expected_ngram.add(text)
    
    ngram = NgramCounter(2)
    ngram.add(text)

    assert ngram != expected_ngram
    assert not (ngram == expected_ngram)
    
def test_multi_ngram_counter_get_ngrams():
    text = "A test text"
    unigram_counter = NgramCounter(1)
    unigram_counter.add(text)
    unigrams = unigram_counter.get_ngrams()
    bigram_counter = NgramCounter(2)
    bigram_counter.add(text)
    bigrams = bigram_counter.get_ngrams()
    expected_ngrams = Counter()

    for ngram, count in unigrams:
        expected_ngrams[ngram] += count
    
    for ngram, count in bigrams:
        expected_ngrams[ngram] += count
        
    ngram_counter = MultiNgramCounter(2)
    ngram_counter.add(text)
    
    ngrams = ngram_counter.get_ngrams()

    assert sorted(list(ngrams)) == sorted(list(expected_ngrams.items()))
    
def test_multi_ngram_counter_eq():
    text = "A test text"
    expected_counter = MultiNgramCounter(2)
    expected_counter.add(text)

    ngram_counter = MultiNgramCounter(2)
    ngram_counter.add(text)

    assert ngram_counter == expected_counter
    assert not (ngram_counter != expected_counter)

def test_multi_ngram_counter_eq_diff():
    text = "A test text"
    expected_counter = MultiNgramCounter(2)
    expected_counter.add("A test text differs")

    ngram_counter = MultiNgramCounter(2)
    ngram_counter.add(text)

    assert ngram_counter != expected_counter
    assert not (ngram_counter == expected_counter)
    
def test_multi_ngram_counter_add():
    text = "A test text"
    unigrams = NgramCounter(1)
    unigrams.add(text)
    bigrams = NgramCounter(2)
    bigrams.add(text)
    expected_ngrams = [unigrams, bigrams]

    ngram_collection = MultiNgramCounter(2)
    ngram_collection.add(text)
    ngrams = ngram_collection.ngram_counters

    assert ngrams == expected_ngrams
    
def test_markov_model_init():
    size = 5

    model = MarkovModel(size)

    assert model.max_ngram_size == size

def test_markov_model_reset_ngram_size():
    model = MarkovModel(1)
    new_size = 3

    model.reset_ngram_size(new_size)

    assert model.max_ngram_size == new_size

def test_markov_model_reset_ngrams():
    size = 2
    expected_ngrams = MultiNgramCounter(size)
    model = MarkovModel(size)
    model.add("some data")

    model.reset_ngrams()
    ngrams = model.ngram_counters
    
    assert ngrams == expected_ngrams

def test_markov_model_add():
    size = 2
    text = "Test text"
    expected_ngrams = MultiNgramCounter(size)
    expected_ngrams.add(text)
    model = MarkovModel(size)

    model.add(text)
    ngrams = model.ngram_counters 

    assert ngrams == expected_ngrams

def test_markov_model_add_comment():
    size = 2
    comment = get_test_comment()
    expected_ngrams = MultiNgramCounter(size)
    expected_ngrams.add(comment.get_body())
    model = MarkovModel(size)

    model.add_comment(comment)
    ngrams = model.ngram_counters

    assert ngrams == expected_ngrams
    
def test_markov_model_train():
    size = 2
    test_comment = get_test_comment()
    content = test_comment.content
    content_string = json.dumps(content)
    two_comments = "\n".join([content_string, content_string])
    handle = io.StringIO(two_comments)
    expected_ngrams = MultiNgramCounter(size)
    expected_ngrams.add(test_comment.get_body())
    expected_ngrams.add(test_comment.get_body())
    model = MarkovModel(size)
    
    model.train(handle)
    ngrams = model.ngram_counters

    assert ngrams == expected_ngrams

def test_markov_model_eq():
    size = 3
    test_comment = get_test_comment()
    expected_model = MarkovModel(size)
    expected_model.add_comment(test_comment)

    model = MarkovModel(size)
    model.add_comment(test_comment)

    assert model == expected_model
    assert not (model != expected_model)
    
def test_markov_model_eq_diff():
    size = 3
    test_comment = get_test_comment()
    expected_model = MarkovModel(size)
    expected_model.add("A totally different text")

    model = MarkovModel(size)
    model.add_comment(test_comment)

    assert model != expected_model
    assert not (model == expected_model)
    

def test_markov_model_save_load():
    size = 3
    test_comment = get_test_comment()
    expected_model = MarkovModel(size)
    expected_model.add_comment(test_comment)
    handle = io.BytesIO()
    expected_model.save(handle)
    handle.seek(0)
    
    model = MarkovModel.load(handle)

    assert model == expected_model

def test_ngram_database_connect():
    db_name = "test_ngram.db"
    ngram_db = NgramDatabase(db_name)

    assert os.path.exists(db_name)

    os.remove(db_name)

def test_ngram_database_create_table():
    db_name = "test_ngram.db"
    ngram_db = NgramDatabase(db_name)
    query = "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?"
    
    ngram_db.create_table()
    result = ngram_db.connection.execute(query, ("ngrams",))

    assert list(result) != []
