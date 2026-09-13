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
        area = self.pila.pop()
        self.pila.push(area)
        return area

    def registrar_solicitud(self, solicitud):
        area = self.obtener_area_tope()
        area.agregar_solicitud(solicitud)

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

            self.enviar_siguiente(area, solicitud)

        return procesadas

    def enviar_siguiente(self, area, solicitud):
        auxiliar = Stack()
        encontrado = False

        while not self.pila.is_empty():
            actual = self.pila.pop()

            if actual.nombre == area.nombre:
                encontrado = True
                auxiliar.push(actual)

                if not self.pila.is_empty():
                    siguiente = self.pila.pop()
                    siguiente.agregar_solicitud(solicitud)
                    auxiliar.push(siguiente)

                break

            auxiliar.push(actual)

        while not auxiliar.is_empty():
            self.pila.push(auxiliar.pop())

        if not encontrado:
            return

    def ejecutar_turno(self):
        self.turno = self.turno + 1

        self.preparar_turno()

        auxiliar = Stack()
        procesadas = 0

        while not self.pila.is_empty():
            area = self.pila.pop()

            cantidad_procesada = self.procesar_area(area)
            procesadas = procesadas + cantidad_procesada

            auxiliar.push(area)

        while not auxiliar.is_empty():
            self.pila.push(auxiliar.pop())

        self.mostrar_reporte(procesadas)

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
            destino = self.obtener_area_tope()

            if eliminada.es_recepcion():
                while not eliminada.cola_alta.is_empty():
                    destino.agregar_solicitud(eliminada.cola_alta.dequeue())

                while not eliminada.cola_normal.is_empty():
                    destino.agregar_solicitud(eliminada.cola_normal.dequeue())
            else:
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

        numero = self.pila.len()

        while not self.pila.is_empty():
            area = self.pila.pop()

            print(f"{numero}. Área: {area.nombre} (Capacidad: {area.capacidad}) | Sobrecargada: {'Sí' if area.sobrecargada else 'No'}")

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

            numero = numero - 1
            auxiliar.push(area)

        while not auxiliar.is_empty():
            self.pila.push(auxiliar.pop())

        print("===============================================")
        print()

    def mostrar_reporte(self, procesadas):
        print()
        print("=============== REPORTE DEL TURNO ===============")
        print("Turno:", self.turno)
        print("Solicitudes procesadas:", procesadas)
        print()

        auxiliar = Stack()

        while not self.pila.is_empty():
            area = self.pila.pop()

            print(area.nombre)
            print("  Pendientes:", area.cantidad_solicitudes())

            if area.sobrecargada:
                print("  ALERTA: Área en estado crítico / sobrecargada")

            auxiliar.push(area)

        while not auxiliar.is_empty():
            self.pila.push(auxiliar.pop())

        print("==================================================")
        print()
        
