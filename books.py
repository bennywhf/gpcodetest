#!/usr/bin/python
from optparse import OptionParser


class Book:
    def __init__(self, author_first_name, author_last_name, book_title, book_publicatoin_date):
        self.auth_first_name = author_first_name.strip()
        self.auth_last_name = author_last_name.strip()
        self.title = book_title.strip()
        self.publication_date = book_publicatoin_date.strip()

    def filter(self, text):
        return text.lower() in str(self).lower()

    def __str__(self):
        return '%s %s %s %s' % (self.auth_first_name, self.auth_last_name, self.title, self.publication_date )


class BookShelf:
    book_container = []

    @classmethod
    def parse_csv_line(cls, line):
        title, last_name, first_name, year = line.strip('\n').split(',')
        cls.book_container.append(Book(first_name, last_name, title, year))

    @classmethod
    def parse_pipe_line(cls, line):
        first_name, last_name, title, year = line.strip('\n').split('|')
        cls.book_container.append(Book(first_name, last_name, title, year))

    @classmethod
    def parse_slash_line(cls, line):
        year, first_name, last_name, title = line.strip('\n').split('/')
        cls.book_container.append(Book(first_name, last_name, title, year))

    @classmethod
    def parse_files(cls, csv_file_path, pipe_file_path, slash_file_path):
        with open(csv_file_path, 'r') as csv_file:
            for line in csv_file:
                cls.parse_csv_line(line)

        with open(slash_file_path, 'r') as slash_file:
            for line in slash_file:
                cls.parse_slash_line(line)

        with open(pipe_file_path, 'r') as pipe_file:
            for line in pipe_file:
                cls.parse_pipe_line(line)

        cls.book_container = sorted(cls.book_container, key=lambda book: book.auth_last_name)

    @classmethod
    def filter(cls, text):
        cls.book_container = [book for book in cls.book_container if book.filter(text)]

    @classmethod
    def reverse(cls):
        cls.book_container = sorted(cls.book_container, reverse=True)

    @classmethod
    def sort_by_year(cls):
        cls.book_container = sorted(cls.book_container, key=lambda book: book.publication_date)

    @classmethod
    def get_results(cls):
        return '\n'.join(str(book) for book in cls.book_container)

    @classmethod
    def act(cls, options):
        cls.parse_files(csv_file_path=options.csv_file, pipe_file_path=options.pipe_file, slash_file_path=options.slash_file)

        if options.filter_text:
            cls.filter(options.filter_text)

        if options.sort_by_year:
            cls.sort_by_year()

        if options.reverse:
            cls.reverse()

        return cls.get_results()


def main():
    parser = OptionParser()
    parser.add_option("-f", "--filter", dest="filter_text",
                      help="Text to filter results by.", metavar="TEXT")

    parser.add_option("-r", "--reverse",
                      action="store_true", dest="reverse", default=False,
                      help="Reverse results.")

    parser.add_option("-y", "--year", dest="sort_by_year", action="store_true",
                      help="Sort results by year", default=False)

    parser.add_option("--csv",
                      dest="csv_file", default="csv", metavar="CSV_FILE",
                      help="Path to CSV file.")

    parser.add_option("--slash",
                      dest="slash_file", default="slash", metavar="SLASH_FILE",
                      help="Path to SLASH file.")

    parser.add_option("--pipe",
                      dest="pipe_file", default="pipe", metavar="PIPE_FILE",
                      help="Path to PIPE file.")

    options, args = parser.parse_args()

    print(BookShelf.act(options))
if __name__ == '__main__':
    main()
