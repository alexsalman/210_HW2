#!/usr/bin/python3
# Alex Salman 1/16/2021 aalsalma@ucsc.edu
# resourses:
# (1) https://ruslanspivak.com/lsbasi-part7/
# (2) https://ruslanspivak.com/lsbasi-part8/
# (3) https://ruslanspivak.com/lsbasi-part9/
# (4) https://github.com/versey-sherry/while/blob/master/parsewhile.py
################################################################################
import sys
import copy
from lexer import *
from definitions import *
from parser import *



################################################################################
# interpreter for tree traversal, AST
class Interpreter():
    def __init__(self, parser):
        self.state = parser.state
        #load the AST by its root node and evaluate recurssively
        self.ast = parser.middle_parse()
        self.print_var = []
        self.print_state = []
        self.print_step = []
        self.init_step = to_print(self.ast)
        #print("The biscuit is here", self.current_node)

    def visit(self):
        return evaluate_print(self.ast, self.state, self.print_var, self.print_state, self.print_step, self.init_step)
################################################################################
# to print
def dictionary(var, value):
    return dict([tuple([var,value])])

#Helper function that prints recursively
def to_print(node):
    if node.operation in ('INTEGER', 'ARRAY', 'VAR', 'SKIP'):
        return node.value
    elif node.operation in ('BOOL'):
        return str(node.value).lower()
    elif node.operation in ('PLUS', 'MINUS', 'MUL', 'EQUALS', 'SMALLER', 'AND', 'OR'):
        return ''.join(['(',str(to_print(node.left)), node.operation, str(to_print(node.right)), ')'])
    elif node.operation in ('NOT'):
        return ''.join([node.operation,str(to_print(node.nt))])
    elif node.operation in ('ASSIGN'):
        return ' '.join([str(to_print(node.left)), node.operation, str(to_print(node.right))])
    elif node.operation in ('SEMI'):
        return ' '.join([''.join([str(to_print(node.left)), node.operation]), str(to_print(node.right))])
    elif node.operation in ('WHILE'):
        return ' '.join(['while', str(to_print(node.condition)), 'do', '{', str(to_print(node.while_true)), '}'])
    elif node.operation in ('IF'):
        return ' '.join(['if', str(to_print(node.condition)), 'then', '{', str(to_print(node.if_true)), '}', 'else', '{', str(to_print(node.if_false)) , '}'])
    else:
        raise Exception('You have a syntax error . . ')

class Str_Function():
    def __init__(self, string):
        self.string = string
    def __add__(self, other):
        return (self.string + other.string)
    def __sub__(self, other):
        return (self.string.replace(other.string, '', 1))


