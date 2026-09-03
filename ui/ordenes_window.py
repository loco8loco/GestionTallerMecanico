"""
Ventana de Órdenes de Reparación
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTableWidget,
                              QTableWidgetItem, QPushButton, QLineEdit, QLabel,
                              QMessageBox, QHeaderView, QComboBox)
from database import Session, OrdenReparacion
import config

class OrdenesWindow(QDialog):
    """Ventana de gestión de órdenes de reparación"""
    
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.init_ui()
        self.cargar_ordenes()
    
    def init_ui(self):
        """Inicializa la interfaz"""
        self.setWindowTitle('Órdenes de Reparación')
        self.setGeometry(150, 150, 1000, 700)
        
        layout = QVBoxLayout()
        
        # Filtros
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel('Estado:'))
        self.combo_estado = QComboBox()
        self.combo_estado.addItems(['Todos', 'Pendiente', 'En Proceso', 'Terminado', 'Entregado'])
        self.combo_estado.currentTextChanged.connect(self.filtrar_ordenes)
        filter_layout.addWidget(self.combo_estado)
        
        filter_layout.addWidget(QLabel('Buscar:'))
        self.input_buscar = QLineEdit()
        self.input_buscar.setPlaceholderText('Matrícula, cliente...')
        self.input_buscar.textChanged.connect(self.buscar_ordenes)
        filter_layout.addWidget(self.input_buscar)
        
        # Solo jefe y oficina pueden crear órdenes
        if self.usuario.rol in ['jefe', 'oficina']:
            btn_nueva = QPushButton('Nueva Orden')
            btn_nueva.clicked.connect(self.nueva_orden)
            filter_layout.addWidget(btn_nueva)
        
        layout.addLayout(filter_layout)
        
        # Tabla de órdenes
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(8)
        self.tabla.setHorizontalHeaderLabels(['ID', 'Vehículo', 'Cliente', 'Fecha Entrada',
                                               'Estado', 'Mecánico', 'Descripción', 'Total'])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.tabla)
        
        # Botones
        btn_layout = QHBoxLayout()
        
        btn_ver = QPushButton('Ver/Editar')
        btn_ver.clicked.connect(self.ver_orden)
        btn_layout.addWidget(btn_ver)
        
        # Mecánico solo puede cambiar estado
        if self.usuario.rol == 'mecanico':
            btn_estado = QPushButton('Cambiar Estado')
            btn_estado.clicked.connect(self.cambiar_estado)
            btn_layout.addWidget(btn_estado)
        
        btn_cerrar = QPushButton('Cerrar')
        btn_cerrar.clicked.connect(self.close)
        btn_layout.addWidget(btn_cerrar)
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def cargar_ordenes(self):
        """Carga todas las órdenes"""
        session = Session()
        try:
            ordenes = session.query(OrdenReparacion).all()
            self.mostrar_ordenes(ordenes)
        finally:
            session.close()
    
    def mostrar_ordenes(self, ordenes):
        """Muestra órdenes en la tabla"""
        self.tabla.setRowCount(len(ordenes))
        
        for row, orden in enumerate(ordenes):
            self.tabla.setItem(row, 0, QTableWidgetItem(str(orden.id)))
            self.tabla.setItem(row, 1, QTableWidgetItem(orden.vehiculo.matricula if orden.vehiculo else ''))
            self.tabla.setItem(row, 2, QTableWidgetItem(orden.vehiculo.cliente.nombre_razon_social if orden.vehiculo and orden.vehiculo.cliente else ''))
            self.tabla.setItem(row, 3, QTableWidgetItem(orden.fecha_entrada.strftime('%d/%m/%Y') if orden.fecha_entrada else ''))
            self.tabla.setItem(row, 4, QTableWidgetItem(orden.estado))
            self.tabla.setItem(row, 5, QTableWidgetItem(orden.mecanico.nombre_completo if orden.mecanico else ''))
            self.tabla.setItem(row, 6, QTableWidgetItem(orden.descripcion_averia[:50] + '...' if orden.descripcion_averia and len(orden.descripcion_averia) > 50 else (orden.descripcion_averia or '')))
            self.tabla.setItem(row, 7, QTableWidgetItem(f'€{orden.total:.2f}'))
    
    def filtrar_ordenes(self, estado):
        """Filtra órdenes por estado"""
        session = Session()
        try:
            if estado == 'Todos':
                ordenes = session.query(OrdenReparacion).all()
            else:
                estado_map = {
                    'Pendiente': config.ESTADO_PENDIENTE,
                    'En Proceso': config.ESTADO_EN_PROCESO,
                    'Terminado': config.ESTADO_TERMINADO,
                    'Entregado': config.ESTADO_ENTREGADO
                }
                ordenes = session.query(OrdenReparacion).filter_by(estado=estado_map[estado]).all()
            
            self.mostrar_ordenes(ordenes)
        finally:
            session.close()
    
    def buscar_ordenes(self, texto):
        """Busca órdenes"""
        QMessageBox.information(self, 'Info', 'Búsqueda en desarrollo')
    
    def nueva_orden(self):
        """Crea nueva orden"""
        QMessageBox.information(self, 'Info', 'Función en desarrollo')
    
    def ver_orden(self):
        """Ve detalles de orden"""
        QMessageBox.information(self, 'Info', 'Función en desarrollo')
    
    def cambiar_estado(self):
        """Cambia estado de orden (mecánico)"""
        QMessageBox.information(self, 'Info', 'Función en desarrollo')
