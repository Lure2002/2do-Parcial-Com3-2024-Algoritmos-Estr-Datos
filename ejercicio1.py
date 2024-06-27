from datetime import date, timedelta
import random
import os

#Ejercicio 1

class Fecha:
    def __init__(self, dia:int=None, mes:int=None, anio:int=None):
        if dia is None or mes is None or anio is None:
            hoy = date.today()
            self.dia = hoy.day
            self.mes = hoy.month
            self.anio = hoy.year
        else:
            self.dia = dia
            self.mes = mes
            self.anio = anio

    def __str__(self):
        return f"{self.dia:02d}/{self.mes:02d}/{self.anio}"

    def __add__(self, dias):
        nueva_fecha = date(self.anio, self.mes, self.dia) + timedelta(days=dias)
        return Fecha(nueva_fecha.day, nueva_fecha.month, nueva_fecha.year)

    def __eq__(self, otra_fecha):
        return (self.dia == otra_fecha.dia and self.mes == otra_fecha.mes and self.anio == otra_fecha.anio)

    def calcular_dif_fecha(self, otra_fecha):
        fecha1 = date(self.anio, self.mes, self.dia)
        fecha2 = date(otra_fecha.anio, otra_fecha.mes, otra_fecha.dia)
        return abs((fecha2 - fecha1).days)

print(Fecha(25,6,2024) + 6)

print("--------------------------------------------------------")

#Ejercicio 2

class Alumno:
    def __init__(self, nombre:str, dni:int, fecha_ingreso:Fecha, carrera):
        self.datos = {
            "Nombre": nombre,
            "DNI": dni,
            "FechaIngreso": fecha_ingreso,
            "Carrera": carrera
        }

    def __str__(self):
        return f"Nombre: {self.datos['Nombre']}, DNI: {self.datos['DNI']}, Fecha Ingreso: {self.datos['FechaIngreso']}, Carrera: {self.datos['Carrera']}"

    def __eq__(self, otro_alumno):
        return self.datos["DNI"] == otro_alumno.datos["DNI"]

    def cambiar_datos(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.datos:
                self.datos[key] = value

    def antiguedad(self):
        hoy = Fecha()
        fecha_ingreso = Fecha(self.datos["FechaIngreso"].dia, self.datos["FechaIngreso"].mes, self.datos["FechaIngreso"].anio)
        return hoy.calcular_dif_fecha(fecha_ingreso)

alumn = Alumno("Lucas",44444444, Fecha(), "PROGRAMACION")
alumn.cambiar_datos(Nombre="Lucas",DNI=44252463,FechaIngreso=Fecha(20,6,2024),Carrera="CIENCIA")
print(alumn.datos["DNI"])
print(alumn.antiguedad())
print(alumn)

print("--------------------------------------------------------")

#Ejercicio 3

class Nodo:
    def __init__(self, dato:Alumno):
        self.dato:Alumno = dato
        self.siguiente:Nodo = None
        self.anterior:Nodo = None

class ListaDoblementeEnlazada:
    def __init__(self):
        self.cabeza:Nodo = None
        self.cola:Nodo = None
    
    def limpiar(self):
        self.cabeza:Nodo = None
        self.cola:Nodo = None

    def agregar(self, alumno:Alumno):
        nuevo_nodo = Nodo(alumno)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
        else:
            self.cola.siguiente = nuevo_nodo
            nuevo_nodo.anterior = self.cola
            self.cola = nuevo_nodo

    def __iter__(self):
        actual = self.cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

    def lista_ejemplo(self):
        nombres = ["Juan", "Maria", "Pedro", "Ana"]
        for i in range(4):
            fecha_ingreso = Fecha(random.randint(1, 28), random.randint(1, 12), random.randint(2010, 2023))
            alumno = Alumno(nombres[i], random.randint(10000000, 99999999), fecha_ingreso, "Carrera" + str(i+1))
            self.agregar(alumno)
        return self

listaEJ = ListaDoblementeEnlazada().lista_ejemplo()
for alm in listaEJ:
    print(alm)

print("--------------------------------------------------------")

#Ejercicio 4

def ordenar_lista(lista: ListaDoblementeEnlazada):
    if lista.cabeza is None:
        return lista

    cambiando = True
    while cambiando:
        cambiando = False
        actual = lista.cabeza
        while actual.siguiente is not None:
            actual_fecha_ingreso = actual.dato.datos["FechaIngreso"]
            siguiente_fecha_ingreso = actual.siguiente.dato.datos["FechaIngreso"]
            if siguiente_fecha_ingreso.calcular_dif_fecha(Fecha()) < actual_fecha_ingreso.calcular_dif_fecha(Fecha()):
                actual.dato, actual.siguiente.dato = actual.siguiente.dato, actual.dato
                cambiando = True
            actual = actual.siguiente
    return lista

listaEJ2 = ordenar_lista(ListaDoblementeEnlazada().lista_ejemplo())
for alm in listaEJ2:
    print(alm)
    
print("--------------------------------------------------------")
    
#Ejercicio 5

def manejar_directorios(lista_alumnos:ListaDoblementeEnlazada,dir:str,nuevo_dir:str):
    dir = comprobarDir(dir)
    nuevo_dir = comprobarDir(nuevo_dir)
    archivo = "lista_alumnos.txt"

    # Creando el directoroi para guardar el archivo de lista de aumnos
    if not os.path.exists(dir):
        os.makedirs(dir)

    # Guardando lista de alumnos en un archivo txt
    with open(os.path.join(dir, archivo), 'w') as f:
        for alumno in lista_alumnos:
            f.write(str(alumno) + "\n")

    # Mover el directorio
    if os.path.exists(dir):
        os.rename(dir, nuevo_dir)

    print(os.path.join(nuevo_dir, archivo))
    
    # Borrar archivo y directorio
    if os.path.exists(os.path.join(nuevo_dir, archivo)):
        os.remove(os.path.join(nuevo_dir, archivo))

    if os.path.exists(nuevo_dir):
        os.rmdir(nuevo_dir)

def comprobarDir(dir:str):
    if os.path.exists(dir):
        print("El directorio ya existe, inserte un nuevo directorio a continuacion")
        dir = input()
        return comprobarDir(dir)
    else:
        return dir

listaEJ3 = ordenar_lista(ListaDoblementeEnlazada().lista_ejemplo())
manejar_directorios(listaEJ3,"Dir1","nuevo_alumnos_dir")
