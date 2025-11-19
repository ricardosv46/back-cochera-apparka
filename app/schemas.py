# ==========================================
#  ESQUEMAS PYDANTIC
#  Modelos para validar requests y estructurar responses
# ==========================================

from pydantic import BaseModel
from typing import Optional, Dict


class VehiculoRequest(BaseModel):
    """Esquema para registrar un nuevo vehículo."""
    tipo: str  # "CARRO" o "MOTO"
    placa: str
    dueno: str
    dni: str
    telefono: str
    marca: str
    modelo: str
    mes_pagado: int = 0
    anio_pagado: int = 0


class VehiculoResponse(BaseModel):
    """Esquema de respuesta para información de vehículo."""
    tipo: str
    placa: str
    dueno: str
    dni: str
    telefono: str
    marca: str
    modelo: str
    casilla_tipo: str
    casilla_numero: int
    mes_pagado: int
    anio_pagado: int
    tarifa_mensual: float
    nombre_casilla: str


class PagoRequest(BaseModel):
    """Esquema para registrar un pago."""
    placa: str
    mes: int
    anio: int


class DeudoresRequest(BaseModel):
    """Esquema para consultar deudores."""
    mes_actual: int
    anio_actual: int


class CasillaEstado(BaseModel):
    """Esquema para el estado de una casilla."""
    nombre: str
    estado: str  # "LIBRE" o "OCUPADA"
    placa: Optional[str] = None
    dueno: Optional[str] = None


class ResumenResponse(BaseModel):
    """Esquema de respuesta para el resumen de la cochera."""
    carros: Dict[str, int]
    motos: Dict[str, int]
    recaudacion_mensual_teorica: float


class LoginRequest(BaseModel):
    """Esquema para login."""
    username: str
    password: str


class LoginResponse(BaseModel):
    """Esquema de respuesta para login."""
    message: str
    state: bool
    user: str