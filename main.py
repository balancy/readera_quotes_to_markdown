if __name__ == "__main__":
    current_quote = ''
    current_comment = ''
    is_quote = True
    is_comment = False
    with open('quotes.txt', 'r') as quotes_file:
        title = quotes_file.readline()
        author = quotes_file.readline()
        markdown = f'# {title}\n' f'## {author}\n'

        while line := quotes_file.readline():
            line = line.strip()

            if line == '*****':
                if is_quote:
                    markdown += f'{current_quote}\n'
                    current_quote = ''
                elif is_comment:
                    markdown += f'{current_comment}\n'
                    is_quote = True
                    is_comment = False
                    current_comment = ''

                markdown += '***\n'

            elif line == '--':
                markdown += f'{current_quote}\n'
                current_quote = ''

                is_quote = False
                is_comment = True
                # current_comment = ''
                # elif is_comment:
                #     markdown += f'{current_comment}\n'

            elif line:
                if is_quote:
                    current_quote += f'> {line}\n'
                elif is_comment:
                    current_comment += f'{line}\n'

    with open('quotes.md', 'w') as quotes_md:
        quotes_md.write(markdown)
