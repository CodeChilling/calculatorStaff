
# Mi API en Producción

Esta es una API construida con FastAPI y alojada en Render. Funciona con Python 3.11 o superior y utiliza la versión 0.111.0 de FastAPI.

## Requisitos

- Python 3.11+
- FastAPI 0.111.0

## Instalación de Dependencias

Sigue estos pasos para configurar el entorno de desarrollo local:

1. **Crear un entorno virtual**:
   - **Windows**: 
     ```bash
     python -m venv venv
     ```
   - **MacOS/Linux**: 
     ```bash
     python3 -m venv venv
     ```

2. **Activar el entorno virtual**:
   - **Windows**: 
     ```bash
     venv\Scripts\activate
     ```
   - **MacOS/Linux**: 
     ```bash
     source venv/bin/activate
     ```

3. **Instalar dependencias**:
   - Para instalar dependencias mínimas necesarias:
     ```bash
     pip install fastapi openpyxl pandas
     ```
   - Para instalar todas las dependencias:
     ```bash
     pip install -r requirements.txt
     ```

4. **Ejecutar el servidor**:
   ```bash
   uvicorn main:app --reload
   ```

## Uso

Para interactuar con la API, puedes acceder a través de las siguientes URLS:

- **Documentación de la API**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Interfaz alternativa de la API**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
