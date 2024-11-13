from flask import Flask,jsonify,request
from sudokuGame.Sudoku import Sudoku
import numpy as np

app = Flask(__name__)

sudoku = Sudoku()

@app.route("/")
def hello():
    return "¡SUDOKU-API!"

#@app.route("/api/sudoku/generar/<nivel>", methods=["GET"])
#def get_sudoku(nivel):
#    lista_niveles = ['0','1','2']
#    try:
#        if nivel:
#            if nivel in lista_niveles:
#
#                tablero = sudoku.iniciarSudoku()
#
#                tablero = sudoku.rellenarSudoku(tablero)
#                puzzle = sudoku.limpiarCeldas(tablero,nivel)
#                return jsonify({'solucion':tablero.tolist(),'puzzle':puzzle.tolist()}),200
#            else:
#                tablero = sudoku.iniciarSudoku()
#                tablero = sudoku.rellenarSudoku(tablero)
#                puzzle = sudoku.limpiarCeldasSudoku(tablero, '1')
#                return jsonify({'solucion':tablero.tolist(),'puzzle':puzzle.tolist()}),200
#        else:
#            return jsonify({'error':'Bad request'}),400
#    except Exception:
#        return jsonify({'error': 'Error en el servicio'}), 503

@app.route("/api/sudoku/generar", methods=["GET"])
@app.route("/api/sudoku/generar/", methods=["GET"])
def get_sudoku():
    lista_niveles = ['0','1','2']
    nivel = request.args.get('nivel')
    try:
        if nivel is None:
            return jsonify({'error':'Bad Request'}),404
        
        
        if nivel in lista_niveles:
            tablero = sudoku.iniciarSudoku()
            tablero = sudoku.generarSudoku(tablero)
            puzzle = sudoku.limpiarCeldas(tablero,nivel)
            return jsonify({'solucion':tablero.tolist(),'puzzle':puzzle.tolist()}),200
        else:
            tablero = sudoku.iniciarSudoku()
            tablero = sudoku.generarSudoku(tablero)
            puzzle = sudoku.limpiarCeldas(tablero, '1')
            return jsonify({'solucion':tablero.tolist(),'puzzle':puzzle.tolist()}),200
    except Exception:
        return jsonify({'error': 'Error en el servicio'}), 503

@app.route('/api/sudoku/solve', methods=['POST'])
def solve_sudoku():
    try:
        data = request.get_json()
        if data:
            arreglo = np.array(data['sudoku'], dtype=np.float64)
            if arreglo.shape != (9,9):
                return jsonify({'invalid':'Bad Request'}),400
                        
            tablero = sudoku.resolverSudoku(arreglo)
            if tablero is None:
                return jsonify({'solucion':'El tablero no tiene solucion'}),200
            return jsonify({'solucion':tablero.tolist()}),200
        else:
            return jsonify({'error':'datos de entrada incorrectos'}),400
    except Exception:
        return jsonify({'error':'Error en el servicio'}),503
    

@app.route('/api/sudoku/validate', methods=['POST'])
def validate_sudoku():
    try:
        data = request.get_json()
        if data:
            arreglo = np.array(data['sudoku'], dtype=np.float64)
            if arreglo.shape != (9,9):
                return jsonify({'invalid':'Bad Request'}),400

            if sudoku.validarSolucion(arreglo):
                return jsonify({'valid':True}),200
            else:
                return jsonify({'valid':False}),200
        else:
            return jsonify({'error':'datos de entrada incorrectos'}),400
    except Exception:
        return jsonify({'error':'Error en el servicio'}),503


if __name__ == "__main__":
    app.run(debug=True)