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
    handle = io.StringIO()
    test_content = test_comment.content
    
    json.dump(test_content, handle)

    for comment in CommentReader.from_file(handle):
        assert comment.content == test_content
