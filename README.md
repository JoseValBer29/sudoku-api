# API de Sudoku

## Descripción

Esta API proporciona funcionalidades relacionadas con el juego de Sudoku, incluyendo la generación de tableros, la resolución del puzzle y la validación de la respuesta enviada por el usuario.

## Endpoints

### 1. **Generar un tablero de Sudoku**

- **Método:** `GET`
- **Endpoint:** `/api/sudoku/generate`
- **Descripción:** Genera un tablero de Sudoku válido con números ya resueltos.
- **Parámetros:** 
  - `difficulty`: (opcional) Establece la dificultad del tablero. Valores posibles: `0`(fácil), `1`(medio), `2`(difícil). Si no se especifica, se genera un tablero de dificultad media.
  
- **Respuesta Exitosa:**
  - **Código:** 200 OK
  - **Cuerpo de la respuesta:**
    ```json
    {
      "puzzle": [
        [0, 3, 9, 5, 0, 0, 2, 8, 6],
        [0, 8, 0, 0, 9, 0, 7, 0, 0],
        [5, 0, 0, 1, 0, 6, 0, 3, 0],
        [9, 0, 1, 0, 2, 4, 3, 0, 8],
        [3, 0, 0, 0, 0, 8, 6, 0, 7],
        [8, 0, 0, 6, 0, 5, 0, 0, 1],
        [0, 0, 3, 8, 0, 9, 1, 0, 2],
        [0, 0, 8, 4, 7, 1, 0, 6, 3],
        [0, 1, 0, 2, 0, 3, 0, 0, 0]
      ]
      
    }
    ```

- **Respuesta de Error:**
  - **Código:** 500 Internal Server Error
  - **Cuerpo de la respuesta:**
    ```json
    {
      "error": "Error en el servicio"
    }
    ```

### 2. **Resolver un Sudoku**

- **Método:** `POST`
- **Endpoint:** `/api/sudoku/solve`
- **Descripción:** Resuelve un tablero de Sudoku proporcionado por el usuario.
- **Body:**
  - `board`: Una matriz 9x9 que representa el tablero de Sudoku que el usuario desea resolver.
  
- **Cuerpo de la solicitud:**
    ```json
    {
      "sudoku": [
        [0, 3, 9, 5, 0, 0, 2, 8, 6],
        [0, 8, 0, 0, 9, 0, 7, 0, 0],
        [5, 0, 0, 1, 0, 6, 0, 3, 0],
        [9, 0, 1, 0, 2, 4, 3, 0, 8],
        [3, 0, 0, 0, 0, 8, 6, 0, 7],
        [8, 0, 0, 6, 0, 5, 0, 0, 1],
        [0, 0, 3, 8, 0, 9, 1, 0, 2],
        [0, 0, 8, 4, 7, 1, 0, 6, 3],
        [0, 1, 0, 2, 0, 3, 0, 0, 0]
      ]
    }
    ```

- **Respuesta Exitosa:**
  - **Código:** 200 OK
  - **Cuerpo de la respuesta:**
    ```json
    {
      "Solución única" : true/false,
      "solucion": [
        [1, 3, 9, 5, 4, 7, 2, 8, 6],
        [4, 8, 6, 3, 9, 2, 7, 1, 5],
        [5, 2, 7, 1, 8, 6, 9, 3, 4],
        [9, 6, 1, 7, 2, 4, 3, 5, 8],
        [3, 4, 5, 9, 1, 8, 6, 2, 7],
        [8, 7, 2, 6, 3, 5, 4, 9, 1],
        [7, 5, 3, 8, 6, 9, 1, 4, 2],
        [2, 9, 8, 4, 7, 1, 5, 6, 3],
        [6, 1, 4, 2, 5, 3, 8, 7, 9]
      ]
    }
    ```

- **Respuestas de Error:**
  - **Código:** 400 Bad Request
  - **Cuerpo de la respuesta:**
    ```json
    {
      "error": "JSON no válido"
    }
    ```
    O
    ```json
    {
      "error":"Tablero sudoku no válido",
      "more details":"Una o más filas del sudoku contiene una cantidad de elementos diferente a 9"
    }
    ```
    O
    ```json
    {
      "error":"Tablero sudoku no válido",
      "more details":"Las dimensiones del sudoku no coinciden con una matriz 9x9"
    }
    ```
    O
    ```json
    {
      "error": "JSON vacío"
    }
    ```
  - **Código:** 500 Internal Server Error
  - **Cuerpo de la respuesta:**
  ```json
    {
      "error": "Error en el servicio"
    }
    ```

### 3. **Validar una solución de Sudoku**

- **Método:** `POST`
- **Endpoint:** `/api/sudoku/validate`
- **Descripción:** Valida una solución de Sudoku proporcionada por el usuario.
- **Parámetros:**
  - `board`: Una matriz 9x9 que representa el tablero de Sudoku que el usuario desea validar.
  
- **Cuerpo de la solicitud:**
    ```json
    {
      "board": [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9]
      ]
    }
    ```

- **Respuesta:**
  - Si el sudoku está resuelto correctamente
  - **Código:** 200 OK
  - **Cuerpo de la respuesta:**
    ```json
    {
      "valid": "True"
    }
    ```
  - Si el sudoku está mal resuelto
  - **Código:** 200 OK
  - **Cuerpo de la respuesta:**
    ```json
    {
      "valid": "False"
    }
    ```

- **Respuestas de Error:**
  - **Código:** 400 Bad Request
  - **Cuerpo de la respuesta:**
    ```json
    {
      "error": "JSON no válido"
    }
    ```
    O
    ```json
    {
      "error":"Tablero sudoku no válido",
      "more details":"Una o más filas del sudoku contiene una cantidad de elementos diferente a 9"
    }
    ```
    O
    ```json
    {
      "error":"Tablero sudoku no válido",
      "more details":"Las dimensiones del sudoku no coinciden con una matriz 9x9"
    }
    ```
    O
    ```json
    {
      "error": "JSON vacío"
    }
    ```
  - **Código:** 500 Internal Server Error
  - **Cuerpo de la respuesta:**
  ```json
    {
      "error": "Error en el servicio"
    }
    ```

## Requisitos

- Python 3.12
- Flask (para la API)
- Numpy (para manipular los tableros de Sudoku)
- dependencias detalladas en requirements.txt

## Instalación
Clona este repositorio en tu máquina local:
   ```bash
   git clone hxttps://github.com/usuario/sudoku-api.git
   cd sudoku-api
   ```

Instala las dependencias
   ```bash
   git clone https://github.com/usuario/sudoku-api.git
   cd sudoku-api
   ```

Ejecuta la API
   ```bash
   python app.py
   ```

## Contribuciones
Si deseas contribuir a este proyecto, por favor realiza un fork y abre un pull request con tus cambios. Asegúrate de que tus cambios estén bien probados antes de enviarlos.




  