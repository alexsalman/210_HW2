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
        self.print_step = []
        self.init_step = to_print(self.ast)

    def visit(self):
        return evaluate_print(self.ast, self.state, self.print_var, self.print_state, self.print_step, self.init_step)
################################################################################


def main():
    contents = []
    #a = 'i := 5 ; fact := 1 ; while 0 < i do { fact := fact * i ; i := i - 1 }'
    line = input()

    contents.append(line)

    text = ' '.join(contents)
    text = ' '.join(text.split())

    lexer = Tokenizer(text)

    parser = Parser(lexer)

    interpreter = Interpreter(parser)

    interpreter.visit()
    step_list = interpreter.print_step

    step_list = [item for sublist in step_list for item in sublist]
    state_list = interpreter.print_state
    if text[0:5] == 'skip;' or text[0:6] == 'skip ;':
        del step_list[0]
        del state_list[0]

    if len(state_list) > 10000:
        state_list = state_list[0:10000]
        step_list = step_list[0:10000]

    if len(state_list) == 1 and state_list[0] == {} and text[0:4] == 'skip':
        print('')
    else:
        for i in range(len(state_list)):
            output_string = []
            for key in sorted(state_list[i]):
                separator = ' '
                output_string.append(separator.join([key, '→', str(state_list[i][key])]))

            state_string = ''.join(['{', ', '.join(output_string), '}'])
        print(state_string)


if __name__ == '__main__':
    main()
