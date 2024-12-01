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
#        return jsonify({'error': 'Error en el servicio'}), 500

@app.route("/api/sudoku/generate", methods=["GET"])
@app.route("/api/sudoku/generate/", methods=["GET"])
def get_sudoku():
    lista_niveles = ['0','1','2']
    nivel = request.args.get('nivel')
    print(nivel)
    try:
        if nivel is None:
            nivel = '1'
        
        
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
        return jsonify({'error': 'Error en el servicio'}), 500

@app.route('/api/sudoku/solve', methods=['POST'])
def solve_sudoku():
    try:
        try:
            data = request.get_json()
        except Exception:
            return jsonify({'error': 'JSON no válido'}), 400
        if data:
            try:
                arreglo = np.array(data['sudoku'], dtype=np.float64)
            except Exception:
                return jsonify({'error': 'Tablero sudoku no válido',
                                'more details':'Una o más filas del sudoku contiene una cantidad de elementos diferente a 9'}), 404

            if arreglo.shape != (9,9):
                return jsonify({'error':'Tablero sudoku no válido',
                                'more details':'Las dimensiones del sudoku no coinciden con una matriz 9x9'}),400
                        
            tablero = sudoku.resolverSudoku(arreglo)
            if tablero is None:
                return jsonify({'solucion':'El tablero no tiene solucion'}),200
            return jsonify({'solucion':tablero.tolist()}),200
        else:
            return jsonify({'error':'JSON vacío'}),400
    except Exception:
        return jsonify({'error':'Error en el servicio'}),500
    

@app.route('/api/sudoku/validate', methods=['POST'])
def validate_sudoku():
    try:
        try:
            data = request.get_json()
        except Exception:
            return jsonify({'error': 'JSON no válido'}), 400
        if data:
            try:
                arreglo = np.array(data['sudoku'], dtype=np.float64)
            except Exception:
                return jsonify({'error': 'Tablero sudoku no válido',
                                'more details':'Una o más filas del sudoku contiene una cantidad de elementos diferente a 9'}), 404

            if arreglo.shape != (9,9):
                return jsonify({'error':'Tablero sudoku no válido',
                                'more details':'Las dimensiones del sudoku no coinciden con una matriz 9x9'}),400
                        

            if sudoku.validarSolucion(arreglo):
                return jsonify({'valid':"True"}),200
            else:
                return jsonify({'valid':"False"}),200
        else:
            return jsonify({'error':'JSON vacío'}),400
    except Exception:
        return jsonify({'error':'Error en el servicio'}),500


if __name__ == "__main__":
    app.run(debug=True)