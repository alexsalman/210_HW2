from definitions import Defs


# data structure
# binary operators class
class BinaryOperation():
    def __init__(self, left, operands, right):
        self.left = left
        self.token = self.operands = operands
        self.right = right


# integer token class
class Int():
    def __init__(self, token):
        self.value = token.value
        self.operands = token.type


# variable
class Var():
    def __init__(self, token):
        self.value = token.value
        self.operands = token.type


# array of integers
class Array():
    def __init__(self, token):
        self.value = token.value
        self.operands = token.type


# boolean
class Boolean():
    def __init__(self, token):
        self.value = token.value
        self.operands = token.type


# Not
class Not():
    def __init__(self, node):
        self.operands = 'NOT'
        self.nt = node


# Skip
class Skip():
    def __init__(self, token):
        self.value = token.value
        self.operands = token.type


# Assign
class Assign():
    def __init__(self, left, operands, right):
        self.left = left
        self.operands = operands
        self.right = right


# Compare
class Compare():
    def __init__(self, left, operands, right):
        self.left = left
        self.operands = operands
        self.right = right


# while
class While():
    def __init__(self, condition, while_true, while_false):
        self.condition = condition
        self.while_true = while_true
        self.operands = 'WHILE'
        self.while_false = while_false


# if
class If():
    def __init__(self, condition, if_true, if_false):
        self.condition = condition
        self.if_true = if_true
        self.operands = 'IF'
        self.if_false = if_false


# parser
class Parser():

    # constructor
    def __init__(self, lexer):
        self.lexer = lexer
        self.state = lexer.state
        self.current = self.lexer.get_next_token()

    # error catcher
    def syntax_error(self):
        raise Exception('You have a syntax error . . ')

    # compare token type
    def factor(self):
        token = self.current
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
                node = self.before_expression()
            elif self.current_token.type == 'BOOL':
                node = Boolean(self.current_token)
            else:
                self.syntax_error
            node = Not(node)
        elif token.type == 'BOOL':
            node = Boolean(token)
        elif token.type == 'LEFT_PARENTHESIS':
            self.current_token = self.lexer.get_next_token()
            node = self.before_expression()
        elif token.type == 'RIGHT_PARENTHESIS':
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
        elif token.type == 'IF':
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
            self.syntax_error
        self.current_token = self.lexer.get_next_token()
        return node

    def after_term(self):
        node = self.factor()
        while self.current_token.type == 'MUL':
            type_name = self.current_token.type
            self.current_token = self.lexer.get_next_token()
            node = BinaryOperation(left = node, operands= type_name, right = self.factor())
        return node

    def after_expression(self):
        node = self.after_term()
        while self.current_token.type in ('PLUS', 'MINUS'):
            type_name = self.current_token.type
            self.current_token = self.lexer.get_next_token()
            node = BinaryOperation(left = node, operands= type_name, right = self.after_term())
        return node

    def after_parse(self):
        return self.after_parse()

    def before_term(self):
        node = self.after_expression()
        if self.current_token.type in ('EQUALS', 'SMALLER'):
            type_name = self.current_token.type
            self.current_token = self.lexer.get_next_token()
            node = BinaryOperation(left = node, operands= type_name, right = self.after_expression())
        return node

    def before_expression(self):
        node = self.before_term()
        while self.current_token.type in ('AND', 'OR'):
            #print(self.current_token)
            type_name = self.current_token.type
            self.current_token = self.lexer.get_next_token()
            node = BinaryOperation(left = node, operands= type_name, right = self.before_term())
        return node

    def before_parse(self):
        return self.before_expression()

    def middle_term(self):
        node = self.before_expression()
        if self.current_token.type == 'ASSIGN':
            type_name = self.current_token.type
            self.current_token = self.lexer.get_next_token()
            node = Assign(left = node, operands = type_name, right = self.before_expression())
        return node

    def middle_expression(self):
        node = self.middle_term()
        while self.current_token.type == 'SEMI':
            type_name = self.current_token.type
            self.current_token = self.lexer.get_next_token()
            node = Compare(left=node, operands = type_name, right = self.middle_term())
        return node


    #this returns a node that represents combination of aexpr and bexpr
    def middle_parse(self):
        return self.middle_expression()
