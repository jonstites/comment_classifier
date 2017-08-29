from comment_generator.core import Comment, CommentReader, MarkovModel
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

def test_comment_get_subreddit():
    comment = get_test_comment()
    expected_subreddit = get_test_content()["subreddit"]

    subreddit = comment.get_subreddit()

    assert expected_subreddit == subreddit

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
