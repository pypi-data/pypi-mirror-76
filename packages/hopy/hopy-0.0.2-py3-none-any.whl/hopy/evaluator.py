import traceback

from hopy.const import TokenType
from hopy.lexer import Tokenizer
from hopy.parser import Parser, ActionTreeGenerator


class HopyEvaluator:
    def __init__(self, rules, tokenizer=Tokenizer, parser=Parser, action_tree_generator=ActionTreeGenerator):
        tokens = tokenizer(rules).tokenize()
        ast = parser(tokens).parse()
        self._action_tree = action_tree_generator(ast).generate_actions()

    def _inorder_evaluate(self, act_node, rule_input):
        if act_node.ast_node.token.ttype == TokenType.LITERAL:
            return act_node.ast_node.token.value
        elif act_node.ast_node.token.ttype == TokenType.EXTERNAL:
            return act_node.action(act_node.ast_node.token.value, rule_input)
        else:
            return act_node.action(*[self._inorder_evaluate(child, rule_input) for child in act_node.children])

    def evaluate(self, rule_input):
        return self._inorder_evaluate(self._action_tree, rule_input)


if __name__ == '__main__':
    while True:
        inp = input("> Enter an expression to lex:\n> ")
        try:
            evaluator = HopyEvaluator(inp)
            print(evaluator.evaluate({
                "str": "Hello World!",
                "num": 1337,
                "float": 13.37,
                "nested": {
                    "str": "Hello again!"
                }
            }))
        except Exception as e:
            traceback.print_exc()
