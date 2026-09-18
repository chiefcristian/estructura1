from pilasycolas import Stack, Queue


class Solicitud:
    def __init__(self, id, descripcion, tipo):
        self.id = id
        self.descripcion = descripcion
        self.tipo = tipo

    def __str__(self):
        return f"{self.id} - {self.descripcion} - {self.tipo}"


class Area:
    def __init__(self, nombre, capacidad):
        self.nombre = nombre
        self.capacidad = capacidad
        self.cola = Queue()
        self.cola_alta = Queue()
        self.cola_normal = Queue()
        self.sobrecargada = False
        self.pendientes_turno = 0

    def es_recepcion(self):
        return self.nombre == "Recepción y Triaje"

    def agregar_solicitud(self, solicitud):
        if self.es_recepcion():
            if solicitud.tipo == "Alta":
                self.cola_alta.enqueue(solicitud)
            else:
                self.cola_normal.enqueue(solicitud)
        else:
            self.cola.enqueue(solicitud)

    def cantidad_solicitudes(self):
        if self.es_recepcion():
            return self.cola_alta.len() + self.cola_normal.len()
        return self.cola.len()

    def __str__(self):
        return self.nombre


class Sistema:
    def __init__(self):
        self.pila = Stack()
        self.turno = 0
        self.crear_areas()

    def crear_areas(self):
        self.pila.push(Area("Control de Calidad y Cierre", 1))
        self.pila.push(Area("Reparación / Corrección", 2))
        self.pila.push(Area("Diagnóstico Técnico", 2))
        self.pila.push(Area("Recepción y Triaje", 4))

    def obtener_area_tope(self):
        return self.pila.top()

    def registrar_solicitud(self, solicitud):
        if self.pila.is_empty():
            return False
        area = self.obtener_area_tope()
        area.agregar_solicitud(solicitud)
        return True

    def preparar_turno(self):
        auxiliar = Stack()

        while not self.pila.is_empty():
            area = self.pila.pop()

            cantidad = area.cantidad_solicitudes()
            area.pendientes_turno = cantidad

            if area.es_recepcion():
                area.sobrecargada = False
            else:
                if cantidad > 5:
                    area.sobrecargada = True
                else:
                    area.sobrecargada = False

            auxiliar.push(area)

        while not auxiliar.is_empty():
            self.pila.push(auxiliar.pop())

    def capacidad_efectiva(self, area):
        capacidad = area.capacidad

        if area.sobrecargada:
            capacidad = capacidad // 2

            if capacidad < 1:
                capacidad = 1

        return capacidad

    def procesar_area(self, area):
        procesadas = 0

        capacidad = self.capacidad_efectiva(area)
        limite = area.pendientes_turno

        while procesadas < capacidad and procesadas < limite:
            if area.es_recepcion():
                if not area.cola_alta.is_empty():
                    solicitud = area.cola_alta.dequeue()
                elif not area.cola_normal.is_empty():
                    solicitud = area.cola_normal.dequeue()
                else:
                    break
            else:
                if area.cola.is_empty():
                    break

                solicitud = area.cola.dequeue()

            procesadas = procesadas + 1

            self.enviar_siguiente(solicitud)

        return procesadas

    def enviar_siguiente(self, solicitud):
        if not self.pila.is_empty():
            siguiente = self.pila.top()
            siguiente.agregar_solicitud(solicitud)

    def ejecutar_turno(self):
        self.turno = self.turno + 1

        self.preparar_turno()

        print()
        print("=============== REPORTE DEL TURNO ===============")
        print("Turno:", self.turno)
        print()

        auxiliar = Stack()
        procesadas = 0
        finalizadas = 0

        while not self.pila.is_empty():
            area = self.pila.pop()

            es_base = self.pila.is_empty()

            cantidad_procesada = self.procesar_area(area)
            procesadas = procesadas + cantidad_procesada
            en_espera = area.pendientes_turno - cantidad_procesada

            print(area.nombre, f"(Capacidad efectiva: {self.capacidad_efectiva(area)})")
            print("  Procesadas:", cantidad_procesada)

            if es_base:
                finalizadas = finalizadas + cantidad_procesada
                print("  Finalizadas y fuera del sistema:", cantidad_procesada)
            else:
                print("  Transferidas a la siguiente etapa:", cantidad_procesada)

            print("  En espera:", en_espera)

            if area.sobrecargada:
                print("  ALERTA: área en estado crítico (más de 5 pendientes)")

            auxiliar.push(area)

        while not auxiliar.is_empty():
            self.pila.push(auxiliar.pop())

        print()
        print("Total procesadas en el turno:", procesadas)
        print("Total finalizadas:", finalizadas)
        print("=================================================")
        print()

    def hay_solicitudes(self):
        auxiliar = Stack()
        hay = False

        while not self.pila.is_empty():
            area = self.pila.pop()

            if area.cantidad_solicitudes() > 0:
                hay = True

            auxiliar.push(area)

        while not auxiliar.is_empty():
            self.pila.push(auxiliar.pop())

        return hay

    def ejecutar_automaticamente(self):
        while self.hay_solicitudes():
            self.ejecutar_turno()

    def eliminar_area(self, nombre):
        auxiliar = Stack()
        eliminada = None

        while not self.pila.is_empty():
            area = self.pila.pop()

            if eliminada is None and area.nombre == nombre:
                eliminada = area
            else:
                auxiliar.push(area)

        while not auxiliar.is_empty():
            self.pila.push(auxiliar.pop())

        if eliminada is None:
            return False

        if eliminada.cantidad_solicitudes() > 0:
            if self.pila.is_empty():
                print("No hay área destino, las solicitudes salen del sistema.")
                return True

            destino = self.obtener_area_tope()

            while not eliminada.cola_alta.is_empty():
                destino.agregar_solicitud(eliminada.cola_alta.dequeue())

            while not eliminada.cola_normal.is_empty():
                destino.agregar_solicitud(eliminada.cola_normal.dequeue())

            while not eliminada.cola.is_empty():
                destino.agregar_solicitud(eliminada.cola.dequeue())

        return True

    def agregar_area(self, nombre, capacidad):
        nueva = Area(nombre, capacidad)
        self.pila.push(nueva)

    
    def mostrar_estado(self):
        auxiliar = Stack()

        print()
        print("========== ESTADO ACTUAL DEL SISTEMA ==========")
        print()

        numero = 1

        while not self.pila.is_empty():
            area = self.pila.pop()

            if numero == 1:
                posicion = "<< TOPE"
            elif self.pila.is_empty():
                posicion = "<< BASE"
            else:
                posicion = ""

            print(f"{numero}. Área: {area.nombre} (Capacidad: {area.capacidad}) | Sobrecargada: {'Sí' if area.sobrecargada else 'No'} {posicion}")

            if area.es_recepcion():
                print("   Cola Alta Prioridad:")

                if area.cola_alta.is_empty():
                    print("   []")
                else:
                    print("   " + str(area.cola_alta))

                print("   Cola Normal:")

                if area.cola_normal.is_empty():
                    print("   []")
                else:
                    print("   " + str(area.cola_normal))
            else:
                print("   Cola de espera:")

                if area.cola.is_empty():
                    print("   []")
                else:
                    print("   " + str(area.cola))

            print()

            numero = numero + 1
            auxiliar.push(area)

        while not auxiliar.is_empty():
            self.pila.push(auxiliar.pop())

        print("===============================================")
        print()