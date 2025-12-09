# ==========================================
#  MODELOS DEL DOMINIO
#  Clases que representan la lógica de negocio
# ==========================================


class Vehiculo:
    """Representa un vehículo en el sistema de cochera."""

    def __init__(self, tipo, placa, dueno, dni, telefono,
                 marca, modelo, casilla_tipo, casilla_numero,
                 mes_pagado, anio_pagado, tarifa_mensual):
        self.tipo = tipo              # "CARRO" o "MOTO"
        self.placa = placa
        self.dueno = dueno
        self.dni = dni
        self.telefono = telefono
        self.marca = marca
        self.modelo = modelo
        self.casilla_tipo = casilla_tipo   # "CARRO" o "MOTO"
        self.casilla_numero = casilla_numero  # índice (1..40) o (1..10)
        self.mes_pagado = mes_pagado
        self.anio_pagado = anio_pagado
        self.tarifa_mensual = tarifa_mensual

    def esta_al_dia(self, mes_actual, anio_actual):
        """Retorna True si el vehículo está al día con el pago."""
        if self.anio_pagado > anio_actual:
            return True
        if self.anio_pagado == anio_actual and self.mes_pagado >= mes_actual:
            return True
        return False

    def to_dict(self):
        """Convierte el vehículo a diccionario para respuesta JSON."""
        nombre_casilla = f"{self.casilla_tipo[0]}{self.casilla_numero}"  # C1, M1, etc.
        return {
            "tipo": self.tipo,
            "placa": self.placa,
            "dueno": self.dueno,
            "dni": self.dni,
            "telefono": self.telefono,
            "marca": self.marca,
            "modelo": self.modelo,
            "casilla_tipo": self.casilla_tipo,
            "casilla_numero": self.casilla_numero,
            "mes_pagado": self.mes_pagado,
            "anio_pagado": self.anio_pagado,
            "tarifa_mensual": self.tarifa_mensual,
            "nombre_casilla": nombre_casilla
        }


