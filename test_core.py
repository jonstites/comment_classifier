from comment_generator.core import Comment, CommentReader
import json
import io

def test_comment_from_string():
    content = {
        "body": "my test comment",
        "subreddit": "my_test_subreddit"
        }
    content_string = json.dumps(content)
    
    comment = Comment.from_string(content_string)

    assert comment.content["body"] == "my test comment"
    assert comment.content["subreddit"] == "my_test_subreddit"

"""    
def test_comment_reader_from_file():
    test_comments = generate_test_comments()
    handle = setup_handle()

    output_comments = CommentReader.from_file(handle)
    zipped_comments = zip(test_comments, output_comments)
    
    for test_comment, output_comment in zipped_comments:
        assert test_comment == output_comment

    
def test_comment_reader_line_to_comment():
    body = "The test body"
    subreddit = "faked"
    test_comment = {"body": body, "subreddit": subreddit}
    test_comment_string = json.dumps(test_comment)

    comment_reader = CommentReader("fake_file.txt")
    comment = comment_reader.line_to_comment(test_comment_string)
    assert comment.body == body
    assert comment.subreddit == subreddit

"""
