import re
import traceback

from hopy.const import TokenType, Identifier, TOKEN_EXPRS


class Token:
    def __init__(self, value, ttype, identifier, start):
        self.value = value
        self.ttype = ttype
        self.identifier = identifier
        self.start = start

    def __repr__(self):
        return f'Token({self.value!r}, {self.ttype!r}, {self.identifier!r}, {self.start!r})'


class IllegalInputException(Exception):
    pass


class Tokenizer:
    def __init__(self, inp, token_exprs=TOKEN_EXPRS, jsonpath_parser=None):
        self.compiled_token_exprs = self._compile_token_exprs(token_exprs)
        self.inp = inp
        self.i = 0
        self.tokens = []
        self.context = []
        self.jsonpath_parser = jsonpath_parser or self._default_jsonpath_parser()

    @staticmethod
    def _default_jsonpath_parser():
        from jsonpath_ng import parse as jsonpath_parse
        return jsonpath_parse

    @staticmethod
    def _compile_token_exprs(token_exprs):
        return [(re.compile(pattern), identifier, ttype) for pattern, identifier, ttype in token_exprs]

    def _next_match(self):
        max_match = None

        for regex, identifier, ttype in self.compiled_token_exprs:
            regex_match = regex.match(self.inp, self.i)
            if regex_match and (max_match is None or regex_match.end(0) > max_match[0].end(0)):
                max_match = (regex_match, identifier, ttype)

        if not max_match:
            raise IllegalInputException(f"Illegal character '{self.inp[self.i]}' encountered at position {self.i}")

        return max_match

    def _create_token(self, match):
        regex_match, identifier, ttype = match
        if ttype != TokenType.SKIP:
            if identifier == Identifier.OPEN_BRACE:
                self.context.append(Identifier.OPEN_BRACE)
                self.tokens.append(Token(regex_match.group(0), ttype, identifier, self.i))
            elif identifier == Identifier.CLOSE_BRACE:
                if self.context and self.context[-1] != Identifier.OPEN_BRACE:
                    raise IllegalInputException(f"Unmatched parenthesis at {self.i}")
                else:
                    self.context.pop()
                    self.tokens.append(Token(regex_match.group(0), ttype, identifier, self.i))
            elif identifier == Identifier.NUMBER:
                value = float(regex_match.group(0))
                self.tokens.append(Token(value, ttype, identifier, self.i))
            elif identifier == Identifier.STRING:
                value = regex_match.group(0)[1:-1]
                self.tokens.append(Token(value, ttype, identifier, self.i))
            elif identifier == Identifier.BOOLEAN:
                value = regex_match.group(0) in ('true', "TRUE", "True")
                self.tokens.append(Token(value, ttype, identifier, self.i))
            elif identifier == Identifier.JSONPATH:
                jsonpath_str = regex_match.group(0)[1:-1]
                value = self.jsonpath_parser(jsonpath_str)
                self.tokens.append(Token(value, ttype, identifier, self.i))
            else:
                self.tokens.append(Token(regex_match.group(0), ttype, identifier, self.i))

        self.i = regex_match.end(0)

    def tokenize(self):
        while self.i < len(self.inp):
            match = self._next_match()
            self._create_token(match)

        return self.tokens


if __name__ == '__main__':
    while True:
        inp = input("> Enter an expression to lex:\n> ")
        try:
            print(Tokenizer(inp).tokenize())
        except Exception as e:
            traceback.print_exc()
