#!/usr/bin/python3
# Alex Salman 1/16/2021 aalsalma@ucsc.edu
# resourses
# (1) https://ruslanspivak.com/lsbasi-part7/
# (2) https://ruslanspivak.com/lsbasi-part8/
# (3) https://ruslanspivak.com/lsbasi-part9/
################################################################################
# data structure
class AST_Structure(object):
    pass
# binary operators class
class Binary_Operation(AST_Structure):
# constructor
    def __init__(self, left, operation, right):
        self.left = left
        self.token = self.operation = operation
        self.right = right
# integer token class
class Number(AST_Structure):
    def __init__(self, token):
        self.token = token
        self.value = token.value
# to handle number with signs - or + with no space (negative and positive integers)
class UnaryOp(AST_Structure):
    def __init__(self, operation, expr):
        self.token = self.operation = operation
        self.expr = expr
################################################################################
# parser
class Parser(object):
# constructor
    def __init__(self, lexer):
        self.lexer = lexer
        self.current = self.lexer.get_next_token()
# error catcher
    def syntax_error(self):
        raise Exception('You have a syntax error . . ')
# comapre token type
    def str_compare(self, token_type):
        if self.current.type == token_type:
            self.current = self.lexer.get_next_token()
        else:
            self.syntax_error()
# check if value or expression
    def value_or_expression(self):
        token = self.current
        if token.type == pls:
            self.str_compare(pls)
            node = UnaryOp(token, self.value_or_expression())
            return node
        elif token.type == mns:
            self.str_compare(mns)
            node = UnaryOp(token, self.value_or_expression())
            return node
        elif token.type == INTEGER:
            self.str_compare(INTEGER)
            return Number(token)
        elif token.type == no:
            self.str_compare(no)
            node = UnaryOp(token, self.value_or_expression())
            return node
# div and mlt
    def mlt_div(self):
        node = self.value_or_expression()
        while self.current.type in (mlt, div):
            token = self.current
            if token.type == mlt:
                self.str_compare(mlt)
            elif token.type == div:
                self.str_compare(div)
            node = Binary_Operation(left=node, operation=token, right=self.value_or_expression())
        return node
# pls and mns
    def pls_mns(self):
        node = self.mlt_div()
        while self.current.type in (pls, mns):
            token = self.current
            if token.type == pls:
                self.str_compare(pls)
            elif token.type == mns:
                self.str_compare(mns)
            node = Binary_Operation(left=node, operation=token, right=self.mlt_div())
        return node
# parse pls_mns
    def parse_pls_mns(self):
        return self.pls_mns()
################################################################################
# interpreter for tree traversal, AST
class Node(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))
    def visit_UnaryOp(self, node):
        op = node.operation.type
        if op == pls:
            return +self.visit(node.expr)
        elif op == mns:
            return -self.visit(node.expr)
        elif op == no:
            return not self.visit(node.expr)

class Interpreter(Node):
# constructor
    def __init__(self, parsing_node):
        self.parsing_node = parsing_node
# check if children equels either of the arithmatic operations
    def visit_Binary_Operation(self, node):
        if node.operation.type == pls:
            return self.visit(node.left) + self.visit(node.right)
        elif node.operation.type == mns:
            return self.visit(node.left) - self.visit(node.right)
        elif node.operation.type == div:
            return self.visit(node.left) / self.visit(node.right)
        elif node.operation.type == mlt:
            return self.visit(node.left) * self.visit(node.right)

    def boolean(self, node):
        if node.operation.type == true:
            return self.visit(node.right)
        elif node.operation.type == false:
            return not self.visit(node.right)

    def skip(self, node):
        if node.operation.type == skip:
            return self.visit(node.right)

# get number value
    def visit_Number(self, node):
        return node.value

    def interpreter(self):
        ast_tree = self.parsing_node.parse_pls_mns()
        return self.visit(ast_tree)
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
        self.state = {}
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
#    def peek(self):
#        peek_pos = self.pos + 1
#        if peek_pos > len(self.user_input) - 1:
#            return None
#        else:
#            return self.user_input[peek_pos]
####
    def assignment(self):
        result = ''
        while self.current_char is not None and self.current_char in (':', '='):
            result = result + self.current_char
            self.advance()
        if result == ':=':
            return 'assign'
        else:
            return syntax_error(self)
    def a_space(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def int_list(self):
        result = ''
        self.advance()
        while self.current_char is not None and self.current_char != ']':
            result += self.current_char
            self.advance()
        self.advance()
        result = [int(i) for i in result.split(',')]
        return result

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
            if self.current_char == '=':
                self.advance()
                return Token(equals, '=')
            if self.current_char == '>':
                self.advance()
                return Token(greater, '>')
            if self.current_char == '<':
                self.advance()
                return Token(smaller, '<')
            if self.current_char == ';':
                self.advance()
                return Token(semi, ';')
            if self.current_char == '¬':
                self.advance()
                return Token(no, '¬')
            if self.current_char == '∧':
                self.advance()
                return Token(andd, '∧')
            if self.current_char == '∨':
                self.advance()
                return Token(orr, '∨')
            if self.current_char == '[':
                return Token(int_list, self.int_list())
            if self.current_char == ':':
                return Token(assign, self.assignment())
            if self.current_char.isalpha():
                result = ''
                while self.current_char is not None and (self.current_char.isalpha() or self.current_char.isdigit()):
                    result += self.current_char
                    self.advance()
                if result == "while":
                    return Token("WHILE", "while")
                elif result == "skip":
                    return Token("SKIP", "skip")
                elif result == "do":
                    return Token("DO", "do")
                elif result == "if":
                    return Token("IF", "if")
                elif result == "else":
                    return Token("ELSE", "else")
                elif result == "then":
                    return Token("THEN", "then")
                elif result == "true":
                    return Token("BOOL", True)
                elif result == "false":
                    return Token("BOOL", False)
                else:
                    return Token("VAR", result)
            self.error()
        return Token(EOF, None)

INTEGER, int_list, pls, mns, mlt, div, left_parenthesis, left_parenthesis, left_braces, right_braces, assign, equals, greater, smaller, skip, semi, no, AND, OR, WHILE, IF, THEN, ELSE, EOF = (
'INTEGER', 'int_list', 'PLUS', 'MINUS', 'MUL', 'DIV', '(', ')', '{', '}', '->', '=', '>', '<', 'skip', ';', '¬', '∧', '∨', 'while', 'if', 'then', 'else', 'EOF')
################################################################################
# main
def main():
    user_input = input ()
    token = Tokenizer(user_input)
    parsing_node = Parser(token)
    interpreter = Interpreter(parsing_node)
    to_print = interpreter.interpreter()
    print(to_print)

if __name__ == '__main__':
    main()
