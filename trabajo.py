class NodeD:

  __slots__ = ("__value","__next","__prev")

  def __init__(self, value):
    self.__value = value
    self.__next = None
    self.__prev = None

  def __str__(self):
    return str(self.__value)

  @property
  def value(self):
    return self.__value

  @property
  def next(self):
    return self.__next

  @property
  def prev(self):
    return self.__prev

  @value.setter
  def value(self, new_value):
    if new_value is None:
      raise TypeError("El nodo no puede contener valores nulos")
    self.__value = new_value

  @next.setter
  def next(self, new_next):
    if new_next is not None and not isinstance(new_next, NodeD):
      raise TypeError("El next de un nodo, solo puede ser None ó un objeto tipo nodo")
    self.__next = new_next

  @prev.setter
  def prev(self, new_prev):
    if new_prev is not None and not isinstance(new_prev, NodeD):
      raise TypeError("El prev de un nodo, solo puede ser None ó un objeto tipo nodo")
    self.__prev = new_prev


class dlinkedlist:

  __slots__ = ("__head","__tail","__size")

  def __init__(self):
    self.__head = None
    self.__tail = None
    self.__size = 0

  @property
  def head(self):
    return self.__head

  @property
  def tail(self):
    return self.__tail

  @property
  def size(self):
    return self.__size

  @head.setter
  def head(self, new_head):
    if new_head is not None and not isinstance(new_head, NodeD):
      raise TypeError("La cabeza de una lista enlazada, solo puede ser None ó un objeto tipo nodo")
    self.__head = new_head

  @tail.setter
  def tail(self, new_tail):
    if new_tail is not None and not isinstance(new_tail, NodeD):
      raise TypeError("La cola de una lista enlazada, solo puede ser None ó un objeto tipo nodo")
    self.__tail = new_tail

  @size.setter
  def size(self, new_size):
    if not isinstance(new_size, int) or new_size < 0:
      raise TypeError("El tamaño de una lista enlazada, solo puede ser un numero entero mayor ó igual a cero")
    self.__size = new_size

  def __iter__(self):
    cur_node = self.__head

    while cur_node:
      yield cur_node
      cur_node = cur_node.next

  def __str__(self):
    if self.__head is None:
      return "Lista vacia"

    result = [str(temp_node.value) for temp_node in self]
    return " <--> ".join(result)

  def prepend(self, new_value):
    new_node = NodeD(new_value)

    new_node.next = self.__head

    if self.__head is None:
      self.__tail = new_node
    else:
      self.__head.prev = new_node

    self.__head = new_node
    self.__size += 1

  def append(self, new_value):
    new_node = NodeD(new_value)

    if self.__head is None:
      self.__head = new_node
    else:
      self.__tail.next = new_node

    new_node.prev = self.__tail
    self.__tail = new_node
    self.__size += 1

  def getbyIndex(self, index):

    if not isinstance(index, int) or index > self.__size - 1 or index < -1:
      raise TypeError("el parametro indice esta por fuera de rango ó es un valor del tipo incorrecto")

    if index == 0:
      return self.head.value

    elif index == -1 or index == self.__size - 1:
      return self.__tail.value

    else:
      index_temp = 0

      for cur_node in self:
        if index_temp == index:
          return cur_node.value
        index_temp += 1

  def getNodebyIndex(self, index):

    if not isinstance(index, int) or index > self.__size - 1 or index < -1:
      raise TypeError("el parametro indice esta por fuera de rango ó es un valor del tipo incorrecto")

    if index == 0:
      return self.head

    elif index == -1 or index == self.__size - 1:
      return self.__tail

    else:
      index_temp = 0

      for cur_node in self:
        if index_temp == index:
          return cur_node
        index_temp += 1

  def InsertbyIndex(self, index, new_value):

    if not isinstance(index, int) or index > self.__size or index < -1:
      raise TypeError("el parametro indice esta por fuera de rango ó es un valor del tipo incorrecto")

    if index == 0:
      self.prepend(new_value)

    elif index == -1 or index == self.__size:
      self.append(new_value)

    else:
      new_node = NodeD(new_value)
      prev_node = self.getNodebyIndex(index - 1)
      next_node = prev_node.next

      new_node.next = next_node
      prev_node.next = new_node
      new_node.prev = prev_node
      next_node.prev = new_node

      self.__size += 1

  def searchvalue(self, value_to_find):

    for cur_node in self:
      if value_to_find == cur_node.value:
        return True

    return False

  def set_newvalue(self, value, new_value):

    for cur_node in self:
      if value == cur_node.value:
        cur_node.value = new_value

    return False

  def popfirst(self):

    if self.__head is None:
      raise TypeError("No hay elementos para retornar")

    elif self.__head is self.__tail:
      temp_value = self.__head.value
      self.__head = None
      self.__tail = None
      self.__size = 0

    else:
      temp_value = self.__head.value
      self.__head = self.__head.next
      self.__head.prev = None
      self.__size -= 1

    return temp_value

  def pop(self):

    if self.__head is None:
      raise TypeError("No hay elementos para retornar")

    elif self.__head is self.__tail:
      temp_value = self.__head.value
      self.__head = None
      self.__tail = None
      self.__size = 0

    else:
      temp_value = self.__tail.value
      prev_tail = self.__tail.prev
      prev_tail.next = None
      self.__tail = prev_tail
      self.__size -= 1

    return temp_value

  def Prioridad_inmediata(self):

    actual = self.__head
    ultimo_prioritario = None

    while actual is not None:

      siguiente = actual.next

      if actual.value.categoria == "tercera_edad" and actual.value.nivel_triage == 1:

        if actual is self.__head:

          ultimo_prioritario = actual

        else:

          previo = actual.prev

          if previo is not None:
            previo.next = siguiente

          if siguiente is not None:
            siguiente.prev = previo
          else:
            self.__tail = previo

          if ultimo_prioritario is None:

            actual.prev = None
            actual.next = self.__head

            self.__head.prev = actual
            self.__head = actual

            ultimo_prioritario = actual

          else:

            siguiente_prioritario = ultimo_prioritario.next

            actual.prev = ultimo_prioritario
            actual.next = siguiente_prioritario

            ultimo_prioritario.next = actual

            if siguiente_prioritario is not None:
              siguiente_prioritario.prev = actual
            else:
              self.__tail = actual

            ultimo_prioritario = actual

      actual = siguiente

  def Depuracion_consulta_externa(self):

    actual = self.__head

    while actual is not None:

      siguiente = actual.next

      if actual.value.categoria == "adulto" and actual.value.nivel_triage > 3:

        previo = actual.prev

        if previo is None:
          self.__head = siguiente
        else:
          previo.next = siguiente

        if siguiente is None:
          self.__tail = previo
        else:
          siguiente.prev = previo

        actual.next = None
        actual.prev = None

        self.__size -= 1

      actual = siguiente

  def Aislamiento_zona_contagio(self, id_inicio, id_fin):

    lista_aislamiento = dlinkedlist()

    inicio = None
    fin = None
    actual = self.__head

    while actual is not None:

        if actual.value.id_paciente == id_inicio:
            inicio = actual

        if actual.value.id_paciente == id_fin:
            fin = actual

        actual = actual.next

    if inicio is None or fin is None:
        return lista_aislamiento

    if inicio is fin:
        return lista_aislamiento

    actual = inicio

    while actual is not fin and actual is not None:
        actual = actual.next

    if actual is None:
        inicio, fin = fin, inicio

    primero = inicio.next
    ultimo = fin.prev

    if primero is fin:
        return lista_aislamiento

    lista_aislamiento.head = primero
    lista_aislamiento.tail = ultimo

    cantidad = 0
    actual = primero

    while actual is not fin:

        cantidad += 1

        if actual is ultimo:
            break

        actual = actual.next

    lista_aislamiento.head = primero
    lista_aislamiento.tail = ultimo
    lista_aislamiento.size = cantidad

    inicio.next = fin
    fin.prev = inicio

    primero.prev = None
    ultimo.next = None

    self.__size -= cantidad

    return lista_aislamiento

  def Inversion_condicional(self):

    cantidad_pediatria = 0
    cantidad_adulto = 0

    actual = self.__head

    while actual is not None:

      if actual.value.categoria == "pediatria":
        cantidad_pediatria += 1

      elif actual.value.categoria == "adulto":
        cantidad_adulto += 1

      actual = actual.next

    if cantidad_pediatria > cantidad_adulto:

      actual = self.__head

      while actual is not None:

        siguiente = actual.next
        previo = actual.prev

        actual.next = previo
        actual.prev = siguiente

        actual = siguiente

      temporal = self.__head
      self.__head = self.__tail
      self.__tail = temporal

  def Reorganizacion_multicriterio(self):

    if self.__head is None or self.__head is self.__tail:
      return

    nodo_actual = self.__head.next

    while nodo_actual is not None:

      siguiente_nodo = nodo_actual.next

      previo = nodo_actual.prev
      siguiente = nodo_actual.next

      if previo is not None:
        previo.next = siguiente

      if siguiente is not None:
        siguiente.prev = previo

      if nodo_actual is self.__tail:
        self.__tail = previo

      nodo_actual.next = None
      nodo_actual.prev = None

      posicion = self.__head

      while posicion is not None:

        if posicion.value.categoria == "tercera_edad":
          prioridad_categoria_posicion = 1
        elif posicion.value.categoria == "pediatria":
          prioridad_categoria_posicion = 2
        else:
          prioridad_categoria_posicion = 3

        if nodo_actual.value.categoria == "tercera_edad":
          prioridad_categoria_actual = 1
        elif nodo_actual.value.categoria == "pediatria":
          prioridad_categoria_actual = 2
        else:
          prioridad_categoria_actual = 3

        if nodo_actual.value.nivel_triage < posicion.value.nivel_triage:
          break

        elif nodo_actual.value.nivel_triage == posicion.value.nivel_triage:

          if prioridad_categoria_actual < prioridad_categoria_posicion:
            break

        posicion = posicion.next

      if posicion is self.__head:

        nodo_actual.next = self.__head
        nodo_actual.prev = None

        self.__head.prev = nodo_actual
        self.__head = nodo_actual

      elif posicion is None:

        nodo_actual.prev = self.__tail
        nodo_actual.next = None

        self.__tail.next = nodo_actual
        self.__tail = nodo_actual

      else:

        previo = posicion.prev

        nodo_actual.prev = previo
        nodo_actual.next = posicion

        previo.next = nodo_actual
        posicion.prev = nodo_actual

      nodo_actual = siguiente_nodo

  def Intercalado_emergencia(self, lista_derivados):

    if lista_derivados.head is None:
      return

    if self.__head is None:

      self.__head = lista_derivados.head
      self.__tail = lista_derivados.tail
      self.__size = lista_derivados.size

      lista_derivados.head = None
      lista_derivados.tail = None
      lista_derivados.size = 0

      return

    actual_principal = self.__head
    actual_derivado = lista_derivados.head

    while actual_principal is not None and actual_derivado is not None:

      primero = actual_principal
      segundo = primero.next

      if segundo is None:
        break

      siguiente_principal = segundo.next
      siguiente_derivado = actual_derivado.next

      segundo.next = actual_derivado
      actual_derivado.prev = segundo

      actual_derivado.next = siguiente_principal

      if siguiente_principal is not None:
        siguiente_principal.prev = actual_derivado
      else:
        self.__tail = actual_derivado

      actual_principal = siguiente_principal
      actual_derivado = siguiente_derivado

    if actual_derivado is not None:

      actual_derivado.prev = self.__tail
      self.__tail.next = actual_derivado

      self.__tail = lista_derivados.tail

    self.__size += lista_derivados.size

    lista_derivados.head = None
    lista_derivados.tail = None
    lista_derivados.size = 0


