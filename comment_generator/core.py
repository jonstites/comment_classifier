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
        for line in opened_handle:
            comment = Comment.from_string(line)
            yield comment
