"""
Ventana de Gestión de Clientes
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTableWidget,
                              QTableWidgetItem, QPushButton, QLineEdit, QLabel,
                              QMessageBox, QHeaderView)
from database import Session, Cliente

class ClientesWindow(QDialog):
    """Ventana de gestión de clientes"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.cargar_clientes()
    
    def init_ui(self):
        """Inicializa la interfaz"""
        self.setWindowTitle('Gestión de Clientes')
        self.setGeometry(150, 150, 900, 600)
        
        layout = QVBoxLayout()
        
        # Barra de búsqueda
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel('Buscar:'))
        self.input_buscar = QLineEdit()
        self.input_buscar.setPlaceholderText('Nombre, DNI, teléfono...')
        self.input_buscar.textChanged.connect(self.buscar_clientes)
        search_layout.addWidget(self.input_buscar)
        
        btn_nuevo = QPushButton('Nuevo Cliente')
        btn_nuevo.clicked.connect(self.nuevo_cliente)
        search_layout.addWidget(btn_nuevo)
        
        layout.addLayout(search_layout)
        
        # Tabla de clientes
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels(['ID', 'Nombre/Razón Social', 'DNI/NIF', 
                                               'Teléfono', 'Email', 'Dirección'])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.tabla)
        
        # Botones de acción
        btn_layout = QHBoxLayout()
        
        btn_editar = QPushButton('Editar')
        btn_editar.clicked.connect(self.editar_cliente)
        btn_layout.addWidget(btn_editar)
        
        btn_eliminar = QPushButton('Eliminar')
        btn_eliminar.clicked.connect(self.eliminar_cliente)
        btn_layout.addWidget(btn_eliminar)
        
        btn_cerrar = QPushButton('Cerrar')
        btn_cerrar.clicked.connect(self.close)
        btn_layout.addWidget(btn_cerrar)
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def cargar_clientes(self):
        """Carga todos los clientes en la tabla"""
        session = Session()
        try:
            clientes = session.query(Cliente).all()
            self.tabla.setRowCount(len(clientes))
            
            for row, cliente in enumerate(clientes):
                self.tabla.setItem(row, 0, QTableWidgetItem(str(cliente.id)))
                self.tabla.setItem(row, 1, QTableWidgetItem(cliente.nombre_razon_social))
                self.tabla.setItem(row, 2, QTableWidgetItem(cliente.dni_nif or ''))
                self.tabla.setItem(row, 3, QTableWidgetItem(cliente.telefono or ''))
                self.tabla.setItem(row, 4, QTableWidgetItem(cliente.email or ''))
                self.tabla.setItem(row, 5, QTableWidgetItem(cliente.direccion or ''))
        finally:
            session.close()
    
    def buscar_clientes(self, texto):
        """Busca clientes por texto"""
        session = Session()
        try:
            clientes = session.query(Cliente).filter(
                Cliente.nombre_razon_social.ilike(f'%{texto}%') |
                Cliente.dni_nif.ilike(f'%{texto}%') |
                Cliente.telefono.ilike(f'%{texto}%')
            ).all()
            
            self.tabla.setRowCount(len(clientes))
            for row, cliente in enumerate(clientes):
                self.tabla.setItem(row, 0, QTableWidgetItem(str(cliente.id)))
                self.tabla.setItem(row, 1, QTableWidgetItem(cliente.nombre_razon_social))
                self.tabla.setItem(row, 2, QTableWidgetItem(cliente.dni_nif or ''))
                self.tabla.setItem(row, 3, QTableWidgetItem(cliente.telefono or ''))
                self.tabla.setItem(row, 4, QTableWidgetItem(cliente.email or ''))
                self.tabla.setItem(row, 5, QTableWidgetItem(cliente.direccion or ''))
        finally:
            session.close()
    
    def nuevo_cliente(self):
        """Crea un nuevo cliente"""
        QMessageBox.information(self, 'Info', 'Función en desarrollo')
    
    def editar_cliente(self):
        """Edita cliente seleccionado"""
        QMessageBox.information(self, 'Info', 'Función en desarrollo')
    
    def eliminar_cliente(self):
        """Elimina cliente seleccionado"""
        QMessageBox.information(self, 'Info', 'Función en desarrollo')
