-- Eliminar tablas si existen
DROP TABLE IF EXISTS detalle_ventas CASCADE;
DROP TABLE IF EXISTS ventas CASCADE;
DROP TABLE IF EXISTS variantes_producto CASCADE;
DROP TABLE IF EXISTS productos CASCADE;
DROP TABLE IF EXISTS categorias CASCADE;
DROP TABLE IF EXISTS descuentos CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;
DROP TABLE IF EXISTS clientes CASCADE;
DROP TABLE IF EXISTS tiendas CASCADE;

-- TIENDAS
CREATE TABLE tiendas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    dominio VARCHAR(150) UNIQUE,
    color_primario VARCHAR(7),
    color_secundario VARCHAR(7),
    logo_url TEXT,
    activo BOOLEAN DEFAULT TRUE,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- USUARIOS
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    tienda_id INT NOT NULL REFERENCES tiendas(id) ON DELETE CASCADE,
    nombre VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL,
    password_hash TEXT NOT NULL,
    rol VARCHAR(50) CHECK (rol IN ('admin','vendedor')),
    activo BOOLEAN DEFAULT TRUE,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(tienda_id, email)
);

-- CLIENTES
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    tienda_id INT NOT NULL REFERENCES tiendas(id) ON DELETE CASCADE,
    nombre VARCHAR(150) NOT NULL,
    email VARCHAR(150),
    telefono VARCHAR(50),
    activo BOOLEAN DEFAULT TRUE,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- CATEGORIAS
CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    tienda_id INT NOT NULL REFERENCES tiendas(id) ON DELETE CASCADE,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE,

    UNIQUE(tienda_id, nombre)
);

-- PRODUCTOS
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    tienda_id INT NOT NULL REFERENCES tiendas(id) ON DELETE CASCADE,
    categoria_id INT REFERENCES categorias(id),
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índice para búsquedas por categoría
CREATE INDEX idx_productos_categoria ON productos(categoria_id);

-- VARIANTES_PRODUCTO
CREATE TABLE variantes_producto (
    id SERIAL PRIMARY KEY,
    producto_id INT NOT NULL REFERENCES productos(id) ON DELETE CASCADE,
    sku VARCHAR(100) NOT NULL,
    atributo_1 VARCHAR(100),
    atributo_2 VARCHAR(100),
    precio NUMERIC(10,2) NOT NULL CHECK (precio >= 0),
    stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0),
    activo BOOLEAN DEFAULT TRUE,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(producto_id, sku)
);

CREATE INDEX idx_variantes_producto_id ON variantes_producto(producto_id);

-- DESCUENTOS
CREATE TABLE descuentos (
    id SERIAL PRIMARY KEY,
    tienda_id INT NOT NULL REFERENCES tiendas(id) ON DELETE CASCADE,
    nombre VARCHAR(150) NOT NULL,
    porcentaje NUMERIC(5,2),
    monto_fijo NUMERIC(10,2),
    activo BOOLEAN DEFAULT TRUE,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CHECK (
        (porcentaje IS NOT NULL AND monto_fijo IS NULL)
        OR
        (porcentaje IS NULL AND monto_fijo IS NOT NULL)
    )
);

-- VENTAS
CREATE TABLE ventas (
    id SERIAL PRIMARY KEY,
    tienda_id INT NOT NULL REFERENCES tiendas(id) ON DELETE CASCADE,
    usuario_id INT NOT NULL REFERENCES usuarios(id),
    cliente_id INT REFERENCES clientes(id),
    descuento_id INT REFERENCES descuentos(id),
    subtotal NUMERIC(12,2) NOT NULL CHECK (subtotal >= 0),
    total NUMERIC(12,2) NOT NULL CHECK (total >= 0),
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ventas_fecha ON ventas(fecha);
CREATE INDEX idx_ventas_tienda ON ventas(tienda_id);

-- DETALLE_VENTAS
CREATE TABLE detalle_ventas (
    id SERIAL PRIMARY KEY,
    venta_id INT NOT NULL REFERENCES ventas(id) ON DELETE CASCADE,
    variante_id INT NOT NULL REFERENCES variantes_producto(id),
    cantidad INT NOT NULL CHECK (cantidad > 0),
    precio_unitario NUMERIC(10,2) NOT NULL CHECK (precio_unitario >= 0),
    subtotal NUMERIC(12,2) NOT NULL CHECK (subtotal >= 0)
);

CREATE INDEX idx_detalle_ventas_venta ON detalle_ventas(venta_id);
CREATE INDEX idx_detalle_ventas_variante ON detalle_ventas(variante_id);