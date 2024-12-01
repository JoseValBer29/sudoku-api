import numpy as np
import random as rdm

class Sudoku():

    def __init__(self):
        self.soluciones = 0



    def generarCuadro(self):
        """
        This function generates a 3x3 grid of unique numbers from 1 to 9 in random order.

        Parameters:
        None

        Returns:
        list: A 3x3 list representing the generated grid. Each row and column contains unique numbers.
        """
        fila = np.random.permutation(np.arange(1, 10))
        fila_list = fila.tolist()
        cuadro = [fila_list[0:3],fila_list[3:6],fila_list[6:9]]
        return cuadro


    def iniciarSudoku(self):
        """
        This function initializes a 9x9 Sudoku grid with a unique 3x3 grid in the top-left corner.
        The remaining cells are filled with zeros.

        Parameters:
        None

        Returns:
        numpy.ndarray: A 9x9 numpy array representing the initialized Sudoku grid.
        """
        sudoku = np.zeros((9,9))
        primero = np.array(self.generarCuadro())
        sudoku[0:3,0:3] = primero
        return sudoku


    def validarElemento(self,tablero, fila, columna, elemento):
        """
        Validates if a given element can be placed in a specific position in the Sudoku grid.

        Parameters:
        tablero (numpy.ndarray): The 9x9 Sudoku grid represented as a numpy array.
        fila (int): The row index where the element will be placed.
        columna (int): The column index where the element will be placed.
        elemento (int): The number to be validated.

        Returns:
        bool: True if the element can be placed in the specified position, False otherwise.
        """
        if elemento in tablero[fila, :]:
            return False
        if elemento in tablero[:, columna]:
            return False
        if elemento in tablero[3 * (fila // 3):3 * (fila // 3) + 3, 3 * (columna // 3):3 * (columna // 3) + 3]:
            return False
        return True


    def rellenar(self,tablero, numeros_validos,aleatorio=True):
        """
        Solves a Sudoku puzzle using backtracking algorithm.

        This function attempts to fill in the empty cells of a Sudoku grid recursively,
        trying different valid numbers until a solution is found or all possibilities
        are exhausted.

        Parameters:
        tablero (numpy.ndarray): A 9x9 numpy array representing the Sudoku grid.
                                 Empty cells are represented by 0.
        numeros_validos (list): A list of valid numbers that can be used to fill
                                the empty cells (typically 1-9).

        Returns:
        bool: True if a valid solution is found, False if no solution exists.

        Note:
        This function modifies the input 'tablero' in-place.
        """
        for fila in range(9):
            for columna in range(9):
                if tablero[fila, columna] == 0:
                    if aleatorio:
                        rdm.shuffle(numeros_validos)  
                    for elemento in numeros_validos:
                        if self.validarElemento(tablero, fila, columna, elemento):
                            tablero[fila, columna] = elemento
                            if self.rellenar(tablero,numeros_validos,aleatorio):
                                return True
                            tablero[fila, columna] = 0  
                    return False  
        return True  

    def generarSudoku(self,tablero):
        """
        Fills a complete Sudoku grid with valid numbers.

        This function initializes an empty Sudoku grid and attempts to fill it
        completely with valid numbers using a solving algorithm.

        Parameters:
        None

        Returns:
        numpy.ndarray or None: A 9x9 numpy array representing the completed Sudoku grid
                               if a valid solution is found, or None if no solution exists.
        """
        numeros_validos = list(range(1, 10))
        if self.rellenar(tablero,numeros_validos):
            return tablero
        else:
            return None
        
    def limpiarCeldas(self,tablero,nivel):
        """
        Clears cells in a 9x9 game board based on difficulty level.

        Parameters:
        - tablero (numpy.ndarray): A 9x9 numpy array representing the game board where 
          each cell contains a value (e.g., a Sudoku board).
        - nivel (str): The difficulty level of the game. Can be 'FACIL', 'MEDIO', or 'DIFICIL' 
          ('EASY', 'MEDIUM', 'HARD' in English).

        Returns:
        - numpy.ndarray: A copy of the input `tablero` with specific cells cleared (set to 0),
          where the number of cleared cells depends on the specified difficulty level.
        """

        celdas_nivel = {'0': 40, '1': 45, '2': 50}
        posiciones = list(range(81))
        rdm.shuffle(posiciones)
        rows, cols = np.unravel_index(posiciones, (9, 9))
        tablero_temp = tablero.copy()
        eliminadas = 0

        for row, col in zip(rows, cols):
            if eliminadas >= celdas_nivel[nivel]:
                break  # Limitar el número de eliminaciones según el nivel
            
            valor_actual = tablero_temp[row, col]
            tablero_temp[row, col] = 0
            soluciones = [0]  # Lista para hacer el contador mutable
            
            if self.validarUnicidad(tablero_temp, soluciones):  # Si hay una única solución
                eliminadas += 1
            else:
                tablero_temp[row, col] = valor_actual  # Restaurar si no es única
        

        return tablero_temp
    
    def validarUnicidad(self,tablero,soluciones):
        """
        Checks if the Sudoku board has a unique solution.

        This method uses a recursive approach to solve the Sudoku board. It attempts
        to place numbers from 1 to 9 in each empty cell (represented by a 0) and
        counts the number of possible solutions using the attribute `self.soluciones`.
        The function terminates if more than one solution is found, indicating that
        the Sudoku board does not have a unique solution.

        Parameters:
        ----------
        tablero : numpy.ndarray
            A 9x9 matrix representing the Sudoku board. Empty cells are represented
            by zeros (0).

        Returns:
        -------
        bool
            Returns `True` if a unique solution for the board has been found. Returns
            `False` if more than one solution is found, or if the board cannot be
            completely solved.
        """
        if soluciones[0] > 1:
            return False

        tablero_temp = tablero.copy()
        for fila in range(9):
            for columna in range(9):
                if tablero_temp[fila, columna] == 0:
                    for elemento in range(1, 10):
                        if self.validarElemento(tablero_temp, fila, columna, elemento):
                            tablero_temp[fila, columna] = elemento
                            if self.validarUnicidad(tablero_temp, soluciones):
                                tablero_temp[fila, columna] = 0
                                continue  # Si la llamada recursiva es exitosa, continuamos
                            
                            tablero_temp[fila, columna] = 0
                    return False  # Si no se encuentra ningún valor válido, retorna False

        soluciones[0] += 1
        return True  # Solución unica encontrada
    
    def validarSolucion(self, tablero):
        """
        Validates if a given Sudoku solution is correct.

        This function checks each cell in the provided Sudoku grid to ensure that
        the number placed in each cell is valid according to the Sudoku rules. The
        rules state that each number from 1 to 9 must appear exactly once in each
        row, column, and 3x3 subgrid.

        Parameters:
        tablero (numpy.ndarray): A 9x9 numpy array representing the Sudoku grid.
                                 Each cell contains a number from 1 to 9, or 0 if the cell is empty.

        Returns:
        bool: True if the provided Sudoku solution is valid, False otherwise.
        """
        tablero_temp = tablero.copy()
        for row in range(9):
            for col in range(9):
                elemento = tablero[row][col]
                tablero_temp[row][col] = 0
                if not self.validarElemento(tablero_temp, row, col, elemento):
                    return False
                tablero_temp[row, col] = elemento

        return True
    
    def resolverSudoku(self,tablero):
        if self.rellenar(tablero,list(range(1,10)),False):
            return tablero
        else:
            return None


