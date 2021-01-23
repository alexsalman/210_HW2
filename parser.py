from lexer import *


class BinaryOperation:
    def __init__(self, left, operand, right):
        self.left = left
        self.operand = operand
        self.right = right


class Int:
    def __init__(self, token):
        self.value = token.value
        self.operand = token.type


class Var:
    def __init__(self, token):
        self.value = token.value
        self.operand = token.type


class Array:
    def __init__(self, token):
        self.value = token.value
        self.operand = token.type


class Boolean:
    def __init__(self, token):
        self.value = token.value
        self.operand = token.type


class BoolOperation:
    def __init__(self, left, operand, right):
        self.left = left
        self.operand = operand
        self.right = right


class Not:
    def __init__(self, node):
        self.operand = 'NOT'
        self.nt = node


class Skip:
    def __init__(self, token):
        self.value = token.value
        self.operand = token.type


class Assign:
    def __init__(self, left, operand, right):
        self.left = left
        self.operand = operand
        self.right = right


class Semi:
    def __init__(self, left, operand, right):
        self.left = left
        self.operand = operand
        self.right = right


class While:
    def __init__(self, condition, while_true, while_false):
        self.condition = condition
        self.while_true = while_true
        self.operand = 'WHILE'
        self.while_false = while_false


class If:
    def __init__(self, condition, if_true, if_false):
        self.condition = condition
        self.if_true = if_true
        self.operand = 'IF'
        self.if_false = if_false


class Parser:

    def __init__(self, lexer):
        self.lexer = lexer
        self.state = lexer.state
        self.current_token = self.lexer.get_next_token()

    def syntax_error(self):
        raise Exception('You have an error! ')

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

            if self.current_token.type == 'LEFT_PARENTHESIS':
                self.current_token = self.lexer.get_next_token()
                node = self.boolean_expression()

            elif self.current_token.type == 'BOOL':
                node = Boolean(self.current_token)

            else:
                self.syntax_error()
            node = Not(node)

        elif token.type == 'BOOL':
            node = Boolean(token)

        elif token.type == 'LEFT_PARENTHESIS':
            self.current_token = self.lexer.get_next_token()
            node = self.boolean_expression()

        elif token.type == 'RIGHT_PARENTHESIS':
            self.current_token = self.lexer.get_next_token()

        elif token.type == 'LEFT_BRACES':
            self.current_token = self.lexer.get_next_token()
            node = self.statement_expression()

        elif token.type == 'RIGHT_BRACES':
            self.current_token = self.lexer.get_next_token()

        elif token.type == 'SKIP':
            node = Skip(token)

        elif token.type == 'WHILE':
            self.current_token = self.lexer.get_next_token()
            condition = self.boolean_expression()
            while_false = Skip(Token('SKIP', 'skip'))

            if self.current_token.type == 'DO':
                self.current_token = self.lexer.get_next_token()

                if self.current_token == 'LEFT_BRACES':
                    while_true = self.statement_expression()

                else:
                    while_true = self.statement_term()

            return While(condition, while_true, while_false)

        elif token.type == 'IF':
            self.current_token = self.lexer.get_next_token()
            condition = self.boolean_expression()

            if self.current_token.type == "THEN":
                self.current_token = self.lexer.get_next_token()
                if_true = self.statement_expression()

            if self.current_token.type == "ELSE":
                self.current_token = self.lexer.get_next_token()
                if_false = self.statement_expression()

            return If(condition, if_true, if_false)

        else:
            self.syntax_error()
        self.current_token = self.lexer.get_next_token()
        return node

    def arith_term(self):
        node = self.factor()
        while self.current_token.type == 'MUL':
            type_name = self.current_token.type
            self.current_token = self.lexer.get_next_token()
            node = BinaryOperation(left=node, operand=type_name, right=self.factor())
        return node

    def arith_expression(self):
        node = self.arith_term()
        while self.current_token.type in ('PLUS', 'MINUS'):
            type_name = self.current_token.type
            self.current_token = self.lexer.get_next_token()
            node = BinaryOperation(left=node, operand=type_name, right=self.arith_term())
        return node

    def arith_parse(self):
        return self.arith_term()

    def boolean_term(self):
        node = self.arith_expression()
        if self.current_token.type in ('EQUALS', 'SMALLER'):
            type_name = self.current_token.type
            self.current_token = self.lexer.get_next_token()
            node = BinaryOperation(left=node, operand=type_name, right=self.arith_expression())
        return node

    def boolean_expression(self):
        node = self.boolean_term()
        while self.current_token.type in ('AND', 'OR'):
            type_name = self.current_token.type
            self.current_token = self.lexer.get_next_token()
            node = BinaryOperation(left=node, operand=type_name, right=self.boolean_term())
        return node

    def boolean_parse(self):
        return self.boolean_expression()

    def statement_term(self):
        node = self.boolean_expression()
        if self.current_token.type == 'ASSIGN':
            type_name = self.current_token.type
            self.current_token = self.lexer.get_next_token()
            node = Assign(left=node, operand=type_name, right=self.boolean_expression())
        return node

    def statement_expression(self):
        node = self.statement_term()
        while self.current_token.type == 'SEMI':
            type_name = self.current_token.type
            self.current_token = self.lexer.get_next_token()
            node = Semi(left=node, operand=type_name, right=self.statement_term())
        return node

    def statement_parse(self):
        return self.statement_expression()
