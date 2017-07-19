from comment_generator.core import Comment, CommentReader, Ngram, Tokenizer
from collections import Counter
import json
import io

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

def test_comment_reader_from_file():
    test_comment = get_test_comment()
    content = test_comment.content
    content_string = json.dumps(content)

    handle = io.StringIO(content_string)    

    count = 0
    for comment in CommentReader.from_file(handle):
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

def test_ngram_add():
    text = "A text ngram text"
    ngram = Ngram(2)
    tokenizer = Tokenizer("")
    pad_token = tokenizer.pad_token
    end_token = tokenizer.end_token
    expected_ngrams = Counter(
        [(pad_token, "A"),
         ("A", "text"),
         ("text", "ngram"),
         ("ngram", "text"),
         ("text", end_token)
         ])


    ngram.add(text)
    ngrams = ngram.ngrams

    assert ngrams == expected_ngrams
