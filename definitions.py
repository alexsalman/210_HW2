


class Defs(operands):
    op_dict = {
        'INTEGER': 'INTEGER',
        'ARRAY': 'ARRAY',
        'PLUS': 'PLUS',
        'MINUS': 'MINUS',
        'MUL': 'MUL',
        'DIV': 'DIV',
        'LEFT_PARENTHESIS': '(',
        'RIGHT_PARENTHESIS': ')',
        'LEFT_BRACES': '{',
        'RIGHT_BRACES': '}',
        'ASSIGN': ':=',
        'EQUALS': '=',
        'GREATER': '>',
        'SMALLER': '<',
        'SKIP': 'skip',
        'SEMI': ';',
        'NOT': '¬',
        'AND': '^',
        'OR': '∨',
        'DO': 'do',
        'WHILE': 'while',
        'IF': 'if',
        'THEN': 'then',
        'ELSE': 'else',
        'BOOL': 'BOOL',
        'EOF': 'EOF',
    }
    return op_dict.get(self, operands)
