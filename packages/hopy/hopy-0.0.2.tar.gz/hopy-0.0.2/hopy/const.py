class Pattern:
    BLANK_SPACE = r'[ \n\r\t]+'
    COMMA = r','
    OPEN_BRACE = r'\('
    CLOSE_BRACE = r'\)'
    EQUALS = r'=='
    NOT_EQUALS = r'!='
    GREATER_EQUALS = r'>='
    GREATER = r'>'
    LESSER_EQUALS = r'<='
    LESSER = r'<'
    AND = r'&&'
    OR = r'\|\|'
    NOT = r'!'
    NUMBER = r'[+-]?(\d*\.)?\d+'
    BOOLEAN = r'true|false|TRUE|FALSE|True|False'
    STRING = r"\"([^\"\\\n]|\\.|\\\n)*\"|'([^'\\\n]|\\.|\\\n)*'"
    JSONPATH = r'`([^`\\\n]|\\.|\\\n)*`'
    FUNCTION = r'f.[a-z]\w+'


class Identifier:
    BLANK_SPACE = 'BLANK_SPACE'
    COMMA = 'COMMA'
    OPEN_BRACE = 'OPEN_BRACE'
    CLOSE_BRACE = 'CLOSE_BRACE'
    EQUALS = 'EQUALS'
    NOT_EQUALS = 'NOT_EQUALS'
    GREATER_EQUALS = 'GREATER_EQUALS'
    GREATER = 'GREATER'
    LESSER_EQUALS = 'LESSER_EQUALS'
    LESSER = 'LESSER'
    AND = 'AND'
    OR = 'OR'
    NOT = 'NOT'
    NUMBER = 'NUMBER'
    BOOLEAN = 'BOOLEAN'
    STRING = 'STRING'
    JSONPATH = 'JSONPATH'
    FUNCTION = 'FUNCTION'


class TokenType:
    EXTERNAL = 'EXTERNAL'
    LITERAL = 'LITERAL'
    OPERATOR = 'OPERATOR'
    SEPARATOR = 'SEPARATOR'
    SKIP = 'SKIP'


class OperatorType:
    UNARY = 'UNARY'
    BINARY = 'BINARY'
    NARY = 'NARY'


TOKEN_EXPRS = (
    (Pattern.BLANK_SPACE, Identifier.BLANK_SPACE, TokenType.SKIP),
    (Pattern.COMMA, Identifier.COMMA, TokenType.SEPARATOR),
    (Pattern.OPEN_BRACE, Identifier.OPEN_BRACE, TokenType.SEPARATOR),
    (Pattern.CLOSE_BRACE, Identifier.CLOSE_BRACE, TokenType.SEPARATOR),
    (Pattern.EQUALS, Identifier.EQUALS, TokenType.OPERATOR),
    (Pattern.NOT_EQUALS, Identifier.NOT_EQUALS, TokenType.OPERATOR),
    (Pattern.GREATER_EQUALS, Identifier.GREATER_EQUALS, TokenType.OPERATOR),
    (Pattern.GREATER, Identifier.GREATER, TokenType.OPERATOR),
    (Pattern.LESSER_EQUALS, Identifier.LESSER_EQUALS, TokenType.OPERATOR),
    (Pattern.LESSER, Identifier.LESSER, TokenType.OPERATOR),
    (Pattern.AND, Identifier.AND, TokenType.OPERATOR),
    (Pattern.OR, Identifier.OR, TokenType.OPERATOR),
    (Pattern.NOT, Identifier.NOT, TokenType.OPERATOR),
    (Pattern.NUMBER, Identifier.NUMBER, TokenType.LITERAL),
    (Pattern.BOOLEAN, Identifier.BOOLEAN, TokenType.LITERAL),
    (Pattern.STRING, Identifier.STRING, TokenType.LITERAL),
    (Pattern.JSONPATH, Identifier.JSONPATH, TokenType.EXTERNAL),
    (Pattern.FUNCTION, Identifier.FUNCTION, TokenType.OPERATOR),
)

OP_TYPE_MAPPING = {
    Identifier.FUNCTION: OperatorType.NARY,
    Identifier.NOT: OperatorType.UNARY,
    Identifier.EQUALS: OperatorType.BINARY,
    Identifier.NOT_EQUALS: OperatorType.BINARY,
    Identifier.GREATER_EQUALS: OperatorType.BINARY,
    Identifier.GREATER: OperatorType.BINARY,
    Identifier.LESSER_EQUALS: OperatorType.BINARY,
    Identifier.LESSER: OperatorType.BINARY,
    Identifier.AND: OperatorType.BINARY,
    Identifier.OR: OperatorType.BINARY,
}

OP_PRECEDENCE = {
    Identifier.EQUALS: 2,
    Identifier.NOT_EQUALS: 2,
    Identifier.GREATER_EQUALS: 2,
    Identifier.GREATER: 2,
    Identifier.LESSER_EQUALS: 2,
    Identifier.LESSER: 2,
    Identifier.AND: 3,
    Identifier.OR: 3,
    Identifier.NOT: 1,
    Identifier.FUNCTION: 0,
}
