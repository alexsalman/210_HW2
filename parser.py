from lexer import *
import copy


def dictionary(var, value):
    return dict([tuple([var, value])])


def to_print(node):
    if node.operand in ('INTEGER', 'ARRAY', 'VAR', 'SKIP'):
        return node.value
    elif node.operand in 'BOOL':
        return str(node.value).lower()
    elif node.operand in ('PLUS', 'MINUS', 'MUL', 'EQUALS', 'SMALLER', 'AND', 'OR'):
        return ''.join(['(', str(to_print(node.left)), node.operand, str(to_print(node.right)), ')'])
    elif node.operand in 'NOT':
        return ''.join([node.operand, str(to_print(node.nt))])
    elif node.operand in 'ASSIGN':
        return ' '.join([str(to_print(node.left)), node.operand, str(to_print(node.right))])
    elif node.operand in 'SEMI':
        return ' '.join([''.join([str(to_print(node.left)), node.operand]), str(to_print(node.right))])
    elif node.operand in 'WHILE':
        return ' '.join(['while', str(to_print(node.condition)), 'do', '{', str(to_print(node.while_true)), '}'])
    elif node.operand in 'IF':
        return ' '.join(['if', str(to_print(node.condition)), 'then', '{', str(to_print(node.if_true)), '}', 'else', '{', str(to_print(node.if_false)), '}'])
    else:
        raise Exception('You have a syntax error . . ')


class StrFunction:
    def __init__(self, string):
        self.string = string

    def __add__(self, other):
        return self.string + other.string

    def __sub__(self, other):
        return self.string.replace(other.string, '', 1)


