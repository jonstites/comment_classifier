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

    def from_file(opened_handle):
        for comment_line in opened_handle:
            decoded_line = comment_line.decode("utf-8")
            comment = self.from_string(decoded_line)
            yield comment
