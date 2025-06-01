import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from django.views.decorators.http import require_POST
import openpyxl
from openpyxl.utils import get_column_letter
from django.http import HttpResponse
from django.contrib.auth import logout as django_logout

# -------------------------------------------------------------------
# 9.  Transferencias pendientes para contador
# -------------------------------------------------------------------
def home(request):
    return render(request, 'core/index.html')

def carrito(request):
    return render(request, 'core/cart.html')

def listaproductos(request):
    url = 'http://localhost:3002/productos/'
    response = requests.get(url)
    
    if response.status_code == 200:
        productos = response.json()
        return render(request, 'core/listaproductos.html', {'productos': productos})
    else:
        messages.error(request, 'Error al cargar los productos')
        return redirect('home')  # Redirigir a la página de inicio en caso de error
    
def aprobacion_pagos(request):
    # Solo pagos con método transferencia (id=4), estado pendiente (id=2) y PEDIDO aprobado (estado_id=3)
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p.pago_id, p.pedido_id, p.monto, p.fecha_pago, p.estado_pago_id, ep.nombre AS estado_pago,
                   p.metodo_pago_id, mp.nombre AS metodo_pago, p.transaccion_id, p.detalle,
                   ped.cliente_id, u.nombre || ' ' || u.apellido_p AS cliente
            FROM PAGO p
            JOIN ESTADO_PAGO ep ON p.estado_pago_id = ep.estado_pago_id
            JOIN METODO_PAGO mp ON p.metodo_pago_id = mp.metodo_pago
            JOIN PEDIDO ped ON p.pedido_id = ped.pedido_id
            JOIN USUARIO u ON ped.cliente_id = u.id_usuario
            WHERE p.metodo_pago_id = 4
              AND p.estado_pago_id = 2
              AND ped.estado_id = 3
            ORDER BY p.fecha_pago DESC
        """)
        pagos = dictfetchall(cursor)
    return render(request, 'core/aprobacion_pagos.html', {'pagos': pagos})

def dictfetchall(cursor):
    "Devuelve todos los resultados como una lista de diccionarios"
    columns = [col[0].lower() for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

@require_POST
def aprobar_pago(request, pago_id):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE PAGO SET estado_pago_id = 1 WHERE pago_id = %s", [pago_id])  # 3 = Aprobado
    messages.success(request, 'Pago aprobado correctamente')
    return redirect('aprobacion_pagos')

@require_POST
def rechazar_pago(request, pago_id):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE PAGO SET estado_pago_id = 3 WHERE pago_id = %s", [pago_id])  # 4 = Rechazado
    messages.success(request, 'Pago rechazado correctamente')
    return redirect('aprobacion_pagos')

def gestion_pedidos(request):
    # Pedidos que no estén completados ni cancelados
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ped.pedido_id, ped.fecha_pedido, ped.estado_id, e.nombre AS estado,
                   ped.cliente_id, u.nombre || ' ' || u.apellido_p AS cliente, ped.total
            FROM PEDIDO ped
            JOIN ESTADO e ON ped.estado_id = e.estado_id
            JOIN USUARIO u ON ped.cliente_id = u.id_usuario
            WHERE ped.estado_id NOT IN (3, 4)
            ORDER BY ped.fecha_pedido DESC
        """)
        pedidos = dictfetchall(cursor)
    return render(request, 'core/gestion_pedidos.html', {'pedidos': pedidos})

@require_POST
def aprobar_pedido(request, pedido_id):
    # Estado 3 = Aprobado (ajusta según tu tabla ESTADO)
    with connection.cursor() as cursor:
        cursor.execute("UPDATE PEDIDO SET estado_id = 3 WHERE pedido_id = %s", [pedido_id])
    messages.success(request, 'Pedido aprobado correctamente')
    return redirect('gestion_pedidos')

@require_POST
def rechazar_pedido(request, pedido_id):
    # Estado 4 = Rechazado/Cancelado (ajusta según tu tabla ESTADO)
    with connection.cursor() as cursor:
        cursor.execute("UPDATE PEDIDO SET estado_id = 4 WHERE pedido_id = %s", [pedido_id])
    messages.success(request, 'Pedido rechazado correctamente')
    return redirect('gestion_pedidos')

def admin_usuarios(request):
    # Obtener usuarios desde la API
    response = requests.get('http://localhost:8001/usuarios/')
    usuarios = []
    if response.status_code == 200:
        usuarios = response.json()
    return render(request, 'core/admin_usuarios.html', {'usuarios': usuarios})
    
