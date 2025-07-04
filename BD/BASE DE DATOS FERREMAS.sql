DROP SEQUENCE DETALLE_PEDIDO_SEQ;
DROP SEQUENCE PEDIDO_SEQ;
DROP SEQUENCE SEQ_USUARIO;
DROP SEQUENCE PRODUCTO_SEQ;
DROP SEQUENCE PAGO_SEQ;
DROP TABLE PAGO CASCADE CONSTRAINTS;
DROP TABLE INVENTARIO CASCADE CONSTRAINTS;
DROP TABLE DETALLE_PEDIDO CASCADE CONSTRAINTS;
DROP TABLE PEDIDO CASCADE CONSTRAINTS;
DROP TABLE PRODUCTO CASCADE CONSTRAINTS;
DROP TABLE SUCURSAL CASCADE CONSTRAINTS;
DROP TABLE ESTADO CASCADE CONSTRAINTS;
DROP TABLE USUARIO CASCADE CONSTRAINTS;
DROP TABLE METODO_PAGO CASCADE CONSTRAINTS;
DROP TABLE ESTADO_PAGO CASCADE CONSTRAINTS;
DROP TABLE CATEGORIA CASCADE CONSTRAINTS;
DROP TABLE MARCA CASCADE CONSTRAINTS;
DROP TABLE COMUNA CASCADE CONSTRAINTS;
DROP TABLE REGION CASCADE CONSTRAINTS;
DROP TABLE ROL CASCADE CONSTRAINTS;
DROP TABLE TIPO_DESPACHO CASCADE CONSTRAINTS;
-- Creación
CREATE SEQUENCE DETALLE_PEDIDO_SEQ
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

CREATE SEQUENCE PEDIDO_SEQ
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

CREATE SEQUENCE SEQ_USUARIO
    START WITH 11
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

CREATE SEQUENCE PRODUCTO_SEQ
    START WITH 5
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

CREATE SEQUENCE PAGO_SEQ 
    START WITH 1 
    INCREMENT BY 1 
    NOCACHE;

-- Tabla ROL
CREATE TABLE ROL (
    rol_id NUMBER(1) PRIMARY KEY,
    nombre VARCHAR2(50) NOT NULL
);

-- Tabla REGION
CREATE TABLE REGION (
    region_id NUMBER(10) PRIMARY KEY,
    nombre VARCHAR2(100) NOT NULL
);

-- Tabla COMUNA
CREATE TABLE COMUNA (
    comuna_id NUMBER(10) PRIMARY KEY,
    nombre VARCHAR2(100) NOT NULL,
    region_id NUMBER(10) NOT NULL,
    CONSTRAINT COMUNA_REGION_FK FOREIGN KEY (region_id) 
        REFERENCES REGION(region_id) ON DELETE CASCADE
);

-- Tabla MARCA
CREATE TABLE MARCA (
    marca_id NUMBER(10) PRIMARY KEY,
    nombre VARCHAR2(100) NOT NULL
);

-- Tabla CATEGORIA
CREATE TABLE CATEGORIA (
    categoria_id NUMBER(10) PRIMARY KEY,
    nombre VARCHAR2(100) NOT NULL,
    descripcion VARCHAR2(200)
);

-- Tabla ESTADO_PAGO
CREATE TABLE ESTADO_PAGO (
    estado_pago_id NUMBER(10) PRIMARY KEY,
    nombre VARCHAR2(100) NOT NULL
);

-- Tabla METODO_PAGO
CREATE TABLE METODO_PAGO (
    metodo_pago NUMBER(10) PRIMARY KEY,
    nombre VARCHAR2(100) NOT NULL
);

-- Tabla USUARIO
CREATE TABLE USUARIO (
    id_usuario NUMBER(10) PRIMARY KEY,
    rut CHAR(12) NOT NULL UNIQUE,
    nombre VARCHAR2(100) NOT NULL,
    apellido_p VARCHAR2(100) NOT NULL,
    apellido_m VARCHAR2(100),
    snombre VARCHAR2(100),
    email VARCHAR2(100) NOT NULL UNIQUE,
    fono VARCHAR2(20),
    direccion VARCHAR2(200),
    password VARCHAR2(200) NOT NULL,
    debe_cambiar_password NUMBER(1) NOT NULL,
    rol_id number(1) NOT NULL,
    CONSTRAINT USUARIO_ROL_FK FOREIGN KEY (rol_id)
	REFERENCES ROL(rol_id) ON DELETE CASCADE
);

