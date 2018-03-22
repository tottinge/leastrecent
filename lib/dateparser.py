import re
from datetime import datetime


class DateParser(object):
    date_regex = re.compile('(\w{3} \w{3} \d+ \d+:\d+:\d+ \d{4} [+-]\d{4})')

    def __init__(self, text):
        self.text = text

    def has_date(self):
        return self.date_regex.search(self.text)

    def date(self):
        m = self.has_date()
        if not m:
            return None
        pattern = m.group(1)
        return datetime.strptime(pattern, "%a %b %d %H:%M:%S %Y %z")