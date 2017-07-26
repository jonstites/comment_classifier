from comment_generator.core import Comment, CommentReader, Ngram, Tokenizer, MarkovModel, NgramDatabase
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

def get_pad_token():
    return Tokenizer.pad_token

def get_end_token():
    return Tokenizer.end_token

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

    tokens = Tokenizer.tokens(text)
    
    assert tokens == test_tokens

def test_tokenizer_padded_tokens():
    text = "A test text"
    pad_token = get_pad_token()
    ngram_size = 3
    expected_tokens = [pad_token, pad_token, "A", "test", "text"]
    
    tokens = Tokenizer.padded_tokens(text, ngram_size)

    assert tokens == expected_tokens

def test_tokenizer_padded_tokens_unigram():
    text = "A test text"
    ngram_size = 1
    expected_tokens = ["A", "test", "text"]

    tokens = Tokenizer.padded_tokens(text, 1)

    assert tokens == expected_tokens

def test_tokenizer_padded_tokens_with_end():
    text = "A test text"
    pad_token = get_pad_token()
    end_token = get_end_token()
    ngram_size = 2
    expected_tokens = [pad_token, "A", "test", "text", end_token]

    tokens = Tokenizer.padded_tokens_with_end(text, ngram_size)

    assert tokens == expected_tokens

def test_ngram_enumerate_ngrams():
    tokens = ["a", "b", "cde"]
    expected_ngrams = [Ngram((token,)) for token in tokens]
    ngram_size = 1

    ngrams = list(Ngram.enumerate_ngrams(tokens, 1))

    print([ngram.tokens for ngram in ngrams])
    print([ngram.tokens for ngram in expected_ngrams])

    assert ngrams == expected_ngrams    
    
def test_markov_model_init():
    size = 5

    model = MarkovModel(size)

    assert model.max_ngram_size == size

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
    os.remove(db_name)
    
    assert list(result) != []
