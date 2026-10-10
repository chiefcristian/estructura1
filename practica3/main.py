class ADN:
    def __init__(self,id,nombre,secuencia,riesgo):
        self.id = id
        self.nombre = nombre
        self.secuencia = secuencia
        self.riesgo = riesgo
    
    def __repr__(self):
        return(f"ID: {self.id}, Nombre: {self.nombre}, Secuencia: {self.secuencia}, Riesgo: {self.riesgo}")

class secuencias:
    def __init__(self):
        self.secuencias = []

    def registrar(self, ADN,id,i=0):
        if i == len(self.secuencias):
            self.secuencias.append(ADN)
            return "secuencia agregada correctamente"
        if self.secuencias[i].id == id:
            return "Secuencia ya existe"
        return self.registrar(ADN,id,i+1)
    

datos = secuencias()

a1 = ADN(1, "Muestra_A", "ATGCGTA", 7)
a2 = ADN(2, "Muestra_B", "ATATA", 4)
a3 = ADN(1, "Muestra_C", "GGCCTA", 9)

print(datos.registrar(a1, 1))
print(datos.registrar(a2, 2))
print(datos.registrar(a3, 1))
print(datos.secuencias)