-- Tabla TIPO_DESPACHO
CREATE TABLE TIPO_DESPACHO (
    tipo_despacho_id NUMBER(10) PRIMARY KEY,
    nombre VARCHAR2(100) NOT NULL
);

-- Tabla ESTADO
CREATE TABLE ESTADO (
    estado_id NUMBER(10) PRIMARY KEY,
    nombre VARCHAR2(100) NOT NULL
);

-- Tabla SUCURSAL
CREATE TABLE SUCURSAL (
    sucursal_id NUMBER(10) PRIMARY KEY,
    nombre VARCHAR2(100) NOT NULL,
    direccion VARCHAR2(200) NOT NULL,
    comuna_id NUMBER(10) NOT NULL,
    fono VARCHAR2(20),
    responsable_id NUMBER(10),
    CONSTRAINT SUCURSAL_COMUNA_FK FOREIGN KEY (comuna_id) 
        REFERENCES COMUNA(comuna_id) ON DELETE CASCADE,
    CONSTRAINT SUCURSAL_USUARIO_FK FOREIGN KEY (responsable_id) 
        REFERENCES USUARIO(id_usuario)
);

-- Tabla PRODUCTO
CREATE TABLE PRODUCTO (
    producto_id NUMBER(10) PRIMARY KEY,
    nombre VARCHAR2(100) NOT NULL,
    descripcion VARCHAR2(300),
    precio NUMBER(10) NOT NULL,
    STOCK NUMBER(10) DEFAULT 0 NOT NULL,
    categoria_id NUMBER(10) NOT NULL,
    marca_id NUMBER(10) NOT NULL,
    imagen CLOB,
    CONSTRAINT PRODUCTO_CATEGORIA_FK FOREIGN KEY (categoria_id) 
        REFERENCES CATEGORIA(categoria_id) ON DELETE CASCADE,
    CONSTRAINT PRODUCTO_MARCA_FK FOREIGN KEY (marca_id) 
        REFERENCES MARCA(marca_id) ON DELETE CASCADE
);

-- Tabla PEDIDO
CREATE TABLE PEDIDO (
    pedido_id NUMBER(10) PRIMARY KEY,
    cliente_id NUMBER(10) NOT NULL,
    fecha_pedido DATE DEFAULT SYSDATE NOT NULL,
    estado_id NUMBER(10) NOT NULL,
    sucursal_retiro NUMBER(10),
    total NUMBER(10) NOT NULL,
    vendedor_id NUMBER(10) NOT NULL,
    tipo_despacho_id NUMBER(10) NOT NULL,
    CONSTRAINT PEDIDO_ESTADO_FK FOREIGN KEY (estado_id) 
        REFERENCES ESTADO(estado_id) ON DELETE CASCADE,
    CONSTRAINT PEDIDO_USUARIO_FK FOREIGN KEY (cliente_id) 
        REFERENCES USUARIO(id_usuario) ON DELETE CASCADE,
    CONSTRAINT PEDIDO_SUCURSAL_FK FOREIGN KEY (sucursal_retiro) 
        REFERENCES SUCURSAL(sucursal_id) ON DELETE SET NULL,
    CONSTRAINT PEDIDO_VENDEDOR_FK FOREIGN KEY (vendedor_id) 
        REFERENCES USUARIO(id_usuario) ON DELETE CASCADE,
    CONSTRAINT PEDIDO_TIPO_DESPACHO_FK FOREIGN KEY (tipo_despacho_id) 
        REFERENCES TIPO_DESPACHO(tipo_despacho_id) ON DELETE CASCADE
);

-- Tabla DETALLE_PEDIDO
CREATE TABLE DETALLE_PEDIDO (
    detalle_id NUMBER(10) PRIMARY KEY,
    pedido_id NUMBER(10) NOT NULL,
    producto_id NUMBER(10) NOT NULL,
    cantidad NUMBER(10) NOT NULL,
    precio_unit NUMBER(10) NOT NULL,
    CONSTRAINT DETALLE_PEDIDO_PRODUCTO_FK FOREIGN KEY (producto_id) 
        REFERENCES PRODUCTO(producto_id) ON DELETE CASCADE,
    CONSTRAINT DETALLE_PEDIDO_PEDIDO_FK FOREIGN KEY (pedido_id) 
        REFERENCES PEDIDO(pedido_id) ON DELETE CASCADE
);


