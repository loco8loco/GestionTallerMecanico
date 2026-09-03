"""
Sistema de Licencias
"""

import hashlib
import socket
import json
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from database import Session, Licencia
import config

class LicenseManager:
    """Gestor de licencias"""
    
    @staticmethod
    def get_hardware_hash():
        """Genera hash único del hardware"""
        hostname = socket.gethostname()
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) 
                       for ele in range(0, 8*6, 8)][::-1])
        data = f"{hostname}-{mac}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    @staticmethod
    def verificar_licencia():
        """Verifica si la licencia es válida"""
        session = Session()
        try:
            licencia = session.query(Licencia).filter_by(activa=True).first()
            
            if not licencia:
                return False, "No hay licencia activa"
            
            # Licencia de por vida (master key)
            if licencia.tipo == 'lifetime':
                if licencia.hash_hardware == LicenseManager.get_hardware_hash():
                    return True, "Licencia perpetua válida"
            
            # Licencia temporal
            elif licencia.tipo == 'temporal':
                if licencia.fecha_expiracion and datetime.utcnow() > licencia.fecha_expiracion:
                    return False, "Licencia expirada"
                return True, f"Licencia válida hasta {licencia.fecha_expiracion}"
            
            return False, "Licencia inválida"
            
        except Exception as e:
            return False, f"Error al verificar licencia: {e}"
        finally:
            session.close()
    
    @staticmethod
    def activar_licencia(clave_licencia):
        """Activa una licencia"""
        session = Session()
        try:
            # Verificar master key (licencia perpetua)
            if clave_licencia == config.MASTER_KEY:
                licencia = Licencia(
                    tipo='lifetime',
                    hash_hardware=LicenseManager.get_hardware_hash(),
                    clave_licencia=clave_licencia,
                    activa=True
                )
                session.add(licencia)
                session.commit()
                return True, "Licencia perpetua activada"
            
            # Aquí iría la lógica para licencias temporales
            return False, "Clave de licencia inválida"
            
        except Exception as e:
            session.rollback()
            return False, f"Error al activar licencia: {e}"
        finally:
            session.close()