def evaluate_print(ast, state, print_var, print_state, print_step, init_step):
    state = state
    node = ast
    print_var = print_var
    print_state = print_state
    print_step = print_step
    init_step = init_step
    if node.operand in ('INTEGER', 'ARRAY', 'BOOL'):
        return node.value
    elif node.operand == 'VAR':
        if node.value in state:
            return state[node.value]
        else:
            state = state.update(dictionary(node.value, 0))
            return 0
    elif node.operand == 'SKIP':
        state = state
        temp_var = set(print_var)
        temp_state = copy.deepcopy(state)
        temp_state = dict((var, temp_state[var]) for var in temp_var)
        print_state.append(temp_state)
        temp_step = StrFunction(str(to_print(node)))
        print_step.append([StrFunction(StrFunction(init_step) - temp_step) - StrFunction("; ")])
        init_step = StrFunction(StrFunction(init_step) - temp_step) - StrFunction("; ")
    elif node.operand == 'SEMI':
        evaluate_print(node.left, state, print_var, print_state, print_step, init_step)
        temp_var = set(print_var)
        temp_state = copy.deepcopy(state)
        temp_state = dict((var, temp_state[var]) for var in temp_var)
        print_state.append(temp_state)
        temp_step = StrFunction(str(to_print(node.left)))
        print_step.append([str(StrFunction(StrFunction(init_step) - temp_step) - StrFunction("; "))])
        init_step = StrFunction(StrFunction(init_step) - temp_step) - StrFunction("; ")
        evaluate_print(node.right, state, print_var, print_state, print_step, init_step)
    elif node.operand == 'ASSIGN':
        var = node.left.value
        print_var.append(var)
        if var in state:
            state[var] = evaluate_print(node.right, state, print_var, print_state, print_step, init_step)
        else:
            state.update(dictionary(var, evaluate_print(node.right, state, print_var, print_state, print_step, init_step)))
        temp_var = set(print_var)
        temp_state = copy.deepcopy(state)
        temp_state = dict((var, temp_state[var]) for var in temp_var)
        print_state.append(temp_state)
        temp_step = StrFunction(str(to_print(node)))
        print_step.append(['skip; '+str(StrFunction(StrFunction(init_step) - temp_step) - StrFunction('; '))])
        init_step = StrFunction(StrFunction(init_step) - temp_step) - StrFunction('; ')

    elif node.operand == 'PLUS':
        return evaluate_print(node.left, state, print_var, print_state, print_step, init_step)+evaluate_print(node.right, state, print_var, print_state, print_step, init_step)

    elif node.operand == 'MINUS':
        return evaluate_print(node.left, state, print_var, print_state, print_step, init_step)-evaluate_print(node.right, state, print_var, print_state, print_step, init_step)

    elif node.operand == 'MUL':
        return evaluate_print(node.left, state, print_var, print_state, print_step, init_step)*evaluate_print(node.right, state, print_var, print_state, print_step, init_step)

    elif node.operand == 'NOT':
        return not evaluate_print(node.nt, state, print_var, print_state, print_step, init_step)

    elif node.operand == 'EQUALS':
        return evaluate_print(node.left, state, print_var, print_state, print_step, init_step) == evaluate_print(node.right, state, print_var, print_state, print_step, init_step)

    elif node.operand == 'SMALLER':
        return evaluate_print(node.left, state, print_var, print_state, print_step, init_step) < evaluate_print(node.right, state, print_var, print_state, print_step, init_step)

    elif node.operand == 'AND':
        return evaluate_print(node.left, state, print_var, print_state, print_step, init_step) and evaluate_print(node.right, state, print_var, print_state, print_step, init_step)

    elif node.operand == 'OR':
        return evaluate_print(node.left, state, print_var, print_state, print_step, init_step) or evaluate_print(node.right, state, print_var, print_state, print_step, init_step)

    elif node.operand == 'WHILE':
        condition = node.condition
        while_true = node.while_true
        while_false = node.while_false
        sentinel = 0
        while evaluate_print(condition, state, print_var, print_state, print_step, init_step):
            sentinel = sentinel+1
            if sentinel > 60000-1:
                break
            temp_var = set(print_var)
            temp_state = copy.deepcopy(state)
            temp_state = dict((var, temp_state[var]) for var in temp_var)
            print_state.append(temp_state)
            init_step = init_step.replace(to_print(node), str(to_print(node.while_true)+'; '+to_print(node)))
            print_step.append([init_step])
            evaluate_print(while_true, state, print_var, print_state, print_step, init_step)
            temp_var = set(print_var)
            temp_state = copy.deepcopy(state)
            temp_state = dict((var, temp_state[var]) for var in temp_var)
            print_state.append(temp_state)
            temp_step = StrFunction(str(to_print(node.while_true)))
            print_step.append([StrFunction(StrFunction(init_step) - temp_step) - StrFunction("; ")])
            init_step = StrFunction(StrFunction(init_step) - temp_step) - StrFunction("; ")
        temp_var = set(print_var)
        temp_state = copy.deepcopy(state)
        temp_state = dict((var, temp_state[var]) for var in temp_var)
        print_state.append(temp_state)
        temp_step = StrFunction(to_print(node))
        print_step.append(["skip; "+(StrFunction(StrFunction(init_step) - temp_step) - StrFunction("; "))])
        init_step = StrFunction(StrFunction(init_step) - temp_step) - StrFunction("; ")
    elif node.operand == 'IF':
        condition = node.condition
        if_true = node.if_true
        if_false = node.if_false
        if evaluate_print(condition, state, print_var, print_state, print_step, init_step):
            temp_var = set(print_var)
            temp_state = copy.deepcopy(state)
            temp_state = dict((var, temp_state[var]) for var in temp_var)
            print_state.append(temp_state)
            temp_step = StrFunction(str(to_print(node)))
            print_step.append([str(to_print(node.if_true)) + (StrFunction(init_step) - temp_step)])
            init_step = str(to_print(node.if_true)) + (StrFunction(init_step) - temp_step)
            evaluate_print(if_true, state, print_var, print_state, print_step, init_step)
        else:
            temp_var = set(print_var)
            temp_state = copy.deepcopy(state)
            temp_state = dict((var, temp_state[var]) for var in temp_var)
            print_state.append(temp_state)
            temp_step = StrFunction(str(to_print(node)))
            print_step.append([str(to_print(node.if_false)) + (StrFunction(init_step) - temp_step)])
            init_step = str(to_print(node.if_false)) + (StrFunction(init_step) - temp_step)
            evaluate_print(if_false, state, print_var, print_state, print_step, init_step)
    else:
        raise Exception("Something went wrong")


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
