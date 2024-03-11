from flask import Flask, render_template, request, jsonify
from analizador_lexico import lexer, ingreso
from ply.yacc import yacc

app = Flask(__name__)

tokens = [
    'FOR',
    'SYSTEM',
    'OUT',
    'PRINTLN',
    'ITERADOR',
    'IZQPARENT',
    'DERPARENT',
    'IZQCORCHET',
    'DERCORCHET',
    'LLAVEIZQ',
    'LLAVEDER',
    'INCREMENT',
    'INT',
    'PUNTOCOMA',
    'MENORQUE',
    'IGUAL',
    'PUNTO',
    'STRING',
    'COMA',
    'NUMERO',
    'ID',
]

precedence = (
    ('left', 'MENORQUE', 'IGUAL'), 
    ('left', 'INCREMENT'),
)

def p_program(p):
    '''
    program : statement
            | program statement
    '''

def p_statement(p):
    '''
    statement : assignment_statement
              | comparison_statement
              | for_loop_statement
              | print_statement
    '''

def p_assignment_statement(p):
    '''
    assignment_statement : ID IGUAL expression
                         | ID IGUAL INT
                         | ID IGUAL STRING
    '''
    
def p_comparison_statement(p):
    '''
    comparison_statement : expression MENORQUE expression
                         | expression IGUAL expression 
    '''

def p_for_loop_statement(p):
    '''
    for_loop_statement : FOR IZQPARENT assignment_statement PUNTOCOMA comparison_statement PUNTOCOMA assignment_statement DERPARENT LLAVEIZQ print_statement LLAVEDER
    '''

def p_print_statement(p):
    '''
    print_statement : SYSTEM PUNTO OUT PUNTO PRINTLN IZQPARENT expression DERPARENT PUNTOCOMA
    '''

def p_expression(p):
    '''
    expression : ID
               | INT
               | STRING
    '''

def p_string_expression(p):
    '''
    string_expression : STRING
                      | STRING PUNTO INT
                      | STRING PUNTO ID
    '''

def p_error(p):
    raise SyntaxError("Error sintáctico en la posición {}".format(p.lexpos))

parser = yacc()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analizar_lexico', methods=['POST'])  # Cambiado el nombre de la función
def analizar_cadena_lexico():
    cadena = request.json['cadena']
    try:
        tokens_lexicos = ingreso(cadena)
        return jsonify(resultado_lexico=tokens_lexicos)
    except Exception as e:
        return jsonify(error=str(e))

@app.route('/analizar_sintactico', methods=['POST'])
def analizar_cadena_sintactico():
    cadena = request.json['cadena']
    try:
        resultado_sintactico = parser.parse(cadena, lexer=lexer)
        if resultado_sintactico is None:
            mensaje = "La cadena fue aceptada correctamente."
        else:
            mensaje = "Cadena no aceptada"
        return jsonify(resultado_sintactico=mensaje)
    except SyntaxError as e:
        return jsonify(error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
