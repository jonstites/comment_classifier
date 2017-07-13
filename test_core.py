from comment_generator.core import Comment, CommentReader
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

def test_get_body():
    comment = get_test_comment()
    text = get_test_content()["body"]

    body = comment.get_body()

    assert body == text

def test_tokenization():
    comment = get_test_comment()
    text = comment.get_body()
    test_tokens = text.split()

    tokens = comment.get_tokenization()
    
    assert tokens == test_tokens

    
def test_get_unigrams():
    comment = get_test_comment()
    tokens = comment.get_tokenization()
    expected_unigrams = [(token,) for token in tokens]
    
    unigrams = list(comment.get_ngrams(1))
    
    assert unigrams == expected_unigrams
    
def test_get_bigrams():
    comment = get_test_comment()
    expected_bigrams = [("my", "test"), ("test", "comment")]

    bigrams = list(comment.get_ngrams(2))

    assert bigrams == expected_bigrams

def test_get_trigrams():
    comment = get_test_comment()
    expected_trigrams = [("my", "test", "comment")]

    trigrams = list(comment.get_ngrams(3))

    assert trigrams == expected_trigrams
    