class Paciente:

  def __init__(self, id_paciente, categoria, nivel_triage):
    self.id_paciente = id_paciente
    self.categoria = categoria
    self.nivel_triage = nivel_triage

  def __repr__(self):
        return f"({self.id_paciente},{self.categoria},{self.nivel_triage})"


lista_principal = dlinkedlist()

lista_principal.append(
  Paciente("P-101", "adulto", 3)
)

lista_principal.append(
  Paciente("P-102", "tercera_edad", 1)
)

lista_principal.append(
  Paciente("P-103", "adulto", 5)
)

lista_principal.append(
  Paciente("P-104", "pediatria", 2)
)

lista_principal.append(
  Paciente("P-105", "tercera_edad", 1)
)

lista_principal.append(
  Paciente("P-106", "pediatria", 2)
)

lista_principal.append(
  Paciente("P-107", "pediatria", 4)
)

lista_principal.append(
  Paciente("P-108", "adulto", 4)
)

print("PUNTO 1")
print(lista_principal)

lista_principal.Prioridad_inmediata()

print("\nPUNTO 2")
print(lista_principal)

lista_principal.Depuracion_consulta_externa()

print("\nPUNTO 3")
print(lista_principal)

lista_aislamiento = lista_principal.Aislamiento_zona_contagio(
  "P-102",
  "P-106"
)

print("\nPUNTO 4")
print("Lista principal:")
print(lista_principal)
print("Lista aislamiento:")
print(lista_aislamiento)

lista_principal.Inversion_condicional()

print("\nPUNTO 5")
print(lista_principal)

lista_principal.Reorganizacion_multicriterio()

print("\nPUNTO 6")
print(lista_principal)

lista_derivados = dlinkedlist()

lista_derivados.append(
  Paciente("D-201", "tercera_edad", 1)
)

lista_derivados.append(
  Paciente("D-202", "pediatria", 2)
)

lista_derivados.append(
  Paciente("D-203", "adulto", 3)
)

lista_derivados.append(
  Paciente("D-204", "pediatria", 1)
)

print("\nPUNTO 7")
print("Lista derivados:")
print(lista_derivados)

lista_principal.Intercalado_emergencia(lista_derivados)

print("Lista principal:")
print(lista_principal)

print("Lista derivados:")
print(lista_derivados)