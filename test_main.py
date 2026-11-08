from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_crear_producto():
    response = client.post(
        "/productos",
        json={"nombre": "Galletas", "precio": 1.50, "stock": 20}
    )
    assert response.status_code == 201
    assert response.json()["nombre"] == "Galletas"

def test_obtener_productos():
    response = client.get("/productos")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_producto_no_encontrado():
    response = client.get("/productos/999")
    assert response.status_code == 404