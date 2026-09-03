"""
Punto de entrada de la aplicación
"""

import sys
from PyQt5.QtWidgets import QApplication
from ui.login_window import LoginWindow
from license import LicenseManager

def main():
    """Función principal"""
    app = QApplication(sys.argv)
    
    # Verificar licencia
    valida, mensaje = LicenseManager.verificar_licencia()
    if not valida:
        print(f"Licencia no válida: {mensaje}")
        # En producción, mostrar diálogo y salir
        # Por ahora continuamos para desarrollo
    
    # Mostrar ventana de login
    login = LoginWindow()
    login.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
