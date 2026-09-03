
---

## 📄 Archivo 2: `instalar.sh`

```bash
#!/bin/bash

# ============================================================================
# INSTALADOR COMPLETO - TALLER MECÁNICO
# ============================================================================

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     INSTALADOR TALLER MECÁNICO - Fedora 35                ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

VERDE='\033[0;32m'
ROJO='\033[0;31m'
NC='\033[0m'

error_exit() {
    echo -e "${ROJO}ERROR: $1${NC}" >&2
    exit 1
}

echo -e "${VERDE}[1/7] Actualizando sistema...${NC}"
sudo dnf update -y || error_exit "Error al actualizar"

echo -e "${VERDE}[2/7] Instalando PostgreSQL y dependencias...${NC}"
sudo dnf install -y postgresql-server postgresql-contrib python3-pip python3-qt5 python3-sqlalchemy python3-psycopg2 || error_exit "Error en instalación"

echo -e "${VERDE}[3/7] Inicializando PostgreSQL...${NC}"
if [ ! -f /var/lib/pgsql/data/PG_VERSION ]; then
    sudo postgresql-setup --initdb
fi

echo -e "${VERDE}[4/7] Configurando PostgreSQL...${NC}"

sudo cp /var/lib/pgsql/data/postgresql.conf /var/lib/pgsql/data/postgresql.conf.backup 2>/dev/null || true
sudo cp /var/lib/pgsql/data/pg_hba.conf /var/lib/pgsql/data/pg_hba.conf.backup 2>/dev/null || true

sudo tee /var/lib/pgsql/data/postgresql.conf > /dev/null <<'EOF'
listen_addresses = '*'
max_connections = 20
shared_buffers = 256MB
effective_cache_size = 512MB
work_mem = 4MB
maintenance_work_mem = 64MB
wal_buffers = 8MB
checkpoint_completion_target = 0.9
log_destination = 'stderr'
logging_collector = on
log_directory = 'log'
log_filename = 'postgresql-%Y-%m-%d.log'
log_rotation_age = 1d
log_rotation_size = 10MB
log_min_messages = warning
password_encryption = scram-sha-256
EOF

sudo tee /var/lib/pgsql/data/pg_hba.conf > /dev/null <<'EOF'
local   all             all                                     peer
host    all             all             127.0.0.1/32            scram-sha-256
host    all             all             ::1/128                 scram-sha-256
host    all             all             192.168.1.0/24          scram-sha-256
host    all             all             192.168.0.0/24          scram-sha-256
host    all             all             10.0.0.0/8              scram-sha-256
EOF

sudo chown postgres:postgres /var/lib/pgsql/data/postgresql.conf
sudo chown postgres:postgres /var/lib/pgsql/data/pg_hba.conf
sudo chmod 600 /var/lib/pgsql/data/postgresql.conf
sudo chmod 600 /var/lib/pgsql/data/pg_hba.conf

echo -e "${VERDE}[5/7] Iniciando PostgreSQL...${NC}"
sudo systemctl enable postgresql
sudo systemctl start postgresql

echo -e "${VERDE}[6/7] Configurando firewall...${NC}"
sudo firewall-cmd --zone=public --add-port=5432/tcp --permanent
sudo firewall-cmd --reload

echo -e "${VERDE}[7/7] Creando usuario y base de datos...${NC}"
read -p "Introduce contraseña para taller_user: " -s PASSWORD
echo ""

sudo -i -u postgres psql <<EOF
DROP USER IF EXISTS taller_user;
CREATE USER taller_user WITH PASSWORD '$PASSWORD';
DROP DATABASE IF EXISTS taller_db;
CREATE DATABASE taller_db OWNER taller_user;
GRANT ALL PRIVILEGES ON DATABASE taller_db TO taller_user;
EOF

# Guardar contraseña en config.py
sed -i "s/DB_PASSWORD = '.*'/DB_PASSWORD = '$PASSWORD'/" config.py

echo ""
echo -e "${VERDE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${VERDE}║     INSTALACIÓN COMPLETADA                                ║"
echo -e "${VERDE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Próximo paso: python3 database.py"