def evaluate_print(ast, state, print_var, print_state, print_step, init_step):
    state = state
    node = ast
    #This is to store all the variables that need printing, in case var without declaration
    print_var = print_var
    #This is to store all the states
    print_state = print_state
    print_step = print_step
    init_step = init_step
    #These are the fundamentals that won't add to any lists above
    if node.operation in ('INTEGER', 'ARRAY', 'BOOL'):
        return node.value
    elif node.operation == 'VAR':
        if node.value in state:
            return state[node.value]
        else:
            state = state.update(dictionary(node.value, 0))
            return 0
    elif node.operation == 'SKIP':
        state = state
        temp_var = set(print_var)
        temp_state = copy.deepcopy(state)
        temp_state = dict((var, temp_state[var]) for var in temp_var)
        print_state.append(temp_state)
        temp_step = Str_Function(str(to_print(node)))
        print_step.append([Str_Function(Str_Function(init_step) - temp_step) - Str_Function("; ")])
        init_step = Str_Function(Str_Function(init_step) - temp_step) - Str_Function("; ")
    elif node.operation == 'SEMI':
        evaluate_print(node.left, state, print_var, print_state, print_step, init_step)
        temp_var = set(print_var)
        temp_state = copy.deepcopy(state)
        temp_state = dict((var, temp_state[var]) for var in temp_var)
        print_state.append(temp_state)
        temp_step = Str_Function(str(to_print(node.left)))
        #this init is the init at the start of calling comp node
        print_step.append([str(Str_Function(Str_Function(init_step) - temp_step) - Str_Function("; "))])
        init_step = Str_Function(Str_Function(init_step) - temp_step) - Str_Function("; ")
        #print("Comp1", state)
        evaluate_print(node.right, state, print_var, print_state, print_step, init_step)
    elif node.operation == 'ASSIGN':
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
        temp_step = Str_Function(str(to_print(node)))
        print_step.append(["skip; "+ str(Str_Function(Str_Function(init_step) - temp_step) - Str_Function("; "))])
        init_step = Str_Function(Str_Function(init_step) - temp_step) - Str_Function("; ")

    elif node.operation == 'PLUS':
        return evaluate_print(node.left, state, print_var, print_state, print_step, init_step)+evaluate_print(node.right, state, print_var, print_state, print_step, init_step)

    elif node.operation == 'MINUS':
        return evaluate_print(node.left, state, print_var, print_state, print_step, init_step)-evaluate_print(node.right, state, print_var, print_state, print_step, init_step)

    elif node.operation == 'MUL':
        return evaluate_print(node.left, state, print_var, print_state, print_step, init_step)*evaluate_print(node.right, state, print_var, print_state, print_step, init_step)

    elif node.operation == 'NOT':
        return not evaluate_print(node.ap, state, print_var, print_state, print_step, init_step)

    elif node.operation =="EQUALS":
        return evaluate_print(node.left, state, print_var, print_state, print_step, init_step) == evaluate_print(node.right, state, print_var, print_state, print_step, init_step)

    elif node.operation =='SMALLER':
        return evaluate_print(node.left, state, print_var, print_state, print_step, init_step) < evaluate_print(node.right, state, print_var, print_state, print_step, init_step)

    elif node.operation =='AND':
        return (evaluate_print(node.left, state, print_var, print_state, print_step, init_step) and evaluate_print(node.right, state, print_var, print_state, print_step, init_step))

    elif node.operation =='OR':
        return (evaluate_print(node.left, state, print_var, print_state, print_step, init_step) or evaluate_print(node.right, state, print_var, print_state, print_step, init_step))

    elif node.operation == 'WHILE':
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
            #"node" is the whole while node
            temp_step = Str_Function(str(to_print(node.while_true)))
            print_step.append([Str_Function(Str_Function(init_step) - temp_step) - Str_Function("; ")])
            init_step = Str_Function(Str_Function(init_step) - temp_step) - Str_Function("; ")
        temp_var = set(print_var)
        temp_state = copy.deepcopy(state)
        temp_state = dict((var, temp_state[var]) for var in temp_var)
        print_state.append(temp_state)
        #"node" is the whole while node
        temp_step = Str_Function(to_print(node))
        #print_step.append([Str_Function(Str_Function(init_step) - temp_step) - Str_Function("; ") + "skip; "])
        print_step.append(["skip; "+ (Str_Function(Str_Function(init_step) - temp_step) - Str_Function("; "))])
        init_step = Str_Function(Str_Function(init_step) - temp_step) - Str_Function("; ")
    elif node.operation == 'IF':
        condition = node.condition
        if_true = node.if_true
        if_false = node.if_false
        if evaluate_print(condition, state, print_var, print_state, print_step, init_step):
            #only record the state before execution
            temp_var = set(print_var)
            temp_state = copy.deepcopy(state)
            temp_state = dict((var, temp_state[var]) for var in temp_var)
            print_state.append(temp_state)
            temp_step = Str_Function(str(to_print(node)))
            print_step.append([str(to_print(node.if_true)) + (Str_Function(init_step) - temp_step)])
            init_step = str(to_print(node.if_true)) + (Str_Function(init_step) - temp_step)
            evaluate_print(if_true, state, print_var, print_state, print_step, init_step)
        else:
            temp_var = set(print_var)
            temp_state = copy.deepcopy(state)
            temp_state = dict((var, temp_state[var]) for var in temp_var)
            print_state.append(temp_state)
            temp_step = Str_Function(str(to_print(node)))
            print_step.append([str(to_print(node.if_false)) + (Str_Function(init_step) - temp_step)])
            init_step = str(to_print(node.if_false)) + (Str_Function(init_step) - temp_step)
            evaluate_print(if_false, state, print_var, print_state, print_step, init_step)
    else:
        raise Exception("Nothing I can do bro")

################################################################################


INTEGER, ARRAY, PLUS, MINUS, MUL, DIV, LEFT_PARANTHESIS, RIGHT_PARANTHESIS, LEFT_BRACES, RIGHT_BRACES, ASSIGN, EQUALS, GREATER, SMALLER, SKIP, SEMI, NOT, AND, OR, DO, WHILE, IF, THEN, ELSE, BOOL,EOF = (
'INTEGER', 'ARRAY', 'PLUS', 'MINUS', 'MUL', 'DIV', '(', ')', '{', '}', '->', '=', '>', '<', 'skip', ';', '¬', '∧', '∨', 'do', 'while', 'if', 'then', 'else', 'BOOL','EOF')
################################################################################
# main
def main():
    contents = []
    line = input()
    line = line.strip()
    line = " ".join(line.split())
    contents.append(line)

    text = ' '.join(contents)
    text = ' '.join(text.split())
    #check if the first command is skip

    #print(text)
    lexer = Tokenizer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.visit()
    step_list = interpreter.print_step
    #flattened the nested list
    step_list = [item for sublist in step_list for item in sublist]
    state_list = interpreter.print_state
    if text[0:5] == "skip;" or text[0:6] == "skip ;":
        del step_list[0]
        del state_list[0]

#    step_list[-1] = 'skip'

#    if len(state_list) > 10000:
#        state_list = state_list[0:10000]
#        step_list = step_list[0:10000]

    #print(print_var)
#    if len(state_list) ==1 and state_list[0] == {} and text[0:4] == "skip":
#        print('')
#    else:
#        for i in range(len(state_list)):
#            output_string = []
#            for key in sorted(state_list[i]):
#                separator = " "
#                output_string.append(separator.join([key, "→", str(state_list[i][key])]))

#            state_string = ''.join(["{", ", ".join(output_string), "}"])
#            step_string = ' '.join(['→', step_list[i]])
#            print(step_string, state_string, sep = ', ')

#[key, ‘->’  value]
#‘’.join([key, ‘->’  value])
#print(‘’.join([key, ‘->’  value])
#store  = {‘a’: 5, ‘c’:5, ‘b’:3}
#Store = sorted(store)
#For key, value in store:
#print(‘’.join([key, ‘->’  value]))
#Store = {‘a’: 5, ‘c’:5, ‘b’:3}

if __name__ == '__main__':
    main()
