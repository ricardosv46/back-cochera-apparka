# Sistema de Gestión de Cochera "Apparkala" - API REST

Sistema de gestión de cochera convertido a API REST usando FastAPI. Mantiene toda la lógica en memoria (sin base de datos) para demostrar conocimientos de estructuras de datos y algoritmos.

## Características

- 40 casillas para carros (C1-C40)
- 10 casillas para motos (M1-M10)
- Gestión completa de vehículos
- Sistema de pagos y control de deudores
- Historial de movimientos
- API REST lista para conectar con frontend

## Estructura del Proyecto

```
PROYECTO/
├── app/
│   ├── __init__.py      # Paquete de la aplicación
│   ├── main.py          # Endpoints de la API y configuración FastAPI
│   ├── models.py        # Clases del dominio (Vehiculo, Cochera)
│   └── schemas.py       # Modelos Pydantic (Request/Response)
├── main.py              # Punto de entrada (importa app desde app.main)
├── requirements.txt     # Dependencias
└── README.md            # Documentación
```

## Instalación

1. Crear un entorno virtual (recomendado):

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

2. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
uvicorn main:app --reload
```

El servidor estará disponible en: `http://localhost:8000`

## Documentación de la API

Una vez que el servidor esté corriendo, puedes acceder a:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Endpoints Disponibles

### 1. Registrar Vehículo

- **POST** `/vehiculos`
- Body: JSON con datos del vehículo (tipo, placa, dueño, DNI, teléfono, marca, modelo, mes_pagado, año_pagado)

### 2. Obtener Estado de Casillas

- **GET** `/casillas`
- Retorna el estado de todas las casillas (ocupadas/libres)

### 3. Obtener Casillas Libres

- **GET** `/casillas/libres`
- Retorna lista de casillas libres

### 4. Buscar Vehículo por Placa

- **GET** `/vehiculos/{placa}`
- Retorna información del vehículo

### 5. Registrar Pago

- **POST** `/pagos`
- Body: JSON con placa, mes y año del pago

### 6. Obtener Deudores

- **POST** `/deudores`
- Body: JSON con mes_actual y año_actual
- Retorna lista de vehículos con deuda

### 7. Eliminar Vehículo

- **DELETE** `/vehiculos/{placa}`
- Libera la casilla del vehículo

### 8. Obtener Resumen

- **GET** `/resumen`
- Retorna resumen estadístico de la cochera

### 9. Obtener Historial

- **GET** `/historial`
- Retorna historial de movimientos

## Notas

- Todos los datos se mantienen en memoria (se pierden al reiniciar el servidor)
- CORS está configurado para permitir conexiones desde cualquier origen (útil para desarrollo)
- La API retorna respuestas en formato JSON
