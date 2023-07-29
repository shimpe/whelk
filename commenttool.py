import re


class CommentTool(object):
    def __init__(self):
        self.cCommentPattern = r"/\*.*?\*/"
        self.rx = re.compile(self.cCommentPattern, re.DOTALL)

    def replace(self, x):
        y = x.group(0)
        if y.startswith("/"):
            return ""
        return y

    def strip_comments(self, fromString):
        return self.rx.sub(self.replace, fromString)

    def comments_iterator(self, fromString):
        return self.rx.finditer(fromString)

    def comments(self, fromString):
        c = self.rx.finditer(fromString)
        return [ c.group(0) for c in self.comments_iterator(fromString) if c.group(0).startswith("/") ]
