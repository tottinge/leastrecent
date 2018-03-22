import re


class FileLineParser(object):
    file_line_regex = re.compile("\d+\s+\d+\s+(\S+)")

    def __init__(self, text):
        self.text = text

    def filename(self):
        m = self.file_line_regex.match(self.text)
        if not m:
            return None
        return m.group(1)