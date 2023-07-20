from typing import TextIO


class QuotesFormatter:
    def __init__(self, quotes_filename: str):
        self._quotes_filename: str = quotes_filename
        self._markdown: str = ''
        self._current_quote: str = ''
        self._current_comment: str = ''
        self._is_line_quote: bool = True
        self._is_line_comment: bool = False

    def _read_headers(self, quotes_file: TextIO):
        title = quotes_file.readline()
        author = quotes_file.readline()
        self._markdown = f'# {title}\n' f'## {author}\n'

    def _process_five_stars(self):
        if self._is_line_quote:
            self._markdown += f'{self._current_quote}\n'
            self._current_quote = ''

        elif self._is_line_comment:
            self._markdown += f'{self._current_comment}\n'
            self._is_line_quote = True
            self._is_line_comment = False
            self._current_comment = ''

        self._markdown += '***\n'

    def _process_two_hypens(self):
        self._markdown += f'{self._current_quote}\n'
        self._current_quote = ''

        self._is_line_quote = False
        self._is_line_comment = True

    def _process_text(self, text: str):
        if self._is_line_quote:
            self._current_quote += f'> {text}\n'
        elif self._is_line_comment:
            self._current_comment += f'{text}\n'

    def process(self):
        with open(self._quotes_filename, 'r') as quotes_file:
            self._read_headers(quotes_file)

            while line := quotes_file.readline():
                line = line.strip()

                if line == '*****':
                    self._process_five_stars()
                elif line == '--':
                    self._process_two_hypens()
                elif line:
                    self._process_text(line)

        return self._markdown


if __name__ == "__main__":
    quotes_formatter = QuotesFormatter('quotes.txt')
    markdown = quotes_formatter.process()
    with open('quotes.md', 'w') as quotes_md:
        quotes_md.write(markdown)
