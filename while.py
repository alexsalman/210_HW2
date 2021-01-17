#!/usr/bin/python3
# Alex Salman 1/16/2021 aalsalma@ucsc.edu
# resourses
# (1) https://ruslanspivak.com/lsbasi-part7/
# (2) https://ruslanspivak.com/lsbasi-part8/
################################################################################

################################################################################
# tokenizer
class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(type=self.type, value=repr(self.value))

    def __repr__(self):
        return self.__str__()

class Tokenizer(object):
# constructor
    def __init__(self, user_input):
        self.user_input = user_input
        self.pos = 0
        self.current_char = self.user_input[self.pos]

    def syntax_error(self):
        raise Exception('You have an invalid character . . ')
# advance the pointer
    def advance(self):
        self.pos += 1
        if self.pos > len(self.user_input) - 1:
            self.current_char = None
        else:
            self.current_char = self.user_input[self.pos]
# see what is after
    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]
####
    def a_space(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.a_space()
                continue
            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())
            if self.current_char == '+':
                self.advance()
                return Token(pls, '+')
            if self.current_char == '-':
                self.advance()
                return Token(mns, '-')
            if self.current_char == '*':
                self.advance()
                return Token(mlt, '*')
            if self.current_char == '/':
                self.advance()
                return Token(div, '/')
            if self.current_char == '(':
                self.advance()
                return Token(left_parenthesis, '(')
            if self.current_char == ')':
                self.advance()
                return Token(right_parenthesis, ')')
            if self.current_char == '{':
                self.advance()
                return Token(left_braces, '{')
            if self.current_char == '}':
                self.advance()
                return Token(right_braces, '}')
            if self.current_char == ':' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(assign, ':=')
            if self.current_char == '=':
                self.advance()
                return Token(equals, '=')
            if self.current_char == '>':
                self.advance()
                return Token(greater, '>')
            if self.current_char == '<':
                self.advance()
                return Token(smaller, '<')
            self.error()
        return Token(EOF, None)

INTEGER, pls, mns, mlt, div, left_parenthesis, left_parenthesis, left_braces, right_braces, assign, equals, EOF = (
'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', '(', ')', '{', '}', ':=', '=', '>', '<','EOF')
################################################################################
# main
def main():
    user_input = input ()
    token = Tokenizer(user_input)

if __name__ == '__main__':
    main()
