from comment_generator.core import Comment, CommentReader
import json
import io

def get_test_comment():
    content = {
        "body": "my test comment",
        "subreddit": "my_test_subreddit"
    }
    return Comment

def test_comment_from_string():
    content = {
        "body": "my test comment",
        "subreddit": "my_test_subreddit"
        }
    content_string = json.dumps(content)
    
    comment = Comment.from_string(content_string)

    assert comment.content["body"] == "my test comment"
    assert comment.content["subreddit"] == "my_test_subreddit"

def test_comment_reader_from_file():
    test_comment = get_test_comment()
    handle = io.StringIO()
    content = {
        "body": "my test comment",
        "subreddit": "my_test_subreddit"
        }
    json.dump(content, handle)

    for test_comment in CommentReader.from_file(handle):
        assert test_comment.content == content
