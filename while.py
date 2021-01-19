#!/usr/bin/python3
# Alex Salman 1/16/2021 aalsalma@ucsc.edu
# resourses:
# (1) https://ruslanspivak.com/lsbasi-part7/
# (2) https://ruslanspivak.com/lsbasi-part8/
# (3) https://ruslanspivak.com/lsbasi-part9/
# (4) https://github.com/versey-sherry/while/blob/master/parsewhile.py
################################################################################
# data structure
class AST_Structure(object):
    pass
# binary operators class
class Binary_Operation(AST_Structure):
    def __init__(self, left, operation, right):
        self.left = left
        self.token = self.operation = operation
        self.right = right
# integer token class
class Int(AST_Structure):
    def __init__(self, token):
        self.token = token
        self.value = token.value
# variable
class Var(AST_Structure):
    def __init__(self, token):
        self.value = token.value
        self.operation = token.type
# array of integers
class Array(AST_Structure):
    def __init__(self, token):
        self.value = token.value
        self.operation = token.type
# boolean
class Boolean(AST_Structure):
    def __init__(self, token):
        self.value = token.value
        self.operation = token.type
# Not
class Not(AST_Structure):
    def __init__(self, node):
        self.operation = NOT
        self.ap = node
# Skip
class Skip(AST_Structure):
    def __init__(self, token):
        self.value = token.value
        self.operation = token.type
# Assign
class Assign(AST_Structure):
    def __init__(self, left, operation, right):
        self.left = left
        self.operation = operation
        self.right = right
# Compare
class Compare(AST_Structure):
    def __init__(self, left, operation, right):
        self.left = left
        self.operation = operation
        self.right = right
# while
class While(AST_Structure):
    def __init__(self, condition, while_true, while_false):
        self.condition = condition
        self.while_true = while_true
        self.operation = 'WHILE'
        self.while_false = while_false
# if
class If(AST_Structure):
    def __init__(self, condition, if_true, if_false):
        self.condition = condition
        self.if_true = if_true
        self.operation = 'IF'
        self.if_false = if_false
################################################################################
# parser
class Parser(object):
# constructor
    def __init__(self, lexer):
        self.lexer = lexer
        self.state = lexer.state
        self.current = self.lexer.get_next_token()
# error catcher
    def syntax_error(self):
        raise Exception('You have a syntax error . . ')
# comapre token type
    def factor(self):
        token = self.current_token
        if token.type == 'MINUS':
            self.current_token = self.lexer.get_next_token()
            token = self.current_token
            token.value = -token.value
            node = Int(token)
        elif token.type == 'INTEGER':
            node = Int(token)
        elif token.type == 'VAR':
            node = Var(token)
        elif token.type == 'ARRAY':
            node = Array(token)
        elif token.type == 'NOT':
            self.current_token = self.lexer.get_next_token()
            if self.current_token.type == 'LEFT_PARANTHESIS':
                self.current_token = self.lexer.get_next_token()
                node = self.before_expression()
            elif self.current_token.type == 'BOOL':
                node = Boolean(self.current_token)
            else:
                return syntax_error(self)
            node = Not(node)
        elif token.type == 'BOOL':
            node = Boolean(token)
        elif token.type == 'LEFT_PARANTHESIS':
            self.current_token = self.lexer.get_next_token()
            node = self.before_expression()
        elif token.type == 'RIGHT_PARANTHESIS':
            self.current_token = self.lexer.get_next_token()
        elif token.type == 'LEFT_BRACES':
            self.current_token = self.lexer.get_next_token()
            node = self.middle_expression()
        elif token.type == 'RIGHT_BRACES':
            self.current_token = self.lexer.get_next_token()
        elif token.type == 'SKIP':
            node = Skip(token)
        elif token.type == 'WHILE':
            self.current_token = self.lexer.get_next_token()
            condition = self.before_expression()
            while_false = Skip(Token('SKIP' ,'skip'))
            if self.current_token.type == 'DO':
                self.current_token = self.lexer.get_next_token()
                if self.current_token == 'LEFT_BRACES':
                    while_true = self.middle_expression()
                else:
                    while_true = self.middle_term()
            return While(condition, while_true, while_false)
        elif token.type == "IF":
            self.current_token = self.lexer.get_next_token()
            condition = self.before_expression()
            if self.current_token.type == "THEN":
                self.current_token = self.lexer.get_next_token()
                if_true = self.middle_expression()
            if self.current_token.type == "ELSE":
                self.current_token = self.lexer.get_next_token()
                if_false = self.middle_expression()
            return If(condition, if_true, if_false)
        else:
            return syntax_error(self)
        self.current_token = self.lexer.get_next_token()
        return node

    def after_term(self):
        node = self.factor()
        while self.current_token.type == 'MUL':
            type_name = self.current_token.type
            self.current_token = self.lexer.get_next_token()
            node = Binary_Operation(left = node, operation = type_name, right = self.factor())
        return node

    def after_expression(self):
        node = self.after_term()
        while self.current_token.type in ('PLUS', 'MINUS'):
            type_name = self.current_token.type
            self.current_token = self.lexer.get_next_token()
            node = Binary_Operation(left = node, operation = type_name, right = self.after_term())
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
    def visit_Int(self, node):
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

    def assignment(self):
        result = ''
        while self.current_char is not None and self.current_char in (':', '='):
            result = result + self.current_char
            self.advance()
        if result == ':=':
            return 'ASSIGN'
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

    def Array(self):
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
                return Token(PLUS, '+')
            if self.current_char == '-':
                self.advance()
                return Token(MU, '-')
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
                return Token(EQUALS, '=')
            if self.current_char == '>':
                self.advance()
                return Token(GREATER, '>')
            if self.current_char == '<':
                self.advance()
                return Token(SMALLER, '<')
            if self.current_char == ';':
                self.advance()
                return Token(SEMI, ';')
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
                return Token(ARRAY, self.Array())
            if self.current_char == ':':
                return Token(ASSIGN, self.assignment())
            if self.current_char.isalpha():
                result = ''
                while self.current_char is not None and (self.current_char.isalpha() or self.current_char.isdigit()):
                    result += self.current_char
                    self.advance()
                if result == 'while':
                    return Token('WHILE', 'while')
                elif result == 'skip':
                    return Token('SKIP', 'skip')
                elif result == 'do':
                    return Token('DO', 'do')
                elif result == 'if':
                    return Token('IF', 'if')
                elif result == 'else':
                    return Token('ELSE', 'else')
                elif result == 'then':
                    return Token('THEN', 'then')
                elif result == 'true':
                    return Token('BOOL', True)
                elif result == 'false':
                    return Token('BOOL', False)
                else:
                    return Token("VAR", result)
            self.error()
        return Token(EOF, None)

INTEGER, ARRAY, PLUS, MINUS, MUL, DIV, LEFT_PARANTHESIS, RIGHT_PARANTHESIS, LEFT_BRACES, RIGHT_BRACES, ASSIGN, EQUALS, GREATER, SMALLER, SKIP, SEMI, NOT, AND, OR, DO, WHILE, IF, THEN, ELSE, EOF = (
'INTEGER', 'ARRAY', 'PLUS', 'MINUS', 'MUL', 'DIV', '(', ')', '{', '}', '->', '=', '>', '<', 'skip', ';', '¬', '∧', '∨', 'do', 'while', 'if', 'then', 'else', 'EOF')
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
