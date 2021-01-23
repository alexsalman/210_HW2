import copy


class Interpreter:
    def __init__(self, parser):
        self.state = parser.state
        self.ast = parser.statement_parse()
        self.variables = []
        self.immediate_state = []

    def visit(self):
        return eval(self.ast, self.state, self.variables, self.immediate_state)


def dictionary(var, value):
    return dict([tuple([var, value])])


def eval(ast, state, variables, immediate_state):

    state = state
    node = ast
    variables = variables
    immediate_state = immediate_state

    if node.operand in ('INTEGER', 'ARRAY', 'BOOL'):
        return node.value

    elif node.operand == 'PLUS':
        return eval(node.left, state, variables, immediate_state) + eval(node.right, state, variables, immediate_state)

    elif node.operand == 'MINUS':
        return eval(node.left, state, variables, immediate_state) - eval(node.right, state, variables, immediate_state)

    elif node.operand == 'MUL':
        return eval(node.left, state, variables, immediate_state) * eval(node.right, state, variables, immediate_state)

    elif node.operand == 'NOT':
        return not eval(node.nt, state, variables, immediate_state)

    elif node.operand == 'EQUALS':
        return eval(node.left, state, variables, immediate_state) == eval(node.right, state, variables, immediate_state)

    elif node.operand == 'SMALLER':
        return eval(node.left, state, variables, immediate_state) < eval(node.right, state, variables, immediate_state)

    elif node.operand == 'AND':
        return eval(node.left, state, variables, immediate_state) and eval(node.right, state, variables, immediate_state)

    elif node.operand == 'OR':
        return eval(node.left, state, variables, immediate_state) or eval(node.right, state, variables, immediate_state)

    elif node.operand == 'VAR':
        if node.value in state:
            return state[node.value]
        else:
            return 0

    elif node.operand == 'SKIP':
        state = state
        temp_var = set(variables)
        temp_state = copy.deepcopy(state)
        temp_state = dict((var, temp_state[var]) for var in temp_var)
        immediate_state.append(temp_state)

    elif node.operand == 'SEMI':
        eval(node.left, state, variables, immediate_state)
        temp_var = set(variables)
        temp_state = copy.deepcopy(state)
        temp_state = dict((var, temp_state[var]) for var in temp_var)
        immediate_state.append(temp_state)
        eval(node.right, state, variables, immediate_state)

    elif node.operand == 'ASSIGN':
        var = node.left.value
        variables.append(var)

        if var in state:
            state[var] = eval(node.right, state, variables, immediate_state)

        else:
            state.update(dictionary(var, eval(node.right, state, variables, immediate_state)))
        temp_var = set(variables)
        temp_state = copy.deepcopy(state)
        temp_state = dict((var, temp_state[var]) for var in temp_var)
        immediate_state.append(temp_state)

    elif node.operand == 'WHILE':
        condition = node.condition
        while_true = node.while_true

        while eval(condition, state, variables, immediate_state):
            temp_var = set(variables)
            temp_state = copy.deepcopy(state)
            temp_state = dict((var, temp_state[var]) for var in temp_var)
            immediate_state.append(temp_state)
            eval(while_true, state, variables, immediate_state)
            temp_var = set(variables)
            temp_state = copy.deepcopy(state)
            temp_state = dict((var, temp_state[var]) for var in temp_var)
            immediate_state.append(temp_state)
        temp_var = set(variables)
        temp_state = copy.deepcopy(state)
        temp_state = dict((var, temp_state[var]) for var in temp_var)
        immediate_state.append(temp_state)

    elif node.operand == 'IF':
        condition = node.condition
        if_true = node.if_true
        if_false = node.if_false

        if eval(condition, state, variables, immediate_state):
            temp_var = set(variables)
            temp_state = copy.deepcopy(state)
            temp_state = dict((var, temp_state[var]) for var in temp_var)
            immediate_state.append(temp_state)
            eval(if_true, state, variables, immediate_state)

        else:
            temp_var = set(variables)
            temp_state = copy.deepcopy(state)
            temp_state = dict((var, temp_state[var]) for var in temp_var)
            immediate_state.append(temp_state)
            eval(if_false, state, variables, immediate_state)

    else:
        raise Exception("Something went wrong")


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
