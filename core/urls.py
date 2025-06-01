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
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('confirmar_pedido/', views.confirmar_pedido, name='confirmar_pedido'),
    path('informe_pedidos/', views.informe_pedidos, name='informe_pedidos'),
    path('descargar_informe_pedidos/', views.descargar_informe_pedidos, name='descargar_informe_pedidos'),
    path('informe_pagos/', views.informe_pagos, name='informe_pagos'),
    path('descargar_informe_pagos/', views.descargar_informe_pagos, name='descargar_informe_pagos'),
    path('pedidos-para-entregar/', views.pedidos_para_entregar, name='pedidos_para_entregar'),
]