class Cochera:
    """Gestiona las casillas y vehículos de la cochera."""

    def __init__(self):
        # None = casilla libre / Vehiculo = casilla ocupada
        self.casillas_carros = [None] * 40   # C1..C40
        self.casillas_motos = [None] * 10    # M1..M10
        self.historial = []                  # lista de textos con eventos

        # Tarifas base (puedes cambiarlas a gusto)
        self.tarifa_carro = 250.0
        self.tarifa_moto = 150.0

    # -------------------------------
    #  FUNCIONES DE APOYO INTERNAS
    # -------------------------------
    def _buscar_casilla_libre(self, tipo):
        """Busca la primera casilla libre del tipo especificado."""
        if tipo == "CARRO":
            for i in range(len(self.casillas_carros)):
                if self.casillas_carros[i] is None:
                    return i  # índice 0..39
        elif tipo == "MOTO":
            for i in range(len(self.casillas_motos)):
                if self.casillas_motos[i] is None:
                    return i  # índice 0..9
        return None

    def _buscar_vehiculo_por_placa(self, placa):
        """Busca un vehículo por su placa. Retorna (tipo, indice, vehiculo) o (None, None, None)."""
        # Buscar primero en carros
        for i, veh in enumerate(self.casillas_carros):
            if veh is not None and veh.placa.upper() == placa.upper():
                return ("CARRO", i, veh)
        # Luego en motos
        for i, veh in enumerate(self.casillas_motos):
            if veh is not None and veh.placa.upper() == placa.upper():
                return ("MOTO", i, veh)
        return (None, None, None)

    # -------------------------------
    #  FUNCIONALIDADES PRINCIPALES
    # -------------------------------
    def registrar_vehiculo(self, tipo, placa, dueno, dni, telefono, marca, modelo, mes_pagado, anio_pagado):
        """Registra un vehículo y retorna el vehículo creado o None si no hay espacio."""
        # Validar tipo
        if tipo not in ["CARRO", "MOTO"]:
            return None

        # Verificar si ya existe la placa
        tipo_existente, _, _ = self._buscar_vehiculo_por_placa(placa)
        if tipo_existente is not None:
            return None  # Placa ya existe

        indice = self._buscar_casilla_libre(tipo)
        if indice is None:
            return None  # No hay casillas libres

        # Tarifa según tipo
        if tipo == "CARRO":
            tarifa = self.tarifa_carro
        else:
            tarifa = self.tarifa_moto

        casilla_tipo = tipo
        casilla_numero = indice + 1  # humano: 1..40 o 1..10

        veh = Vehiculo(
            tipo=tipo,
            placa=placa.upper(),
            dueno=dueno,
            dni=dni,
            telefono=telefono,
            marca=marca,
            modelo=modelo,
            casilla_tipo=casilla_tipo,
            casilla_numero=casilla_numero,
            mes_pagado=mes_pagado,
            anio_pagado=anio_pagado,
            tarifa_mensual=tarifa
        )

        if tipo == "CARRO":
            self.casillas_carros[indice] = veh
            nombre_casilla = f"C{casilla_numero}"
        else:
            self.casillas_motos[indice] = veh
            nombre_casilla = f"M{casilla_numero}"

        self.historial.append(
            f"Registro: {veh.tipo} {veh.placa} asignado a casilla {nombre_casilla}."
        )

        return veh

    def obtener_casillas(self):
        """Retorna el estado de todas las casillas."""
        casillas_carros = []
        casillas_motos = []

        for i, veh in enumerate(self.casillas_carros):
            nombre = f"C{i+1}"
            if veh is None:
                casillas_carros.append({
                    "nombre": nombre,
                    "estado": "LIBRE",
                    "placa": None,
                    "dueno": None
                })
            else:
                casillas_carros.append({
                    "nombre": nombre,
                    "estado": "OCUPADA",
                    "placa": veh.placa,
                    "dueno": veh.dueno
                })

        for i, veh in enumerate(self.casillas_motos):
            nombre = f"M{i+1}"
            if veh is None:
                casillas_motos.append({
                    "nombre": nombre,
                    "estado": "LIBRE",
                    "placa": None,
                    "dueno": None
                })
            else:
                casillas_motos.append({
                    "nombre": nombre,
                    "estado": "OCUPADA",
                    "placa": veh.placa,
                    "dueno": veh.dueno
                })

        return {"carros": casillas_carros, "motos": casillas_motos}

    def obtener_casillas_libres(self):
        """Retorna las casillas libres."""
        libres_carro = []
        libres_moto = []

        for i, veh in enumerate(self.casillas_carros):
            if veh is None:
                libres_carro.append(f"C{i+1}")

        for i, veh in enumerate(self.casillas_motos):
            if veh is None:
                libres_moto.append(f"M{i+1}")

        return {"carros": libres_carro, "motos": libres_moto}

    def buscar_por_placa(self, placa):
        """Busca un vehículo por placa y retorna el vehículo o None."""
        _, _, veh = self._buscar_vehiculo_por_placa(placa)
        return veh

    def registrar_pago(self, placa, mes, anio):
        """Registra un pago para un vehículo. Retorna True si se registró, False si no se encontró."""
        tipo, indice, veh = self._buscar_vehiculo_por_placa(placa)

        if veh is None:
            return False

        veh.mes_pagado = mes
        veh.anio_pagado = anio

        if tipo == "CARRO":
            nombre_casilla = f"C{indice+1}"
        else:
            nombre_casilla = f"M{indice+1}"

        self.historial.append(
            f"Pago: {veh.tipo} {veh.placa} pagó mes {mes}/{anio} - casilla {nombre_casilla}."
        )

        return True

    def obtener_deudores(self, mes_actual, anio_actual):
        """Retorna lista de deudores."""
        deudores_carros = []
        deudores_motos = []

        for i, veh in enumerate(self.casillas_carros):
            if veh is not None and not veh.esta_al_dia(mes_actual, anio_actual):
                deudores_carros.append({
                    "placa": veh.placa,
                    "dueno": veh.dueno,
                    "casilla": f"C{i+1}",
                    "tarifa": veh.tarifa_mensual,
                    "mes_pagado": veh.mes_pagado,
                    "anio_pagado": veh.anio_pagado
                })

        for i, veh in enumerate(self.casillas_motos):
            if veh is not None and not veh.esta_al_dia(mes_actual, anio_actual):
                deudores_motos.append({
                    "placa": veh.placa,
                    "dueno": veh.dueno,
                    "casilla": f"M{i+1}",
                    "tarifa": veh.tarifa_mensual,
                    "mes_pagado": veh.mes_pagado,
                    "anio_pagado": veh.anio_pagado
                })

        return {"carros": deudores_carros, "motos": deudores_motos}

    def eliminar_vehiculo(self, placa):
        """Elimina un vehículo del sistema. Retorna True si se eliminó, False si no se encontró."""
        tipo, indice, veh = self._buscar_vehiculo_por_placa(placa)

        if veh is None:
            return False

        if tipo == "CARRO":
            self.casillas_carros[indice] = None
            nombre_casilla = f"C{indice+1}"
        else:
            self.casillas_motos[indice] = None
            nombre_casilla = f"M{indice+1}"

        self.historial.append(
            f"Salida: {veh.tipo} {veh.placa} retirado, se libera casilla {nombre_casilla}."
        )

        return True

    def obtener_resumen(self):
        """Retorna un resumen de la cochera."""
        ocupados_carros = sum(1 for v in self.casillas_carros if v is not None)
        ocupados_motos = sum(1 for v in self.casillas_motos if v is not None)

        total_carros = len(self.casillas_carros)
        total_motos = len(self.casillas_motos)

        libres_carros = total_carros - ocupados_carros
        libres_motos = total_motos - ocupados_motos

        # Total recaudado aproximado (suma de tarifas de todos los registrados)
        total_recaudado = 0.0
        for v in self.casillas_carros:
            if v is not None:
                total_recaudado += v.tarifa_mensual
        for v in self.casillas_motos:
            if v is not None:
                total_recaudado += v.tarifa_mensual

        return {
            "carros": {
                "ocupadas": ocupados_carros,
                "libres": libres_carros,
                "total": total_carros
            },
            "motos": {
                "ocupadas": ocupados_motos,
                "libres": libres_motos,
                "total": total_motos
            },
            "recaudacion_mensual_teorica": total_recaudado
        }

    def obtener_historial(self):
        """Retorna el historial de movimientos."""
        return self.historial

    # -------------------------------
    #  MÉTODOS AUXILIARES PARA ORDENAMIENTO Y BÚSQUEDA
    # -------------------------------
    def _obtener_todos_los_vehiculos(self):
        """Obtiene una lista con todos los vehículos (carros y motos)."""
        vehiculos = []
        for veh in self.casillas_carros:
            if veh is not None:
                vehiculos.append(veh)
        for veh in self.casillas_motos:
            if veh is not None:
                vehiculos.append(veh)
        return vehiculos

    def _obtener_vehiculos_ordenados_por_placa(self):
        """Obtiene todos los vehículos ordenados por placa usando inserción directa."""
        vehiculos = self._obtener_todos_los_vehiculos()
        if len(vehiculos) == 0:
            return []
        # Crear copia para no modificar la original
        vehiculos_ordenados = vehiculos.copy()
        # Ordenamiento por inserción directa
        self._ordenar_por_insercion(vehiculos_ordenados, "placa")
        return vehiculos_ordenados

    # -------------------------------
    #  MÉTODOS DE ORDENAMIENTO
    # -------------------------------
    def _ordenar_por_insercion(self, lista, campo="placa"):
        """
        Ordenamiento por inserción directa.
        Ordena la lista in-place por el campo especificado (placa, dueno, etc.).
        """
        for i in range(1, len(lista)):
            clave = lista[i]
            valor_clave = getattr(clave, campo).upper() if hasattr(
                getattr(clave, campo), 'upper') else getattr(clave, campo)
            j = i - 1
            while j >= 0:
                valor_j = getattr(lista[j], campo).upper() if hasattr(
                    getattr(lista[j], campo), 'upper') else getattr(lista[j], campo)
                if valor_j > valor_clave:
                    lista[j + 1] = lista[j]
                    j -= 1
                else:
                    break
            lista[j + 1] = clave

    def _ordenar_por_seleccion(self, lista, campo="placa"):
        """
        Ordenamiento por selección directa.
        Ordena la lista in-place seleccionando el menor elemento en cada iteración.
        """
        n = len(lista)
        for i in range(n - 1):
            indice_menor = i
            valor_menor = getattr(lista[i], campo).upper() if hasattr(
                getattr(lista[i], campo), 'upper') else getattr(lista[i], campo)
            for j in range(i + 1, n):
                valor_j = getattr(lista[j], campo).upper() if hasattr(
                    getattr(lista[j], campo), 'upper') else getattr(lista[j], campo)
                if valor_j < valor_menor:
                    indice_menor = j
                    valor_menor = valor_j
            # Intercambiar
            if indice_menor != i:
                lista[i], lista[indice_menor] = lista[indice_menor], lista[i]

    def _ordenar_por_burbuja(self, lista, campo="placa"):
        """
        Ordenamiento por burbuja (intercambio directo).
        Ordena la lista in-place comparando e intercambiando elementos adyacentes.
        """
        n = len(lista)
        for i in range(n - 1):
            intercambio = False
            for j in range(n - 1 - i):
                valor_j = getattr(lista[j], campo).upper() if hasattr(
                    getattr(lista[j], campo), 'upper') else getattr(lista[j], campo)
                valor_j1 = getattr(lista[j + 1], campo).upper() if hasattr(
                    getattr(lista[j + 1], campo), 'upper') else getattr(lista[j + 1], campo)
                if valor_j > valor_j1:
                    lista[j], lista[j + 1] = lista[j + 1], lista[j]
                    intercambio = True
            # Optimización: si no hubo intercambios, la lista ya está ordenada
            if not intercambio:
                break

    def _quicksort(self, lista, campo="placa", inicio=0, fin=None):
        """
        Ordenamiento Quicksort (método logarítmico).
        Ordena la lista in-place usando el algoritmo de divide y vencerás.
        """
        if fin is None:
            fin = len(lista) - 1
        if inicio < fin:
            # Particionar y obtener el índice del pivote
            pivote_indice = self._particionar(lista, campo, inicio, fin)
            # Ordenar recursivamente las dos mitades
            self._quicksort(lista, campo, inicio, pivote_indice - 1)
            self._quicksort(lista, campo, pivote_indice + 1, fin)

    def _particionar(self, lista, campo, inicio, fin):
        """Función auxiliar para Quicksort: particiona la lista alrededor de un pivote."""
        pivote_valor = getattr(lista[fin], campo).upper() if hasattr(
            getattr(lista[fin], campo), 'upper') else getattr(lista[fin], campo)
        i = inicio - 1
        for j in range(inicio, fin):
            valor_j = getattr(lista[j], campo).upper() if hasattr(
                getattr(lista[j], campo), 'upper') else getattr(lista[j], campo)
            if valor_j <= pivote_valor:
                i += 1
                lista[i], lista[j] = lista[j], lista[i]
        lista[i + 1], lista[fin] = lista[fin], lista[i + 1]
        return i + 1

    def ordenar_vehiculos_por_placa(self, metodo="insercion"):
        """
        Ordena todos los vehículos por placa usando el método especificado.
        Métodos disponibles: 'insercion', 'seleccion', 'burbuja', 'quicksort'
        Retorna una lista ordenada de vehículos.
        """
        vehiculos = self._obtener_todos_los_vehiculos()
        if len(vehiculos) == 0:
            return []

        vehiculos_ordenados = vehiculos.copy()

        if metodo == "insercion":
            self._ordenar_por_insercion(vehiculos_ordenados, "placa")
        elif metodo == "seleccion":
            self._ordenar_por_seleccion(vehiculos_ordenados, "placa")
        elif metodo == "burbuja":
            self._ordenar_por_burbuja(vehiculos_ordenados, "placa")
        elif metodo == "quicksort":
            self._quicksort(vehiculos_ordenados, "placa")
        else:
            raise ValueError(
                f"Método de ordenamiento '{metodo}' no reconocido")

        return vehiculos_ordenados

    def ordenar_vehiculos_por_dueno(self, metodo="insercion"):
        """
        Ordena todos los vehículos por dueño usando el método especificado.
        Retorna una lista ordenada de vehículos.
        """
        vehiculos = self._obtener_todos_los_vehiculos()
        if len(vehiculos) == 0:
            return []

        vehiculos_ordenados = vehiculos.copy()

        if metodo == "insercion":
            self._ordenar_por_insercion(vehiculos_ordenados, "dueno")
        elif metodo == "seleccion":
            self._ordenar_por_seleccion(vehiculos_ordenados, "dueno")
        elif metodo == "burbuja":
            self._ordenar_por_burbuja(vehiculos_ordenados, "dueno")
        elif metodo == "quicksort":
            self._quicksort(vehiculos_ordenados, "dueno")
        else:
            raise ValueError(
                f"Método de ordenamiento '{metodo}' no reconocido")

        return vehiculos_ordenados

    # -------------------------------
    #  MÉTODOS DE BÚSQUEDA
    # -------------------------------
    def buscar_por_placa_secuencial_ordenada(self, placa):
        """
        Búsqueda secuencial en lista ordenada.
        Requiere que los datos estén ordenados por placa.
        Se detiene tempranamente si encuentra un elemento mayor.
        Retorna el vehículo encontrado o None.
        """
        vehiculos_ordenados = self._obtener_vehiculos_ordenados_por_placa()
        placa_upper = placa.upper()

        for veh in vehiculos_ordenados:
            if veh.placa.upper() == placa_upper:
                return veh
            elif veh.placa.upper() > placa_upper:
                # Parada temprana: si la placa actual es mayor, no seguirá encontrándose
                break
        return None

    def buscar_por_placa_binaria(self, placa):
        """
        Búsqueda binaria (requiere datos ordenados).
        Divide repetidamente el conjunto de datos a la mitad hasta encontrar el valor.
        Retorna el vehículo encontrado o None.
        """
        vehiculos_ordenados = self._obtener_vehiculos_ordenados_por_placa()
        if len(vehiculos_ordenados) == 0:
            return None

        placa_upper = placa.upper()
        izquierda = 0
        derecha = len(vehiculos_ordenados) - 1

        while izquierda <= derecha:
            medio = (izquierda + derecha) // 2
            placa_medio = vehiculos_ordenados[medio].placa.upper()

            if placa_medio == placa_upper:
                return vehiculos_ordenados[medio]
            elif placa_medio < placa_upper:
                izquierda = medio + 1
            else:
                derecha = medio - 1

        return None

    def buscar_por_placa_indexada(self, placa):
        """
        Búsqueda secuencial indexada (simulada).
        Crea un índice simple por primera letra de la placa para acelerar la búsqueda.
        Retorna el vehículo encontrado o None.
        """
        vehiculos = self._obtener_todos_los_vehiculos()
        placa_upper = placa.upper()

        # Crear índice simple por primera letra
        indice = {}
        for veh in vehiculos:
            primera_letra = veh.placa[0].upper() if veh.placa else ""
            if primera_letra not in indice:
                indice[primera_letra] = []
            indice[primera_letra].append(veh)

        # Buscar en el grupo correspondiente
        primera_letra_buscada = placa_upper[0] if placa_upper else ""
        if primera_letra_buscada in indice:
            for veh in indice[primera_letra_buscada]:
                if veh.placa.upper() == placa_upper:
                    return veh

        return None

    def obtener_vehiculos_ordenados(self, campo="placa", metodo="insercion"):
        """
        Obtiene todos los vehículos ordenados por el campo especificado.
        Campos disponibles: 'placa', 'dueno', 'marca', 'modelo', etc.
        Métodos: 'insercion', 'seleccion', 'burbuja', 'quicksort'
        Retorna lista de diccionarios con la información de los vehículos.
        """
        vehiculos = self._obtener_todos_los_vehiculos()
        if len(vehiculos) == 0:
            return []

        vehiculos_ordenados = vehiculos.copy()

        if metodo == "insercion":
            self._ordenar_por_insercion(vehiculos_ordenados, campo)
        elif metodo == "seleccion":
            self._ordenar_por_seleccion(vehiculos_ordenados, campo)
        elif metodo == "burbuja":
            self._ordenar_por_burbuja(vehiculos_ordenados, campo)
        elif metodo == "quicksort":
            self._quicksort(vehiculos_ordenados, campo)
        else:
            raise ValueError(
                f"Método de ordenamiento '{metodo}' no reconocido")

        return [veh.to_dict() for veh in vehiculos_ordenados]
