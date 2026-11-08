from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Dict

app = FastAPI(title="API Bodega - Reto Integrador")

# Modelo Pydantic con al menos 3 campos
class Producto(BaseModel):
    nombre: str
    precio: float
    stock: int

# Base de datos simulada en memoria
productos_db: Dict[int, dict] = {
    1: {"nombre": "Arroz 1kg", "precio": 4.50, "stock": 50},
    2: {"nombre": "Aceite 1L", "precio": 9.20, "stock": 30}
}

# 1. Endpoint: Listar todos los productos
@app.get("/productos", status_code=status.HTTP_200_OK)
def listar_productos():
    return productos_db

# 2. Endpoint: Obtener un producto por ID (con error 404)
@app.get("/productos/{producto_id}", status_code=status.HTTP_200_OK)
def obtener_producto(producto_id: int):
    if producto_id not in productos_db:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return productos_db[producto_id]

# 3. Endpoint: Crear un nuevo producto (con código 201)
@app.post("/productos", status_code=status.HTTP_201_CREATED)
def crear_producto(producto: Producto):
    nuevo_id = max(productos_db.keys(), default=0) + 1
    productos_db[nuevo_id] = producto.model_dump()
    return {"id": nuevo_id, **productos_db[nuevo_id]}

# 4. Endpoint: Actualizar un producto existente
@app.put("/productos/{producto_id}", status_code=status.HTTP_200_OK)
def actualizar_producto(producto_id: int, producto: Producto):
    if producto_id not in productos_db:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    productos_db[producto_id] = producto.model_dump()
    return productos_db[producto_id]

# 5. Endpoint: Eliminar un producto (con código 204)
@app.delete("/productos/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(producto_id: int):
    if producto_id not in productos_db:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    del productos_db[producto_id]
    return None