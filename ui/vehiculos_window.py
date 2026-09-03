"""
Ventana de Gestión de Vehículos
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTableWidget,
                              QTableWidgetItem, QPushButton, QLineEdit, QLabel,
                              QMessageBox, QHeaderView)
from database import Session, Vehiculo

class VehiculosWindow(QDialog):
    """Ventana de gestión de vehículos"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.cargar_vehiculos()
    
    def init_ui(self):
        """Inicializa la interfaz"""
        self.setWindowTitle('Gestión de Vehículos')
        self.setGeometry(150, 150, 900, 600)
        
        layout = QVBoxLayout()
        
        # Barra de búsqueda
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel('Buscar:'))
        self.input_buscar = QLineEdit()
        self.input_buscar.setPlaceholderText('Matricula, marca, modelo...')
        self.input_buscar.textChanged.connect(self.buscar_vehiculos)
        search_layout.addWidget(self.input_buscar)
        
        btn_nuevo = QPushButton('Nuevo Vehículo')
        btn_nuevo.clicked.connect(self.nuevo_vehiculo)
        search_layout.addWidget(btn_nuevo)
        
        layout.addLayout(search_layout)
        
        # Tabla de vehículos
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels(['ID', 'Matrícula', 'Marca', 
                                               'Modelo', 'Bastidor', 'KM'])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.tabla)
        
        # Botones
        btn_layout = QHBoxLayout()
        
        btn_editar = QPushButton('Editar')
        btn_editar.clicked.connect(self.editar_vehiculo)
        btn_layout.addWidget(btn_editar)
        
        btn_eliminar = QPushButton('Eliminar')
        btn_eliminar.clicked.connect(self.eliminar_vehiculo)
        btn_layout.addWidget(btn_eliminar)
        
        btn_cerrar = QPushButton('Cerrar')
        btn_cerrar.clicked.connect(self.close)
        btn_layout.addWidget(btn_cerrar)
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def cargar_vehiculos(self):
        """Carga todos los vehículos"""
        session = Session()
        try:
            vehiculos = session.query(Vehiculo).all()
            self.tabla.setRowCount(len(vehiculos))
            
            for row, vehiculo in enumerate(vehiculos):
                self.tabla.setItem(row, 0, QTableWidgetItem(str(vehiculo.id)))
                self.tabla.setItem(row, 1, QTableWidgetItem(vehiculo.matricula))
                self.tabla.setItem(row, 2, QTableWidgetItem(vehiculo.marca or ''))
                self.tabla.setItem(row, 3, QTableWidgetItem(vehiculo.modelo or ''))
                self.tabla.setItem(row, 4, QTableWidgetItem(vehiculo.bastidor or ''))
                self.tabla.setItem(row, 5, QTableWidgetItem(str(vehiculo.km_actual)))
        finally:
            session.close()
    
    def buscar_vehiculos(self, texto):
        """Busca vehículos"""
        session = Session()
        try:
            vehiculos = session.query(Vehiculo).filter(
                Vehiculo.matricula.ilike(f'%{texto}%') |
                Vehiculo.marca.ilike(f'%{texto}%') |
                Vehiculo.modelo.ilike(f'%{texto}%')
            ).all()
            
            self.tabla.setRowCount(len(vehiculos))
            for row, vehiculo in enumerate(vehiculos):
                self.tabla.setItem(row, 0, QTableWidgetItem(str(vehiculo.id)))
                self.tabla.setItem(row, 1, QTableWidgetItem(vehiculo.matricula))
                self.tabla.setItem(row, 2, QTableWidgetItem(vehiculo.marca or ''))
                self.tabla.setItem(row, 3, QTableWidgetItem(vehiculo.modelo or ''))
                self.tabla.setItem(row, 4, QTableWidgetItem(vehiculo.bastidor or ''))
                self.tabla.setItem(row, 5, QTableWidgetItem(str(vehiculo.km_actual)))
        finally:
            session.close()
    
    def nuevo_vehiculo(self):
        """Crea nuevo vehículo"""
        QMessageBox.information(self, 'Info', 'Función en desarrollo')
    
    def editar_vehiculo(self):
        """Edita vehículo"""
        QMessageBox.information(self, 'Info', 'Función en desarrollo')
    
    def eliminar_vehiculo(self):
        """Elimina vehículo"""
        QMessageBox.information(self, 'Info', 'Función en desarrollo')
