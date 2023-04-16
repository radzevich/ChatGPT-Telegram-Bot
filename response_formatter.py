# escape '_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!'
# to be able to use Markdown2 style for Telegram messages
# (https://core.telegram.org/api/entities)
import logging


def escape_string_for_markdown2(token):
    return token \
        .replace('.', '\\.') \
        .replace('_', '\\_') \
        .replace('*', '\\*') \
        .replace('[', '\\[') \
        .replace(']', '\\]') \
        .replace('(', '\\(') \
        .replace(')', '\\)') \
        .replace('~', '\\~') \
        .replace('>', '\\>') \
        .replace('#', '\\#') \
        .replace('+', '\\+') \
        .replace('-', '\\-') \
        .replace('=', '\\=') \
        .replace('|', '\\|') \
        .replace('{', '\\{') \
        .replace('}', '\\}') \
        .replace('!', '\\!') \
        .replace('`', '\\`')


def to_markdown2_string(raw_text):

    def formatter(text, code_delimiter):
        parts = filter(None, text.split(code_delimiter))

        is_code_snippet = False
        for part in parts:
            if is_code_snippet:
                code_snippet = '```' + part
                if code_snippet.endswith('``'):     # ``` code `` -> ``` code ```
                    code_snippet += '`'
                elif code_snippet.endswith('`'):    # ``` code `  -> ``` code ```
                    code_snippet += '``'
                else:                               # ``` code    -> ``` code ```
                    code_snippet += '```'

                yield code_snippet
            elif code_delimiter == '```':
                for subpart in formatter(part, code_delimiter='`'):
                    yield subpart
            else:
                escaped_text = escape_string_for_markdown2(part)
                yield escaped_text

            is_code_snippet = not is_code_snippet

    return ''.join(formatter(raw_text, code_delimiter='```'))
