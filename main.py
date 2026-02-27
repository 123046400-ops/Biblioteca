from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional

app = FastAPI(
    title=" Biblioteca Digital",
    description="Control de biblioteca digital",
    version="1.0"
)

# MOdelos 

class Usuario(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50)
    correo: EmailStr

class Libro(BaseModel):
    id: int = Field(..., gt=0)
    nombre: str = Field(..., min_length=2, max_length=100)
    autor: str
    anio: int = Field(..., gt=1450, le=datetime.now().year)
    paginas: int = Field(..., gt=1)
    estado: str = "disponible"  # o prestado

class Prestamo(BaseModel):
    libro_id: int
    usuario: Usuario

# BD  

libros = []
prestamos = []

# Creación de los endpoints


# a) Registrar libro
@app.post("/libros", status_code=201)
def RegistrarLibro(libro: Libro):
    for l in libros:
        if l["id"] == libro.id:
            raise HTTPException(status_code=400, detail="El libro ya existe")

    libros.append(libro.dict())
    return {"mensaje": "Libro registrado correctamente"}


# b) Listar todos los libros disponibles 
@app.get("/libros")
def ListarLibros():
    return libros


# c) Buscar libro por  su nombre
@app.get("/libros/buscar/{nombre}")
def BuscarLibro(nombre: str):
    for libro in libros:
        if nombre.lower() in libro["nombre"].lower():
            return libro

    return {"mensaje": "No se encontro el libro "}


# d) Registrar préstamo de un libro a un usuario
@app.post("/prestamos")
def RegistrarPrestamo(prestamo: Prestamo):

    for libro in libros:
        if libro["id"] == prestamo.libro_id:

            if libro["estado"] == "prestado":
                raise HTTPException(status_code=409, detail="El libro ya se encuentra  prestado")

            libro["estado"] = "prestado"
            prestamos.append(prestamo.dict())
            return {"mensaje": "Préstamo registrado correctamente"}

    raise HTTPException(status_code=404, detail="Libro no encontrado")


# e) Marcar un libro como devuelto
@app.put("/prestamos/devolver/{libro_id}")
def DevolverLibro(libro_id: int):

    for libro in libros:
        if libro["id"] == libro_id:
            libro["estado"] = "disponible"
            return {"mensaje": "Libro devuelto correctamente"}

    raise HTTPException(status_code=404, detail="Libro no encontrado")


# f) Eliminar el registro de un prestamo
@app.delete("/prestamos/{libro_id}")
def EliminarPrestamo(libro_id: int):

    for prestamo in prestamos:
        if prestamo["libro_id"] == libro_id:
            prestamos.remove(prestamo)
            return {"mensaje": "Préstamo eliminado"}

    raise HTTPException(status_code=409, detail="El registro de préstamo ya no existe ")