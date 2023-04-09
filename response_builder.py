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


class ResponseBuilder:
    def __init__(self):
        self.__tokens = []
        self.__logger = logging.getLogger('ResponseBuilder')

    def append_token(self, token):
        self.__tokens.append(token)

    def to_string(self):
        text = ''.join(self.__tokens)
        return ''.join(self.__split_by_type(text, code_delimiter='```'))

    def __split_by_type(self, text, code_delimiter):
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

                self.__logger.info('code: %s', code_snippet)

                yield code_snippet
            elif code_delimiter == '```':
                for subpart in self.__split_by_type(part, code_delimiter='`'):
                    yield subpart
            else:
                escaped_text = escape_string_for_markdown2(part)
                self.__logger.info('text: %s', escaped_text)
                yield escaped_text

            is_code_snippet = not is_code_snippet
