class Node:

  __slots__ = ("__value","__next")

  def __init__(self, value):
    self.__value = value
    self.__next = None

  def __str__(self):
    return str(self.__value)

  @property
  def value(self):
    return self.__value

  @value.setter
  def value(self, new_value):
    if new_value is None:
      raise TypeError("El nodo no puede contener valores nulos")
    self.__value = new_value

  @property
  def next(self):
    return self.__next

  @next.setter
  def next(self, new_next):
    if new_next is not None and not isinstance(new_next,Node):
      raise TypeError("El next de un nodo, solo puede ser None ó un objeto tipo nodo")
    self.__next = new_next



class slinkedlist:

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
    if new_head is not None and not isinstance(new_head,Node):
      raise TypeError("La cabeza de una lista enlazada, solo puede ser None ó un objeto tipo nodo")
    self.__head = new_head

  @tail.setter
  def tail(self, new_tail):
    if new_tail is not None and not isinstance(new_tail,Node):
      raise TypeError("La cola de una lista enlazada, solo puede ser None ó un objeto tipo nodo")
    self.__tail = new_tail

  @size.setter
  def size(self, new_size):
    if new_size < 0 and not isinstance(new_size,int):
      raise TypeError("El tamaño de una lista enlazada, solo puede ser un numero entero mayor ó igual a cero")
    self.__size = new_size

  def __iter__(self):
    cur_node = self.__head

    while cur_node:
      yield cur_node
      cur_node = cur_node.next

  def __str__(self):
    result = [str(temp_node.value) for temp_node in self]
    return ' --> '.join(result)


  def prepend(self, new_value):
    new_node = Node(new_value)

    new_node.next = self.__head
    if self.__head is None:
      self.__tail = new_node
    self.__head = new_node

    self.__size += 1

  def append(self, new_value):
    new_node = Node(new_value)

    if self.__head is None:
      self.__head = new_node
    else:
      self.__tail.next = new_node

    self.__tail = new_node
    self.__size += 1

  def getbyIndex(self, index):

    if not isinstance(index,int) or index > self.__size -1 or index < -1:
      raise TypeError("el parametro indice esta por fuera de rango ó es un valor del tipo incorrecto")

    if index == 0:
      return self.head.value
    elif index == -1 or index == self.__size -1:
      return self.__tail.value
    else:
      index_temp = 0

      for cur_node in self:
        if index_temp == index:
          return cur_node.value
        index_temp += 1


  def getNodebyIndex(self, index):

      if not isinstance(index,int) or index > self.__size -1 or index < -1:
        raise TypeError("el parametro indice esta por fuera de rango ó es un valor del tipo incorrecto")

      if index == 0:
        return self.head
      elif index == -1 or index == self.__size -1:
        return self.__tail
      else:
        index_temp = 0

        for cur_node in self:
          if index_temp == index:
            return cur_node
          index_temp += 1


  def InsertbyIndex(self, index, new_value):

    if not isinstance(index,int) or index > self.__size or index < -1:
        raise TypeError("el parametro indice esta por fuera de rango ó es un valor del tipo incorrecto")


    if index == 0:
       self.prepend(new_value)
    elif index == -1 or index == self.__size:
       self.append(new_value)
    else:
        new_node = Node(new_value)
        prev_node = self.getNodebyIndex(index-1)
        print("prev_node", prev_node)
        print("new_node", new_node)

        new_node.next = prev_node.next
        prev_node.next = new_node
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

      for cur_node in self:
        if cur_node.next is self.__tail:
          prev_tail = cur_node

      prev_tail.next = None
      self.__tail = prev_tail
      self.__size -= 1

    return temp_value

