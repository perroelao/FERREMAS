from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("carrito/", views.carrito, name="carrito"),
    path('logout/', views.logout, name='logout'),
    path("listaproductos/", views.listaproductos, name="listaproductos"),
    path('aprobacion-pagos/', views.aprobacion_pagos, name='aprobacion_pagos'),
    path('aprobacion-pagos/aprobar/<int:pago_id>/', views.aprobar_pago, name='aprobar_pago'),
    path('aprobacion-pagos/rechazar/<int:pago_id>/', views.rechazar_pago, name='rechazar_pago'),
    path("gestion_pedidos/", views.gestion_pedidos, name="gestion_pedidos"),
    path('gestion-pedidos/aprobar/<int:pedido_id>/', views.aprobar_pedido, name='aprobar_pedido'),
    path('gestion-pedidos/rechazar/<int:pedido_id>/', views.rechazar_pedido, name='rechazar_pedido'),
    path("adminview/usuarios/", views.admin_usuarios, name="admin_usuarios"),
    path("adminview/usuarios/agregar/", views.agregar_usuario, name="agregar_usuario"),
    path("adminview/usuarios/editar/<int:id_actualizar>/", views.editar_usuario, name="editar_usuario"),
    path("adminview/usuarios/eliminar/<int:id_eliminar>/", views.eliminar_usuario, name="eliminar_usuario"),
]