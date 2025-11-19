# ==========================================
#  SISTEMA DE GESTIÓN DE COCHERA "APPARKALA"
#  40 casillas para carros, 10 para motos
#  API REST con FastAPI
# ==========================================

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import Cochera
from app.schemas import (
    VehiculoRequest, VehiculoResponse, PagoRequest,
    DeudoresRequest, ResumenResponse, LoginRequest, LoginResponse
)

# ==========================================
#  CONFIGURACIÓN DE FASTAPI
# ==========================================

app = FastAPI(title="Sistema de Gestión de Cochera Apparkala", version="1.0.0")

# Configurar CORS para permitir conexiones desde frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica el dominio de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
#  INSTANCIA GLOBAL DE COCHERA (EN MEMORIA)
# ==========================================

cochera = Cochera()

# ==========================================
#  ENDPOINTS DE LA API
# ==========================================


@app.get("/")
def root():
    """Endpoint raíz de la API."""
    return {"message": "Sistema de Gestión de Cochera Apparkala API", "version": "1.0.0"}


@app.post("/login", response_model=LoginResponse)
def login(credentials: LoginRequest):
    """Endpoint de autenticación. Usuario: admin, Contraseña: 12345678"""
    if credentials.username == "admin" and credentials.password == "12345678":
        return {
            "message": "Login exitoso",
            "state": True,
            "user": credentials.username
        }
    raise HTTPException(
        status_code=401,
        detail="Credenciales inválidas. Usuario: admin, Contraseña: 12345678"
    )


@app.post("/vehiculos", response_model=VehiculoResponse, status_code=201)
def registrar_vehiculo(vehiculo: VehiculoRequest):
    """Registra un nuevo vehículo en el sistema."""
    if vehiculo.tipo not in ["CARRO", "MOTO"]:
        raise HTTPException(
            status_code=400, detail="Tipo de vehículo inválido. Debe ser 'CARRO' o 'MOTO'")

    veh = cochera.registrar_vehiculo(
        tipo=vehiculo.tipo,
        placa=vehiculo.placa,
        dueno=vehiculo.dueno,
        dni=vehiculo.dni,
        telefono=vehiculo.telefono,
        marca=vehiculo.marca,
        modelo=vehiculo.modelo,
        mes_pagado=vehiculo.mes_pagado,
        anio_pagado=vehiculo.anio_pagado
    )

    if veh is None:
        # Verificar si es por placa duplicada o sin espacio
        tipo_existente, _, _ = cochera._buscar_vehiculo_por_placa(vehiculo.placa)  # noqa: SLF001
        if tipo_existente is not None:
            raise HTTPException(
                status_code=400, detail="Ya existe un vehículo con esa placa")
        raise HTTPException(
            status_code=400, detail=f"No hay casillas libres para {vehiculo.tipo.lower()}s")

    return veh.to_dict()


@app.get("/casillas")
def obtener_casillas():
    """Obtiene el estado de todas las casillas."""
    return cochera.obtener_casillas()


@app.get("/casillas/libres")
def obtener_casillas_libres():
    """Obtiene las casillas libres."""
    return cochera.obtener_casillas_libres()


@app.get("/vehiculos/{placa}", response_model=VehiculoResponse)
def buscar_vehiculo(placa: str):
    """Busca un vehículo por su placa."""
    veh = cochera.buscar_por_placa(placa)
    if veh is None:
        raise HTTPException(
            status_code=404, detail="No se encontró vehículo con esa placa")
    return veh.to_dict()


@app.post("/pagos")
def registrar_pago(pago: PagoRequest):
    """Registra un pago de mensualidad para un vehículo."""
    if not (1 <= pago.mes <= 12):
        raise HTTPException(
            status_code=400, detail="El mes debe estar entre 1 y 12")

    if pago.anio < 2000 or pago.anio > 2100:
        raise HTTPException(status_code=400, detail="Año inválido")

    exito = cochera.registrar_pago(pago.placa, pago.mes, pago.anio)
    if not exito:
        raise HTTPException(
            status_code=404, detail="No se encontró vehículo con esa placa")

    return {"message": f"Pago registrado correctamente para {pago.placa}", "state": True}


@app.post("/deudores")
def obtener_deudores(request: DeudoresRequest):
    """Obtiene la lista de deudores según el mes y año actual."""
    if not (1 <= request.mes_actual <= 12):
        raise HTTPException(
            status_code=400, detail="El mes debe estar entre 1 y 12")

    if request.anio_actual < 2000 or request.anio_actual > 2100:
        raise HTTPException(status_code=400, detail="Año inválido")

    deudores = cochera.obtener_deudores(
        request.mes_actual, request.anio_actual)
    return deudores


@app.delete("/vehiculos/{placa}")
def eliminar_vehiculo(placa: str):
    """Elimina un vehículo del sistema (libera la casilla)."""
    exito = cochera.eliminar_vehiculo(placa)
    if not exito:
        raise HTTPException(
            status_code=404, detail="No se encontró vehículo con esa placa")

    return {"message": f"Vehículo {placa} eliminado del sistema", "state": True}


@app.get("/resumen", response_model=ResumenResponse)
def obtener_resumen():
    """Obtiene un resumen de la cochera."""
    resumen = cochera.obtener_resumen()
    return resumen


@app.get("/historial")
def obtener_historial():
    """Obtiene el historial de movimientos."""
    return {"historial": cochera.obtener_historial()}