def agregar_usuario(request):
    if request.method == 'POST':
        data = {
            'rut': request.POST.get('rut', ''),
            'nombre': request.POST.get('nombre', ''),
            'apellido_p': request.POST.get('apellido_p', ''),
            'apellido_m': request.POST.get('apellido_m', ''),
            'snombre': request.POST.get('snombre', ''),
            'email': request.POST.get('email', ''),
            'fono': request.POST.get('fono', ''),
            'direccion': request.POST.get('direccion', ''),
            'password': request.POST.get('password', ''),
        }
        print("DATA ENVIADA:", data)
        # Envía los datos como params, no como json
        response = requests.post('http://localhost:8001/usuarios/', params=data)
        print("RESPUESTA:", response.status_code, response.text)
        if response.status_code == 201 or response.status_code == 200:
            messages.success(request, 'Usuario agregado correctamente')
        else:
            messages.error(request, f'Error al agregar usuario: {response.text}')
        return redirect('admin_usuarios')

    response = requests.get('http://localhost:8001/usuarios/')
    usuarios = []
    if response.status_code == 200:
        usuarios = response.json()
    return render(request, 'core/admin_usuarios.html', {'usuarios': usuarios})
   

def editar_usuario(request, id_actualizar):
    if request.method == 'POST':
        data = {
            'rut': request.POST['rut'],
            'nombre': request.POST['nombre'],
            'apellido_p': request.POST['apellido_p'],
            'apellido_m': request.POST['apellido_m'],
            'snombre': request.POST['snombre'],
            'email': request.POST['email'],
            'telefono': request.POST['telefono'],
            'direccion': request.POST['direccion'],
            'password': request.POST['password'],
            'rol': request.POST['rol'],
        }
        url = f'http://localhost:8001/usuarios/{id_actualizar}'
        response = requests.put(url, json=data)
        if response.status_code == 200:
            messages.success(request, 'Usuario actualizado correctamente')
        else:
            messages.error(request, 'Error al actualizar usuario')
    return redirect('admin_usuarios')

def eliminar_usuario(request, id_eliminar):
    url = f'http://localhost:8001/usuarios/{id_eliminar}'
    response = requests.delete(url)
    if response.status_code == 200:
        messages.success(request, 'Usuario eliminado correctamente')
    else:
        messages.error(request, 'Error al eliminar usuario')
    return redirect('admin_usuarios')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            response = requests.post(
                'http://localhost:8001/usuarios/login/',
                params={'email': email, 'password': password}
            )
            if response.status_code == 200:
                data = response.json()
                request.session['usuario_id'] = data.get('id_usuario')
                request.session['nombre'] = data.get('nombre')
                request.session['rol_id'] = data.get('rol_id')
                rol = data.get('rol_id')
                # Redirección según rol
                if rol == 1 or rol == 2:
                    return redirect('home')
                elif rol == 3:
                    return redirect('admin_usuarios')
                elif rol == 4:
                    return redirect('gestion_pedidos')
                elif rol == 5:
                    return redirect('aprobacion_pagos')
                else:
                    messages.error(request, 'Rol no reconocido.')
            else:
                messages.error(request, 'Correo o contraseña incorrectos.')
        except Exception as e:
            messages.error(request, f'Error de conexión: {e}')
    return render(request, 'core/login.html')

def logout(request):
    django_logout(request)  # Limpia la sesión
    return redirect('home')

def detalle_producto(request, producto_id):
    try:
        resp = requests.get(f'http://localhost:3002/productos/{producto_id}')
        resp.raise_for_status()
        producto = resp.json()
    except Exception:
        producto = None
    return render(request, 'core/detalle_producto.html', {'producto': producto})

def confirmar_pedido(request):
    return render(request, 'core/confirmar_pedido.html')

