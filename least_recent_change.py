import fileinput
from datetime import datetime, timezone, timedelta

from lib.dateparser import DateParser
from lib.filelineparser import FileLineParser

def get_date(line):
    return DateParser(line).date()

def get_file(line):
    return FileLineParser(line).filename()

def most_recent_change(source):
    dates = {}
    current_date = None
    ancient_history = datetime(1, 1, 1, 1, 1, 1, 1, timezone(-timedelta(hours=4)))
    for line in source:
        current_date = get_date(line) or current_date
        file = get_file(line)
        if file:
            if current_date > dates.get(file, ancient_history):
                dates[file] = current_date
    return dates


def least_recent_change(source):
    dates = {}
    current_date = None
    for line in source:
        current_date = get_date(line) or current_date
        file = get_file(line)
        if file:
            if current_date < dates.get(file, datetime.now().astimezone()):
                dates[file] = current_date
    return dates

def main():
    result = most_recent_change(fileinput.input())
    print("Ordered by least recent")
    for (filename, time) in sorted(result.items(), key=lambda x: x[1]):
        print('\t', filename, '\t', time.date())

if __name__ == '__main__':
    main()