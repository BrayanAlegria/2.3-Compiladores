from ply.yacc import yacc
from flask import Flask, render_template, request, jsonify
from analizador_lexico import ingreso as analizar_lexico  
from analizador_sintactico import parser as analizador_sintactico      

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analizar', methods=['POST'])
def analizar_cadena_lexico():
    cadena = request.json['cadena']
    try:
        tokens_lexicos = analizar_lexico(cadena)  
        return jsonify(resultado_lexico=tokens_lexicos)
    except Exception as e:
        return jsonify(error=str(e))
    
@app.route('/analizar_sintactico', methods=['POST'])
def analizar_cadena_sintactico():
    cadena = request.json['cadena']
    try:
        resultado_sintactico = analizador_sintactico.parse(cadena) 
        if resultado_sintactico == "Cadena aceptada correctamente":
            mensaje = "La cadena fue aceptada correctamente."
        else:
            mensaje = "Error de sintaxis: " + str(resultado_sintactico)
        return jsonify(resultado_sintactico=mensaje)
    except Exception as e:
        return jsonify(error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
