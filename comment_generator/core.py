#!/usr/bin/env python3

import bz2
import json

class Comment:

    def __init__(self, content):
        self.content = content

    def from_string(comment):
        content = json.loads(comment)
        return Comment(content)

    
class CommentReader:

    def get_comments(self, input_handle):
        for comment in from_file(input_handle):
            yield comment

    def from_file(self, input_handle):
        for comment_line in opened_file:
            decoded_line = comment_line.decode("utf-8")
            comment = self.from_string(decoded_line)
            yield comment


#        with bz2.BZ2File(self.comment_file, "r") as opened_file:
