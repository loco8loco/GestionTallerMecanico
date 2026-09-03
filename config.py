"""
Configuración centralizada de la aplicación
"""

# Configuración de Base de Datos
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'taller_db'
DB_USER = 'taller_user'
DB_PASSWORD = 'tu_contraseña_aqui'  # ⚠️ Cambiar después de instalar

# Configuración de la Aplicación
APP_NAME = 'Taller Mecánico'
APP_VERSION = '1.0.0'
APP_ICON = 'icon.png'

# Roles de usuario
ROL_JEFE = 'jefe'
ROL_OFICINA = 'oficina'
ROL_MECANICO = 'mecanico'

# Estados de órdenes
ESTADO_PENDIENTE = 'pendiente'
ESTADO_EN_PROCESO = 'en_proceso'
ESTADO_TERMINADO = 'terminado'
ESTADO_ENTREGADO = 'entregado'

# Estados de facturas
FACTURA_PAGADA = 'pagada'
FACTURA_PENDIENTE = 'pendiente'

# Configuración de red
NETWORK_TIMEOUT = 30  # segundos
MAX_CONNECTIONS = 20

# Configuración de licencias
LICENSE_FILE = 'license.dat'
MASTER_KEY = 'TU_CLAVE_MAESTRA_AQUI'  # ⚠️ Cambiar
