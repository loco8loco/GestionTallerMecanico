"""
Ventana Principal
"""

from PyQt5.QtWidgets import (QMainWindow, QAction, QMenuBar, QStatusBar,
                              QLabel, QMessageBox)
from PyQt5.QtCore import Qt
from auth import AuthManager
from ui.clientes_window import ClientesWindow
from ui.vehiculos_window import VehiculosWindow
from ui.ordenes_window import OrdenesWindow
from ui.facturas_window import FacturasWindow
from ui.config_window import ConfigWindow
import config

class MainWindow(QMainWindow):
    """Ventana principal de la aplicación"""
    
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz"""
        self.setWindowTitle(config.APP_NAME)
        self.setGeometry(100, 100, 1200, 800)
        
        # Menú principal
        self.crear_menu()
        
        # Barra de estado
        self.statusBar().showMessage(f'Usuario: {self.usuario.nombre_completo} | Rol: {self.usuario.rol}')
        
        # Etiqueta central
        label = QLabel('Bienvenido al Sistema de Gestión del Taller')
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet('font-size: 24px;')
        self.setCentralWidget(label)
    
    def crear_menu(self):
        """Crea el menú principal según el rol"""
        menubar = self.menuBar()
        
        # Menú Archivo
        archivo_menu = menubar.addMenu('Archivo')
        
        if self.usuario.rol in ['jefe', 'oficina']:
            clientes_action = QAction('Clientes', self)
            clientes_action.triggered.connect(self.abrir_clientes)
            archivo_menu.addAction(clientes_action)
            
            vehiculos_action = QAction('Vehículos', self)
            vehiculos_action.triggered.connect(self.abrir_vehiculos)
            archivo_menu.addAction(vehiculos_action)
        
        ordenes_action = QAction('Órdenes de Reparación', self)
        ordenes_action.triggered.connect(self.abrir_ordenes)
        archivo_menu.addAction(ordenes_action)
        
        if self.usuario.rol in ['jefe', 'oficina']:
            facturas_action = QAction('Facturas', self)
            facturas_action.triggered.connect(self.abrir_facturas)
            archivo_menu.addAction(facturas_action)
        
        archivo_menu.addSeparator()
        
        salir_action = QAction('Salir', self)
        salir_action.triggered.connect(self.close)
        archivo_menu.addAction(salir_action)
        
        # Menú Configuración (solo jefe)
        if self.usuario.rol == 'jefe':
            config_menu = menubar.addMenu('Configuración')
            
            personalizar_action = QAction('Personalizar Interfaz', self)
            personalizar_action.triggered.connect(self.abrir_config)
            config_menu.addAction(personalizar_action)
        
        # Menú Ayuda
        ayuda_menu = menubar.addMenu('Ayuda')
        
        acerca_action = QAction('Acerca de', self)
        acerca_action.triggered.connect(self.mostrar_acerca)
        ayuda_menu.addAction(acerca_action)
    
    def abrir_clientes(self):
        """Abre ventana de clientes"""
        self.clientes_window = ClientesWindow()
        self.clientes_window.show()
    
    def abrir_vehiculos(self):
        """Abre ventana de vehículos"""
        self.vehiculos_window = VehiculosWindow()
        self.vehiculos_window.show()
    
    def abrir_ordenes(self):
        """Abre ventana de órdenes"""
        self.ordenes_window = OrdenesWindow(self.usuario)
        self.ordenes_window.show()
    
    def abrir_facturas(self):
        """Abre ventana de facturas"""
        self.facturas_window = FacturasWindow()
        self.facturas_window.show()
    
    def abrir_config(self):
        """Abre ventana de configuración"""
        self.config_window = ConfigWindow()
        self.config_window.show()
    
    def mostrar_acerca(self):
        """Muestra información de la aplicación"""
        QMessageBox.information(
            self,
            'Acerca de',
            f'{config.APP_NAME}\n'
            f'Versión: {config.APP_VERSION}\n\n'
            'Sistema de gestión profesional para talleres mecánicos'
        )
