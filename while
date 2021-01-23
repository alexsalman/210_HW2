#!/usr/bin/python3
# Alex Salman 1/16/2021 aalsalma@ucsc.edu
# resource:
# (1) https://ruslanspivak.com/lsbasi-part7/
# (2) https://ruslanspivak.com/lsbasi-part8/
# (3) https://ruslanspivak.com/lsbasi-part9/
# (4) https://github.com/versey-sherry/while/blob/master/parsewhile.py

from parser import *
from interpreter import *


def main():
    line = [input()]
    text = ' '.join(line)
    lexer = Tokenizer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.visit()
    state_list = interpreter.immediate_state

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
