import argparse
import logging
import os
from typing import TextIO


class QuotesFormatter:
    def __init__(self, quotes_filename: str):
        self._quotes_filename: str = quotes_filename
        self._markdown: str = ''
        self._current_quote: str = ''
        self._current_comment: str = ''
        self._is_line_quote: bool = True
        self._is_line_comment: bool = False

    def _read_headers(self, quotes_file: TextIO) -> None:
        title: str = quotes_file.readline()
        author: str = quotes_file.readline()
        self._markdown = f'# {title}\n' f'## {author}\n'

    def _process_five_stars(self) -> None:
        if self._is_line_quote:
            self._markdown += f'{self._current_quote}\n'
            self._current_quote = ''

        elif self._is_line_comment:
            self._markdown += f'{self._current_comment}\n'
            self._is_line_quote = True
            self._is_line_comment = False
            self._current_comment = ''

        self._markdown += '***\n'

    def _process_two_hypens(self) -> None:
        self._markdown += f'{self._current_quote}\n'
        self._current_quote = ''

        self._is_line_quote = False
        self._is_line_comment = True

    def _process_text(self, text: str) -> None:
        if self._is_line_quote:
            self._current_quote += f'> {text}\n'
        elif self._is_line_comment:
            self._current_comment += f'{text}\n'

    def process(self) -> str:
        if not os.path.exists(self._quotes_filename):
            raise FileNotFoundError

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


def parse_arguments() -> tuple[str, str]:
    parser = argparse.ArgumentParser(
        prog='Script to format quotes from a text file to markdown',
        description='Main usage is to export ReadEra quotes to Notion',
    )

    parser.add_argument(
        '--input_file',
        '-i',
        type=str,
        default='quotes.txt',
        help='Name of the input file with quotes. By default "quotes.txt"',
    )
    parser.add_argument(
        '--output_file',
        '-o',
        type=str,
        default='quotes.md',
        help='Name of the output file with quotes. By default "quotes.md"',
    )

    args = parser.parse_args()
    quotes_file: str = args.input_file
    quotes_md: str = args.output_file

    return quotes_file, quotes_md


if __name__ == "__main__":
    quotes_file, quotes_md = parse_arguments()

    quotes_formatter = QuotesFormatter(quotes_file)

    try:
        markdown = quotes_formatter.process()
    except FileNotFoundError:
        logging.error(f'File {quotes_file} not found')
    else:
        with open(quotes_md, 'w') as quotes_md:
            quotes_md.write(markdown)
