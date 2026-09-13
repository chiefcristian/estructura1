
from linkedlist import slinkedlist

class Queue:

  def __init__(self):
    self.__q = slinkedlist()

  def __str__(self):
    result = [str(nodo.value) for nodo in self.__q]
    return '--'.join(result)

  def enqueue(self,e):
    self.__q.append(e)
    return True

  def dequeue(self):
    if not self.is_empty():
      return self.__q.popfirst()
    else:
      raise TypeError("La cola esta vacia, no hay elementos para desencolar")

  def first(self):
    if not self.is_empty():
      #return self.__q.getbyIndex(0)
      return self.__q.head.value
    else:
      raise TypeError("La cola esta vacia, no hay elementos para leer")

  def is_empty(self):
    return self.__q.size == 0

  def len(self):
    return self.__q.size


class Stack:

  def __init__(self):
    self.__s = slinkedlist()

  def __str__(self):
    result = [str(nodo.value) for nodo in self.__s ]
    return '||'.join(result)

  def push(self,e):
    self.__s.append(e)
    return True

  def pop(self):
    if not self.is_empty():
      return self.__s.pop()
    else:
      raise TypeError("La pila esta vacia, no hay elementos para desapilar")

  def top(self):
    if not self.is_empty():
      #return self.__q.getbyIndex(0)
      return self.__s.tail.value
    else:
      raise TypeError("La pila esta vacia, no hay elementos para leer")

  def is_empty(self):
    return self.__s.size == 0

  def len(self):
    return self.__s.size