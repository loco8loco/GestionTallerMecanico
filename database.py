
"""
Gestión de Base de Datos con SQLAlchemy
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
import config

# URL de conexión
DATABASE_URL = f"postgresql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"

# Engine y Session
engine = create_engine(DATABASE_URL, pool_size=5, max_overflow=10, pool_timeout=30)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# ============================================================================
# MODELOS
# ============================================================================

class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True)
    nombre_usuario = Column(String(50), unique=True, nullable=False)
    hash_contraseña = Column(String(255), nullable=False)
    nombre_completo = Column(String(100))
    rol = Column(String(20), nullable=False)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

class Cliente(Base):
    __tablename__ = 'clientes'
    
    id = Column(Integer, primary_key=True)
    nombre_razon_social = Column(String(150), nullable=False)
    dni_nif = Column(String(20))
    direccion = Column(String(200))
    telefono = Column(String(20))
    email = Column(String(100))
    notas = Column(Text)
    fecha_alta = Column(DateTime, default=datetime.utcnow)
    
    vehiculos = relationship('Vehiculo', back_populates='cliente', cascade='all, delete-orphan')

class Vehiculo(Base):
    __tablename__ = 'vehiculos'
    
    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id', ondelete='CASCADE'))
    matricula = Column(String(20), unique=True, nullable=False)
    marca = Column(String(50))
    modelo = Column(String(50))
    bastidor = Column(String(50))
    km_actual = Column(Integer, default=0)
    fecha_alta = Column(DateTime, default=datetime.utcnow)
    
    cliente = relationship('Cliente', back_populates='vehiculos')
    ordenes = relationship('OrdenReparacion', back_populates='vehiculo')

class OrdenReparacion(Base):
    __tablename__ = 'ordenes_reparacion'
    
    id = Column(Integer, primary_key=True)
    vehiculo_id = Column(Integer, ForeignKey('vehiculos.id'))
    mecanico_id = Column(Integer, ForeignKey('usuarios.id'))
    fecha_entrada = Column(DateTime, default=datetime.utcnow)
    fecha_salida = Column(DateTime)
    estado = Column(String(20), default='pendiente')
    descripcion_averia = Column(Text)
    observaciones = Column(Text)
    mano_obra = Column(Numeric(10, 2), default=0)
    repuestos = Column(Numeric(10, 2), default=0)
    total = Column(Numeric(10, 2), default=0)
    
    vehiculo = relationship('Vehiculo', back_populates='ordenes')
    mecanico = relationship('Usuario')
    factura = relationship('Factura', back_populates='orden', uselist=False)

class Factura(Base):
    __tablename__ = 'facturas'
    
    id = Column(Integer, primary_key=True)
    orden_id = Column(Integer, ForeignKey('ordenes_reparacion.id'))
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    numero_factura = Column(String(50), unique=True)
    fecha_emision = Column(DateTime, default=datetime.utcnow)
    base_imponible = Column(Numeric(10, 2), default=0)
    iva = Column(Numeric(10, 2), default=0)
    total = Column(Numeric(10, 2), default=0)
    estado_pago = Column(String(20), default='pendiente')
    
    orden = relationship('OrdenReparacion', back_populates='factura')
    cliente = relationship('Cliente')

class Configuracion(Base):
    __tablename__ = 'configuracion'
    
    id = Column(Integer, primary_key=True)
    clave = Column(String(50), unique=True, nullable=False)
    valor = Column(Text)
    tipo = Column(String(20), default='texto')

class Licencia(Base):
    __tablename__ = 'licencias'
    
    id = Column(Integer, primary_key=True)
    tipo = Column(String(20), nullable=False)
    fecha_activacion = Column(DateTime, default=datetime.utcnow)
    fecha_expiracion = Column(DateTime)
    hash_hardware = Column(String(255))
    clave_licencia = Column(String(255))
    activa = Column(Boolean, default=True)

# ============================================================================
# FUNCIONES DE INICIALIZACIÓN
# ============================================================================

def crear_tablas():
    """Crea todas las tablas en la base de datos"""
    Base.metadata.create_all(engine)
    
    # Insertar datos iniciales
    session = Session()
    try:
        # Usuario admin por defecto
        admin = session.query(Usuario).filter_by(nombre_usuario='admin').first()
        if not admin:
            admin = Usuario(
                nombre_usuario='admin',
                hash_contraseña='admin123',  # ⚠️ En producción usar hash real
                nombre_completo='Administrador',
                rol='jefe'
            )
            session.add(admin)
        
        # Configuración inicial
        configs = [
            ('titulo_app', 'Taller Mecánico', 'texto'),
            ('fondo_pantalla', '', 'imagen'),
            ('icono_app', '', 'imagen')
        ]
        
        for clave, valor, tipo in configs:
            config_existente = session.query(Configuracion).filter_by(clave=clave).first()
            if not config_existente:
                session.add(Configuracion(clave=clave, valor=valor, tipo=tipo))
        
        session.commit()
        print("✓ Base de datos inicializada correctamente")
        
    except Exception as e:
        session.rollback()
        print(f"✗ Error al inicializar: {e}")
    finally:
        session.close()

if __name__ == '__main__':
    crear_tablas()