-- Tabla PAGO
CREATE TABLE PAGO (
    pago_id NUMBER(10) PRIMARY KEY,
    pedido_id NUMBER(10) NOT NULL,
    metodo_pago_id NUMBER(10) NOT NULL,
    monto NUMBER(10) NOT NULL,
    fecha_pago DATE DEFAULT SYSDATE NOT NULL,
    estado_pago_id NUMBER(10) NOT NULL,
    transaccion_id VARCHAR2(200),
    detalle CLOB,
    contador_id NUMBER(10),
    CONSTRAINT PAGO_PEDIDO_FK FOREIGN KEY (pedido_id) 
        REFERENCES PEDIDO(pedido_id) ON DELETE CASCADE,
    CONSTRAINT PAGO_METODO_PAGO_FK FOREIGN KEY (metodo_pago_id) 
        REFERENCES METODO_PAGO(metodo_pago) ON DELETE CASCADE,
    CONSTRAINT PAGO_ESTADO_PAGO_FK FOREIGN KEY (estado_pago_id) 
        REFERENCES ESTADO_PAGO(estado_pago_id) ON DELETE CASCADE,
    CONSTRAINT PAGO_USUARIO_FK FOREIGN KEY (contador_id) 
        REFERENCES USUARIO(id_usuario) ON DELETE SET NULL
);

COMMIT;

INSERT INTO ROL (rol_id, nombre)
VALUES (1, 'Cliente');

INSERT INTO ROL (rol_id, nombre)
VALUES (2, 'Vendedor');

INSERT INTO ROL (rol_id, nombre)
VALUES (3, 'Administrador');

INSERT INTO ROL (rol_id, nombre)
VALUES (4, 'Bodeguero');

INSERT INTO ROL (rol_id, nombre)
VALUES (5, 'Contador');


-- Insertar usuarios con rol Cliente

INSERT INTO USUARIO (id_usuario, rut, nombre, apellido_p, apellido_m, snombre, email, fono, direccion, password, debe_cambiar_password, rol_id)
VALUES (3, '34567890-1', 'Carlos', 'Gómez', 'Vega', 'Javier', 'carlos.gomez@gmail.com', '923456789', 'Calle Bellavista 789, Valparaíso, Chile', 'carlos', 0, 2);

INSERT INTO USUARIO (id_usuario, rut, nombre, apellido_p, apellido_m, snombre, email, fono, direccion, password, debe_cambiar_password, rol_id)
VALUES (6, '67890123-4', 'Carla', 'Fernández', 'Muñoz', 'Gabriela', 'carla.fernandez@gmail.com', '956789012', 'Calle San Martín 987, Temuco, Chile', 'carla', 1, 3);


-- REGIONES
INSERT INTO REGION (region_id, nombre) VALUES (1, 'Región Metropolitana');
INSERT INTO REGION (region_id, nombre) VALUES (2, 'Región de Valparaíso');
INSERT INTO REGION (region_id, nombre) VALUES (3, 'Región del Biobío');

-- COMUNAS
INSERT INTO COMUNA (comuna_id, nombre, region_id) VALUES (1, 'Santiago', 1);
INSERT INTO COMUNA (comuna_id, nombre, region_id) VALUES (2, 'Puente Alto', 1);
INSERT INTO COMUNA (comuna_id, nombre, region_id) VALUES (3, 'Valparaíso', 2);
INSERT INTO COMUNA (comuna_id, nombre, region_id) VALUES (4, 'Concepción', 3);

-- MARCAS
INSERT INTO MARCA (marca_id, nombre) VALUES (1, 'Truper');
INSERT INTO MARCA (marca_id, nombre) VALUES (2, 'Bosch');
INSERT INTO MARCA (marca_id, nombre) VALUES (3, 'Stanley');
INSERT INTO MARCA (marca_id, nombre) VALUES (4, 'Makita');
INSERT INTO MARCA (marca_id, nombre) VALUES (5, 'DeWalt');
INSERT INTO MARCA (marca_id, nombre) VALUES (6, 'Black+Decker');
INSERT INTO MARCA (marca_id, nombre) VALUES (7, 'Hilti');
INSERT INTO MARCA (marca_id, nombre) VALUES (8, 'Irwin');
INSERT INTO MARCA (marca_id, nombre) VALUES (9, 'Bahco');
INSERT INTO MARCA (marca_id, nombre) VALUES (10, 'Klein Tools');
INSERT INTO MARCA (marca_id, nombre) VALUES (11, 'Milwaukee');
INSERT INTO MARCA (marca_id, nombre) VALUES (12, '3M');
INSERT INTO MARCA (marca_id, nombre) VALUES (13, 'Sodimac');
INSERT INTO MARCA (marca_id, nombre) VALUES (14, 'Volumen Industrial');
INSERT INTO MARCA (marca_id, nombre) VALUES (15, 'Hyundai');
INSERT INTO MARCA (marca_id, nombre) VALUES (16, 'Bosque Tools');

