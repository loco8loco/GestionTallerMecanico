"""
Ventana de Login
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                              QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from auth import AuthManager
from ui.main_window import MainWindow

class LoginWindow(QDialog):
    """Ventana de inicio de sesión"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz"""
        self.setWindowTitle('Login - Taller Mecánico')
        self.setFixedSize(400, 250)
        
        layout = QVBoxLayout()
        
        # Título
        titulo = QLabel('Taller Mecánico')
        titulo.setStyleSheet('font-size: 24px; font-weight: bold;')
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)
        
        layout.addSpacing(20)
        
        # Usuario
        layout.addWidget(QLabel('Usuario:'))
        self.input_usuario = QLineEdit()
        self.input_usuario.setPlaceholderText('nombre_usuario')
        layout.addWidget(self.input_usuario)
        
        # Contraseña
        layout.addWidget(QLabel('Contraseña:'))
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)
        self.input_password.setPlaceholderText('••••••••')
        layout.addWidget(self.input_password)
        
        layout.addSpacing(20)
        
        # Botón login
        btn_login = QPushButton('Iniciar Sesión')
        btn_login.setStyleSheet('padding: 10px; font-size: 14px;')
        btn_login.clicked.connect(self.login)
        layout.addWidget(btn_login)
        
        self.setLayout(layout)
    
    def login(self):
        """Procesa el login"""
        username = self.input_usuario.text().strip()
        password = self.input_password.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Complete todos los campos')
            return
        
        user = AuthManager.login(username, password)
        
        if user:
            self.accept()
            self.main_window = MainWindow(user)
            self.main_window.show()
        else:
            QMessageBox.critical(self, 'Error', 'Usuario o contraseña incorrectos')