def dictfetchall(cursor):
    columns = [col[0].lower() for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def informe_pedidos(request):
    # Solo permitir acceso a administradores (rol_id == 3)
    if request.session.get('rol_id') != 3:
        return redirect('home')
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ped.pedido_id, ped.fecha_pedido, ped.total, e.nombre AS estado, u.nombre || ' ' || u.apellido_p AS cliente
            FROM PEDIDO ped
            JOIN ESTADO e ON ped.estado_id = e.estado_id
            JOIN USUARIO u ON ped.cliente_id = u.id_usuario
            ORDER BY ped.fecha_pedido DESC
        """)
        pedidos = dictfetchall(cursor)
    return render(request, 'core/informe_pedidos.html', {'pedidos': pedidos})

def descargar_informe_pedidos(request):
    if request.session.get('rol_id') != 3:
        return redirect('home')
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ped.pedido_id, ped.fecha_pedido, ped.total, e.nombre AS estado, u.nombre || ' ' || u.apellido_p AS cliente
            FROM PEDIDO ped
            JOIN ESTADO e ON ped.estado_id = e.estado_id
            JOIN USUARIO u ON ped.cliente_id = u.id_usuario
            ORDER BY ped.fecha_pedido DESC
        """)
        pedidos = dictfetchall(cursor)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Pedidos"
    headers = ["ID Pedido", "Fecha", "Cliente", "Estado", "Total"]
    ws.append(headers)
    for p in pedidos:
        ws.append([
            p['pedido_id'],
            str(p['fecha_pedido']),
            p['cliente'],
            p['estado'],
            float(p['total'])
        ])
    for i, col in enumerate(headers, 1):
        ws.column_dimensions[get_column_letter(i)].width = 18

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=pedidos.xlsx'
    wb.save(response)
    return response

def informe_pagos(request):
    # Solo permitir acceso a administradores (rol_id == 3)
    if request.session.get('rol_id') != 3:
        return redirect('home')
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p.pago_id, p.pedido_id, p.monto, p.fecha_pago, ep.nombre AS estado_pago,
                   mp.nombre AS metodo_pago, u.nombre || ' ' || u.apellido_p AS cliente
            FROM PAGO p
            JOIN ESTADO_PAGO ep ON p.estado_pago_id = ep.estado_pago_id
            JOIN METODO_PAGO mp ON p.metodo_pago_id = mp.metodo_pago
            JOIN PEDIDO ped ON p.pedido_id = ped.pedido_id
            JOIN USUARIO u ON ped.cliente_id = u.id_usuario
            ORDER BY p.fecha_pago DESC
        """)
        pagos = dictfetchall(cursor)
    return render(request, 'core/informe_pagos.html', {'pagos': pagos})

def descargar_informe_pagos(request):
    if request.session.get('rol_id') != 3:
        return redirect('home')
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p.pago_id, p.pedido_id, p.monto, p.fecha_pago, ep.nombre AS estado_pago,
                   mp.nombre AS metodo_pago, u.nombre || ' ' || u.apellido_p AS cliente
            FROM PAGO p
            JOIN ESTADO_PAGO ep ON p.estado_pago_id = ep.estado_pago_id
            JOIN METODO_PAGO mp ON p.metodo_pago_id = mp.metodo_pago
            JOIN PEDIDO ped ON p.pedido_id = ped.pedido_id
            JOIN USUARIO u ON ped.cliente_id = u.id_usuario
            ORDER BY p.fecha_pago DESC
        """)
        pagos = dictfetchall(cursor)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Pagos"
    headers = ["ID Pago", "ID Pedido", "Cliente", "Método de Pago", "Estado Pago", "Monto", "Fecha"]
    ws.append(headers)
    for p in pagos:
        ws.append([
            p['pago_id'],
            p['pedido_id'],
            p['cliente'],
            p['metodo_pago'],
            p['estado_pago'],
            float(p['monto']),
            str(p['fecha_pago'])
        ])
    for i, col in enumerate(headers, 1):
        ws.column_dimensions[get_column_letter(i)].width = 18

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=pagos.xlsx'
    wb.save(response)
    return response

def pedidos_para_entregar(request):
    # Solo mostrar si el usuario es vendedor
    if request.session.get('rol_id') != 2:
        return render(request, 'core/no_autorizado.html')

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p.pedido_id, u.nombre || ' ' || u.apellido_p AS cliente, p.fecha_pedido, p.total, e.nombre AS estado
            FROM PEDIDO p
            JOIN USUARIO u ON p.cliente_id = u.id_usuario
            JOIN ESTADO e ON p.estado_id = e.estado_id
            JOIN PAGO pa ON pa.pedido_id = p.pedido_id
            WHERE p.estado_id = 3 -- Completado
              AND pa.estado_pago_id = 1 -- Pagado
            ORDER BY p.fecha_pedido DESC
        """)
        pedidos = [
            {
                'pedido_id': row[0],
                'cliente': row[1],
                'fecha_pedido': row[2],
                'total': row[3],
                'estado': row[4],
            }
            for row in cursor.fetchall()
        ]
    return render(request, 'core/pedidos_para_entregar.html', {'pedidos': pedidos})