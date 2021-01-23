def definitions(operand):
    operand_dict = {
        'INTEGER': 'INTEGER',
        'ARRAY': 'ARRAY',
        'PLUS': 'PLUS',
        'MINUS': 'MINUS',
        'MUL': 'MUL',
        'DIV': 'DIV',
        'LEFT_PARENTHESIS': '(',
        'RIGHT_PARENTHESIS': ')',
        'LEFT_BRACES': '{',
        'OR': '∨',
        'DO': 'do',
        'WHILE': 'while',
        'IF': 'if',
        'THEN': 'then',
        'ELSE': 'else',
        'BOOL': 'BOOL',
        'EOF': 'EOF',
    }
    return operand_dict.get(operand)
