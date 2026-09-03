"""
Sistema de Autenticación y Gestión de Roles
"""

import hashlib
from database import Session, Usuario
import config

class AuthManager:
    """Gestor de autenticación y roles"""
    
    @staticmethod
    def hash_password(password):
        """Genera hash de contraseña"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(password, hashed):
        """Verifica contraseña"""
        return AuthManager.hash_password(password) == hashed
    
    @staticmethod
    def login(username, password):
        """Inicia sesión y retorna usuario si es válido"""
        session = Session()
        try:
            user = session.query(Usuario).filter_by(
                nombre_usuario=username,
                activo=True
            ).first()
            
            if user and AuthManager.verify_password(password, user.hash_contraseña):
                return user
            return None
        finally:
            session.close()
    
    @staticmethod
    def tiene_permiso(rol, modulo):
        """Verifica si un rol tiene permiso para acceder a un módulo"""
        permisos = {
            'jefe': ['todos'],
            'oficina': ['clientes', 'vehiculos', 'ordenes', 'facturas', 'contabilidad'],
            'mecanico': ['ordenes_consulta']
        }
        
        if rol in permisos:
            return modulo in permisos[rol] or 'todos' in permisos[rol]
        return False
    
    @staticmethod
    def crear_usuario(username, password, nombre_completo, rol):
        """Crea un nuevo usuario"""
        session = Session()
        try:
            user = Usuario(
                nombre_usuario=username,
                hash_contraseña=AuthManager.hash_password(password),
                nombre_completo=nombre_completo,
                rol=rol
            )
            session.add(user)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error al crear usuario: {e}")
            return False
        finally:
            session.close()
