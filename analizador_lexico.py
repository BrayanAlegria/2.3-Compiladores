import ply.lex as lex
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

tokens = ['FOR', 'ITERADOR', 'SYSTEM', 'OUT', 'PRINTLN', 'IZQPARENT', 'DERPARENT', 'IZQCORCHET', 'DERCORCHET', 'LLAVEIZQ', 'LLAVEDER', 'INCREMENT', 'INT', 'IGUAL', 'PUNTOCOMA', 'MENORQUE', 'PUNTO', 'COMILLAS', 'DOSPUNTOS', 'NUMERO', 'ID']

palabras_reservadas = {
    'for': 'FOR',
    'i': 'ITERADOR',
    'System': 'SYSTEM',
    'out': 'OUT',
    'println': 'PRINTLN',
    '(': 'IZQPARENT',
    ')': 'DERPARENT',
    '{': 'IZQCORCHET',
    '}': 'DERCORCHET',
    '[': 'LLAVEIZQ',
    ']': 'LLAVEDER',
    '++': 'INCREMENT',
    '=': 'IGUAL',
    '<': 'MENORQUE',
    ';': 'PUNTOCOMA',
    '.': 'PUNTO',
    'Numero': 'NUMERO',
    '"': 'COMILLAS',
    ':': 'DOSPUNTOS',
}

def clasificar_token(token):
    if token.type == 'ID':
        return 'Identificador' if token.value in palabras_reservadas else 'No clasificado'
    elif token.type in ['INT', 'NUMERO']:
        return 'Tipo de dato'
    elif token.type in ['MENORQUE', 'PUNTO', 'INCREMENT']:
        return 'Operador'
    elif token.type in ['COMILLAS', 'DOSPUNTOS', 'IZQPARENT', 'DERPARENT', 'IGUAL', 'PUNTOCOMA', 'IZQCORCHET', 'DERCORCHET']:
        return 'Símbolo'
    elif token.type == 'FOR':
        return 'Reservada FOR'
    elif token.type in ['PRINTLN', 'SYSTEM', 'ITERADOR', 'OUT', 'NUMERO']:
        return 'Reservada'
    else:
        return 'No clasificado'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = palabras_reservadas.get(t.value, 'ID')
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t
    
def t_FOR(t):
    r'for'
    return t

#regex tokens
t_PUNTOCOMA = r'\;'
t_INCREMENT = r'\++'
#paréntesis
t_IZQPARENT = r'\('
t_DERPARENT = r'\)'
#corchete
t_IZQCORCHET = r'\{'
t_DERCORCHET = r'\}'
#llaves
t_LLAVEIZQ = r'\['
t_LLAVEDER = r'\]'
#símbolos
t_MENORQUE = r'\<'
t_PUNTO = r'\.'
t_IGUAL = r'\='
t_COMILLAS = r'\"'
t_DOSPUNTOS = r'\:'
t_ignore = ' \t'

def t_error(t):
    t.lexer.skip(1)

lexer = lex.lex()

def ingreso(datos):
    if not datos:
        return ['Cadena inválida: La cadena está vacía.']

    token = lex.lex()  
    token.input(datos)
    lexer = []
    es_valido = True

    for toke in token:
        categoria = clasificar_token(toke)
        estado = "->Valor: {:16} Categoría: {:16}".format(
            str(toke.value), categoria)
        lexer.append(estado)

    return lexer

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analizar', methods=['POST'])
def analizar_cadena():
    cadena = request.json['cadena']
    try:
        resultado_lexico = ingreso(cadena)
        return jsonify(resultado_lexico=[(tok.type, tok.value) for tok in resultado_lexico])
    except Exception as e:
        return jsonify(error=str(e))

if __name__ == '__main__':
    app.run(debug=True)

