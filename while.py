#!/usr/bin/python3
# Alex Salman 1/16/2021 aalsalma@ucsc.edu
# resource:
# (1) https://ruslanspivak.com/lsbasi-part7/
# (2) https://ruslanspivak.com/lsbasi-part8/
# (3) https://ruslanspivak.com/lsbasi-part9/
# (4) https://github.com/versey-sherry/while/blob/master/parsewhile.py
################################################################################
from parser import *
from lexer import *


class Interpreter:
    def __init__(self, parser):
        self.state = parser.state
        self.ast = parser.statement_parse()
        self.print_var = []
        self.print_state = []

    def visit(self):
        return evaluate_print(self.ast, self.state, self.print_var, self.print_state)


def main():
    array_input = []
    line = input()
    array_input.append(line)
    text = ' '.join(array_input)
    lexer = Tokenizer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.visit()
    state_list = interpreter.print_state

    if text == 'skip;':
        del state_list
    else:
        for i in range(len(state_list)):
            incomplete_output = []
            for key in sorted(state_list[i]):
                incomplete_output.append(' '.join([key, '→', str(state_list[i][key])]))
        output = ''.join(['{', ', '.join(incomplete_output), '}'])
    print(output)


if __name__ == '__main__':
    main()
