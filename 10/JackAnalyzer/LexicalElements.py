keyword = [
    'class', 
    'constructor', 
    'function', 
    'method', 
    'field', 
    'static', 
    'var', 
    'int', 
    'char', 
    'boolean', 
    'void',
    'true',
    'false',
    'null',
    'this',
    'let',
    'do',
    'if',
    'else',
    'while',
    'return'
    ]

symbol = [
    '{',
    '}',
    '(',
    ')',
    '[',
    ']',
    '.',
    ',',
    ';',
    '+',
    '-',
    '*',
    '/',
    '&',
    '|',
    '<',
    '>',
    '=',
    '~'
]

tokens = [
    'keyword', 
    'symbol', 
    'integerConstant', 
    'stringConstant', 
    'identifier'
    ]

symbols_replace = {
    '<' : '&lt;',
    '>' : '&gt;',
    '"' : '&quot;',
    '&' : '&amp;'
}
