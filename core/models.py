from django.db import models

class Region(models.Model):
    region_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'region'

class Comuna(models.Model):
    comuna_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'comuna'

class Rol(models.Model):
    rol_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    class Meta:
        db_table = 'rol'

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    apellido_p = models.CharField(max_length=100)
    apellido_m = models.CharField(max_length=100, blank=True, null=True)
    snombre = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, unique=True)
    fono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    password = models.CharField(max_length=200)
    rol = models.ForeignKey(Rol, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'usuario'

class Categoria(models.Model):
    categoria_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'categoria'

class Marca(models.Model):
    marca_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'marca'

class Producto(models.Model):
    producto_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=300, blank=True, null=True)
    precio = models.IntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    marca = models.ForeignKey(Marca, on_delete=models.DO_NOTHING)
    imagen = models.BinaryField(blank=True, null=True)

    class Meta:
        db_table = 'producto'

class Estado(models.Model):
    estado_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'estado'

class EstadoPago(models.Model):
    estado_pago_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'estado_pago'

class MetodoPago(models.Model):
    metodo_pago = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'metodo_pago'

class Sucursal(models.Model):
    sucursal_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    comuna = models.ForeignKey(Comuna, on_delete=models.DO_NOTHING)
    fono = models.CharField(max_length=20, blank=True, null=True)
    responsable = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'sucursal'

class Inventario(models.Model):
    inventario_id = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.DO_NOTHING)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.DO_NOTHING)
    stock = models.IntegerField()

    class Meta:
        db_table = 'inventario'
        unique_together = (('producto', 'sucursal'),)

class Pedido(models.Model):
    pedido_id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
    fecha_pedido = models.DateField(auto_now_add=True)
    estado = models.ForeignKey(Estado, on_delete=models.DO_NOTHING)
    sucursal_retiro = models.ForeignKey(Sucursal, on_delete=models.DO_NOTHING, blank=True, null=True)
    total = models.IntegerField()
    vendedor = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, related_name='pedido_vendedor_set')

    class Meta:
        db_table = 'pedido'

class DetallePedido(models.Model):
    detalle_id = models.AutoField(primary_key=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.DO_NOTHING)
    producto = models.ForeignKey(Producto, on_delete=models.DO_NOTHING)
    cantidad = models.IntegerField()
    precio_unit = models.IntegerField()

    class Meta:
        db_table = 'detalle_pedido'

class Pago(models.Model):
    pago_id = models.AutoField(primary_key=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.DO_NOTHING)
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.DO_NOTHING)
    monto = models.IntegerField()
    fecha_pago = models.DateField(auto_now_add=True)
    estado_pago = models.ForeignKey(EstadoPago, on_delete=models.DO_NOTHING)
    transaccion_id = models.CharField(max_length=200, blank=True, null=True)
    detalle = models.CharField(max_length=200, blank=True, null=True)
    contador = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'pago'