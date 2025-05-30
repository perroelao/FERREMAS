# FERREMAS

**FERREMAS** es una aplicación web para la gestión y venta de productos de ferretería, desarrollada con Django (frontend) y 2 APIs externas (Desarrolladas Express y FastAPI integradas a una base de datos Oracle) como backend para productos y usuarios.

---

## Características principales

- Listado de productos con información desde una API externa.
- Carrito de compras persistente en el navegador (localStorage).
- Descuento automático del 10% si compras 4 o más artículos.
- Checkout que envía el pedido a la API.
- Panel de administración y gestión de usuarios mediante la API de usuarios (FastAPI)
- Interfaz moderna y responsiva con Tailwind CSS.

---

## Requisitos

- Python 3.8+
- Django 4.x
- Node.js
- Oracle
- Navegador moderno

---

## Instalación y ejecución

### 1. Clona el repositorio

```sh
git clone https://github.com/perroelao/FERREMAS.git
cd ferremas
```

### 2. Instala dependencias de Django

```sh
pip install -r requirements.txt
```

### 3. Configura la base de datos y la API

- Las APIs corren en los puertos: (FastAPI-->8001, Express-->3002)
- Comando para correr las APIs:
  FastAPI
  Express
  (Respectivamente)
  ```sh
  uvicorn app.main:app --reload --port 8001
  ```
  ```sh
  node index.js
  ```

### 4. Ejecuta el servidor Django

```sh
python manage.py runserver
```

---

## Uso

- Accede a `http://localhost:8000/` en tu navegador.
- Navega a "Todos los Productos" para ver el catálogo.
- Agrega productos al carrito.
- Si compras 4 o más artículos, se aplica un 10% de descuento automáticamente.
- Finaliza la compra y el pedido se trabaja mediante las APIs

---

## Notas técnicas

- El carrito se guarda en `localStorage` del navegador.

---

## Créditos

Desarrollado por el equipo EIISREELTPUN.

---

¿Dudas o sugerencias?  jo.cisterna@duocuc.cl