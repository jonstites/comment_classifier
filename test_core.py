from comment_generator.core import Comment, CommentReader
import json
import io

def get_test_comment():
    content = {
        "body": "my test comment",
        "subreddit": "my_test_subreddit"
    }
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

def test_tokenization():
    text = "The dog bit the boy. The boy bit the dog."
    test_tokens = text.split()
    content = {"body": text}
    comment = Comment(content)

    tokens = comment.get_tokenization()
    
    assert tokens == test_tokens

def test_get_body():
    text = "test get body"
    comment = Comment({"body": text})

    body = comment.get_body()

    assert body == text
    
def test_get_unigrams():
    text = "The dog bit the boy. The boy bit the dog."
    comment = Comment({"body": text})
    tokens = comment.get_tokenization()
    expected_unigrams = [(token,) for token in tokens]
    
    unigrams = list(comment.get_ngrams(1))
    
    assert unigrams == expected_unigrams
    
