import operator
import traceback
from hopy.const import TOKEN_EXPRS, TokenType, Identifier, OP_TYPE_MAPPING, OperatorType, OP_PRECEDENCE
from hopy.lexer import Tokenizer


class ASTNode:
    def __init__(self, token, children=None):
        if children is None:
            children = []
        self.token = token
        self.children = children

    def __repr__(self, level=0):
        tabs = '\t' * level
        child_repr = "".join([child.__repr__(level + 1) for child in self.children])
        return f'{tabs}- {self.token.value}\n{child_repr}'


class ActionTreeNode:
    def __init__(self, ast_node, action, children=None, variable=False):
        if children is None:
            children = []
        self.ast_node = ast_node
        self.action = action
        self.variable = variable
        self.children = children


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.op_stack = []
        self.nodes = []

    @staticmethod
    def _precedent(token1, token2):
        return OP_PRECEDENCE.get(token1.identifier, 99) <= OP_PRECEDENCE.get(token2.identifier, 99)

    def _backtrack(self):
        last_op = self.op_stack.pop()
        if OP_TYPE_MAPPING[last_op.identifier] == OperatorType.UNARY:
            operands = [self.nodes.pop()]
            self.nodes.append(ASTNode(last_op, operands))
        elif OP_TYPE_MAPPING[last_op.identifier] == OperatorType.BINARY:
            operand2 = self.nodes.pop()
            operand1 = self.nodes.pop()
            operands = [operand1, operand2]
            self.nodes.append(ASTNode(last_op, operands))
        else:
            raise Exception("Invalid operator encountered on stack")

    def parse(self):
        for token in self.tokens:
            if token.ttype == TokenType.OPERATOR:
                while len(self.op_stack) != 0 and self._precedent(self.op_stack[-1], token):
                    self._backtrack()
                self.op_stack.append(token)
            elif token.ttype == TokenType.SEPARATOR:
                if token.identifier == Identifier.OPEN_BRACE:
                    self.op_stack.append(token)
                elif token.identifier == Identifier.COMMA:
                    while len(self.op_stack) != 0 and self.op_stack[-1].ttype != TokenType.SEPARATOR:
                        self._backtrack()
                    self.op_stack.append(token)
                elif token.identifier == Identifier.CLOSE_BRACE:
                    while len(self.op_stack) != 0 and self.op_stack[-1].ttype != TokenType.SEPARATOR:
                        self._backtrack()

                    operands = []
                    while len(self.op_stack) != 0 and self.op_stack[-1].identifier != Identifier.OPEN_BRACE:
                        last_op = self.op_stack.pop()
                        if last_op.identifier == Identifier.COMMA:
                            operands.append(self.nodes.pop())
                        else:
                            raise Exception("Invalid operator found on stack")

                    if len(self.op_stack) == 0 or self.op_stack[-1].identifier != Identifier.OPEN_BRACE:
                        raise Exception("Invalid closing parenthesis")

                    else:
                        operands.append(self.nodes.pop())
                        self.op_stack.pop()

                    operands.reverse()
                    if len(self.op_stack) != 0 and OP_TYPE_MAPPING[self.op_stack[-1].identifier] == OperatorType.NARY:
                        self.nodes.append(ASTNode(self.op_stack.pop(), operands))
                    else:
                        self.nodes.append(operands[0])

            else:
                self.nodes.append(ASTNode(token))

        while len(self.op_stack) != 0:
            self._backtrack()

        return self.nodes[0]


class ActionTreeGenerator:
    def __init__(self, ast):
        self._ast = ast
        self._ast_act_map = {}

    @staticmethod
    def _get_equals_action(token):
        return operator.eq, False

    @staticmethod
    def _get_not_equals_action(token):
        return operator.ne, False

    @staticmethod
    def _get_greater_equals_action(token):
        return operator.ge, False

    @staticmethod
    def _get_greater_action(token):
        return operator.gt, False

    @staticmethod
    def _get_lesser_equals_action(token):
        return operator.le, False

    @staticmethod
    def _get_lesser_action(token):
        return operator.lt, False

    @staticmethod
    def _get_and_action(token):
        return (lambda a, b: a and b), False

    @staticmethod
    def _get_or_action(token):
        return (lambda a, b: a or b), False

    @staticmethod
    def _get_not_action(token):
        return operator.not_, False

    @staticmethod
    def _get_jsonpath_action(token):
        return (lambda x, y: x.find(y)[0].value), True

    @staticmethod
    def _get_function_action(token):
        import math, re
        name_function_map = {
            'f.abs': (abs, False),
            'f.max': (max, False),
            'f.min': (min, False),
            'f.ceil': (math.ceil, False),
            'f.floor': (math.floor, False),
            'f.add': (operator.add, False),
            'f.mul': (operator.mul, False),
            'f.sub': (operator.sub, False),
            'f.floordiv': (operator.floordiv, False),
            'f.truediv': (operator.truediv, False),
            'f.pow': (math.pow, False),
            'f.match': ((lambda a, b: bool(re.match(a, b))), False),
            'f.len': (len, False),
            'f.upper': ((lambda a: a.upper()), False),
            'f.lower': ((lambda a: a.lower()), False),
            'f.in': (operator.contains, False),
        }
        if token.value in name_function_map.keys():
            return name_function_map[token.value]

        raise Exception("Invalid function found")

    def _get_action(self, token):
        if token.ttype in (TokenType.OPERATOR, TokenType.EXTERNAL):
            return getattr(self, f'_get_{token.identifier.lower()}_action')(token)
        elif token.ttype == TokenType.LITERAL:
            return token.value, False
        else:
            raise Exception("Invalid token type")

    def _get_act_node_shallow(self, ast_node):
        action, variable = self._get_action(ast_node.token)
        return ActionTreeNode(ast_node, action, variable=variable)

    def _inorder(self, ast_node):
        act_node = self._get_act_node_shallow(ast_node)
        for child in ast_node.children:
            act_node.children.append(self._inorder(child))

        return act_node

    def generate_actions(self):
        return self._inorder(self._ast)


if __name__ == '__main__':
    while True:
        inp = input("> Enter an expression to lex:\n> ")
        try:
            tokens = Tokenizer(TOKEN_EXPRS, inp).tokenize()
            print(tokens)
            ast = Parser(tokens).parse()
            print(ast)
        except Exception as e:
            traceback.print_exc()
