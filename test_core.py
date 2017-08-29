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

def test_comment_reader_get_batch():
    test_comment = get_test_comment()
    content = test_comment.content
    content_string = json.dumps(content)

    handle = io.StringIO(content_string + "\n" + content_string)

    batch_count = 0
    comment_count = 0
    for batch in CommentReader.get_batch(handle, 2):
        batch_count += 1
        for comment in batch:
            comment_count += 1

    assert batch_count == 1            
    assert comment_count == 2

def test_comment_reader_get_batch_by_subreddit_diff():
    test_comment = get_test_comment()
    test_subreddit = test_comment.get_subreddit()
    different_subreddit = test_subreddit + "different_string"
    use_subreddits = set([different_subreddit])
    content = test_comment.content
    content_string = json.dumps(content)
    handle = io.StringIO(content_string + "\n" + content_string)

    batch_count = 0
    comment_count = 0
    for batch in CommentReader.get_batch(handle, 2, use_subreddits):
        batch_count += 1
        for comment in batch:
            comment_count += 1

    assert batch_count == 0
    assert comment_count == 0
    
def test_comment_reader_get_batch_by_subreddit_same():
    test_comment = get_test_comment()
    test_subreddit = test_comment.get_subreddit()
    same_subreddit = test_subreddit
    use_subreddits = set([same_subreddit])
    content = test_comment.content
    content_string = json.dumps(content)
    handle = io.StringIO(content_string + "\n" + content_string)

    batch_count = 0
    comment_count = 0
    for batch in CommentReader.get_batch(handle, 2, use_subreddits):
        batch_count += 1
        for comment in batch:
            comment_count += 1

    assert batch_count == 1
    assert comment_count == 2
    
def test_comment_reader_get_subreddit_counts():
    test_comment = get_test_comment()
    subreddit = test_comment.get_subreddit()
    content = test_comment.content
    content_string = json.dumps(content)
    test_counts = Counter([subreddit, subreddit])
    handle = io.StringIO(content_string + "\n" + content_string)

    counts = CommentReader.get_subreddit_counts(handle)
    
    assert counts == test_counts