-- CATEGORIAS
INSERT INTO CATEGORIA (categoria_id, nombre, descripcion) VALUES (1, 'Herramientas Manuales', 'Herramientas de uso manual');
INSERT INTO CATEGORIA (categoria_id, nombre, descripcion) VALUES (2, 'Herramientas Eléctricas', 'Herramientas con motor eléctrico');
INSERT INTO CATEGORIA (categoria_id, nombre, descripcion) VALUES (3, 'Materiales de Construcción', 'Materiales básicos para construcción');
INSERT INTO CATEGORIA (categoria_id, nombre, descripcion) VALUES (4, 'Ferretería General', 'Artículos generales de ferretería');
INSERT INTO CATEGORIA (categoria_id, nombre, descripcion) VALUES (5, 'Pinturas y Adhesivos', 'Pinturas, barnices y adhesivos');
INSERT INTO CATEGORIA (categoria_id, nombre, descripcion) VALUES (6, 'Electricidad', 'Materiales y herramientas eléctricas');
INSERT INTO CATEGORIA (categoria_id, nombre, descripcion) VALUES (7, 'Plomería', 'Materiales y herramientas de plomería');
INSERT INTO CATEGORIA (categoria_id, nombre, descripcion) VALUES (8, 'Seguridad Industrial', 'Elementos de protección personal y seguridad');
INSERT INTO CATEGORIA (categoria_id, nombre, descripcion) VALUES (9, 'Jardinería', 'Herramientas y productos para jardín');
INSERT INTO CATEGORIA (categoria_id, nombre, descripcion) VALUES (10, 'Construcción Pesada', 'Materiales y herramientas para construcción pesada');
INSERT INTO CATEGORIA (categoria_id, nombre, descripcion) VALUES (11, 'Volumen Industrial', 'Productos para uso industrial y grandes volúmenes');
INSERT INTO CATEGORIA (categoria_id, nombre, descripcion) VALUES (12, 'Automotriz', 'Herramientas y productos automotrices');

-- ESTADO PEDIDO
INSERT INTO ESTADO (estado_id, nombre) VALUES (1, 'Pendiente');
INSERT INTO ESTADO (estado_id, nombre) VALUES (2, 'Entregado');
INSERT INTO ESTADO (estado_id, nombre) VALUES (3, 'Completado');
INSERT INTO ESTADO (estado_id, nombre) VALUES (4, 'Cancelado');

-- ESTADO PAGO
INSERT INTO ESTADO_PAGO (estado_pago_id, nombre) VALUES (1, 'Pagado');
INSERT INTO ESTADO_PAGO (estado_pago_id, nombre) VALUES (2, 'Pendiente');
INSERT INTO ESTADO_PAGO (estado_pago_id, nombre) VALUES (3, 'Rechazado');

-- METODO PAGO
INSERT INTO METODO_PAGO (metodo_pago, nombre) VALUES (1, 'Paypal');
INSERT INTO METODO_PAGO (metodo_pago, nombre) VALUES (4, 'Transferencia');

-- SUCURSALES
INSERT INTO SUCURSAL (sucursal_id, nombre, direccion, comuna_id, fono, responsable_id) VALUES (1, 'Sucursal Central', 'Av. Matucana 1001', 1, '226000001', 6);
INSERT INTO SUCURSAL (sucursal_id, nombre, direccion, comuna_id, fono, responsable_id) VALUES (2, 'Sucursal Valparaíso', 'Calle Blanco 123', 3, '322600002', 6);

-- PRODUCTOS


INSERT INTO TIPO_DESPACHO (tipo_despacho_id, nombre) VALUES (1, 'Despacho a domicilio');
INSERT INTO TIPO_DESPACHO (tipo_despacho_id, nombre) VALUES (2, 'Retiro en tienda');

-- PEDIDOS

-- DETALLE PEDIDO

-- PAGOS

commit;

select * from usuario;