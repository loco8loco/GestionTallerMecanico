# Taller Mecánico - Sistema de Gestión

Sistema profesional de gestión para talleres mecánicos desarrollado en Python con PyQt5 y PostgreSQL.

## Características

- ✅ Gestión completa de clientes y vehículos
- ✅ Órdenes de reparación con seguimiento de estados
- ✅ Facturación automática
- ✅ Sistema de roles (Jefe, Oficina, Mecánico)
- ✅ Personalización de interfaz (fondo, iconos, título)
- ✅ Sistema de licencias (perpetua y temporal)
- ✅ Conexión por red LAN
- ✅ Optimizado para hardware limitado

## Requisitos

- Fedora 35 o superior
- PostgreSQL 14+
- Python 3.9+
- 2GB RAM mínimo

## Instalación

```bash
# 1. Clonar o descargar el proyecto
git clone [tu-repo]
cd taller_mecanico

# 2. Ejecutar instalador
chmod +x instalar.sh
./instalar.sh

# 3. Crear base de datos
python3 database.py

# 4. Ejecutar aplicación
python3 main.py
