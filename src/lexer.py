import ply.lex as plex

class Lexer:
    reserved = {
        'import': 'IMPORT',
        'table': 'TABLE',
        'from': 'FROM',
        'export': 'EXPORT',
        'discard': 'DISCARD',
        'rename': 'RENAME',
        'print': 'PRINT',
        'select': 'SELECT',
        'create': 'CREATE',
        'where': 'WHERE',
        'and': 'AND',
        'limit': 'LIMIT',
        'join': 'JOIN',
        'using': 'USING',
        'call': 'CALL',
        'as': 'AS',
        'procedure': 'PROCEDURE',
        'end': 'END',
        'do': 'DO',
    }
    tokens  = [
        'ID',
        'STRING',
        'COMMA',
        'SEMICOLON',
        'NUMBER',
        'EQUALS',
        'NOT_EQUALS',
        'LPAREN',
        'RPAREN',
        'LESS_THAN',
        'LESS_EQUALS',
        'GREATER_THAN',
        'GREATER_EQUALS',
        'COMMENT',
        'COMMENTS',
        'ASTERISK',
        ] + list(reserved.values())
    
    t_COMMA = r'\,'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_SEMICOLON = r';'
    t_EQUALS = r'='
    t_NOT_EQUALS = r'<>'
    t_LESS_THAN = r'<'
    t_LESS_EQUALS = r'<='
    t_GREATER_THAN = r'>'
    t_GREATER_EQUALS = r'>='
    t_ASTERISK = r'\*'

    t_ignore = ' \t\n'

    def build(self, **kwargs):
        self.lexer = plex.lex(module=self, **kwargs)
        return self.lexer
    
    def input(self, data):
        self.lexer.input(data)

    def t_ID(self, t):
        r'[A-Za-z_][A-Za-z0-9_]*'
        t.type = self.reserved.get(t.value.lower(), "ID")
        return t
    
    def t_STRING(self, t):
        r'\"([^\\\"]|\\.)*\"'
        t.value = t.value[1:-1]
        return t

    def t_NUMBER(self, t):
        r'\d+(\.\d+)?'
        t.value = float(t.value)
        return t    
    
    def t_COMMENT(self, t):
        r'--.*'
        pass

    def t_COMMENTS(self, t):
        r"\{-[\s\S]*?-\}"
        pass

    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)
