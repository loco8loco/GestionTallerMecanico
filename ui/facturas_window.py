"""
Ventana de Facturas
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTableWidget,
                              QTableWidgetItem, QPushButton, QLineEdit, QLabel,
                              QMessageBox, QHeaderView)
from database import Session, Factura

class FacturasWindow(QDialog):
    """Ventana de gestión de facturas"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.cargar_facturas()
    
    def init_ui(self):
        """Inicializa la interfaz"""
        self.setWindowTitle('Gestión de Facturas')
        self.setGeometry(150, 150, 1000, 600)
        
        layout = QVBoxLayout()
        
        # Barra de búsqueda
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel('Buscar:'))
        self.input_buscar = QLineEdit()
        self.input_buscar.setPlaceholderText('Número factura, cliente...')
        search_layout.addWidget(self.input_buscar)
        
        btn_nueva = QPushButton('Nueva Factura')
        btn_nueva.clicked.connect(self.nueva_factura)
        search_layout.addWidget(btn_nueva)
        
        layout.addLayout(search_layout)
        
        # Tabla de facturas
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(7)
        self.tabla.setHorizontalHeaderLabels(['ID', 'Nº Factura', 'Cliente', 'Fecha',
                                               'Base', 'IVA', 'Total'])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.tabla)
        
        # Botones
        btn_layout = QHBoxLayout()
        
        btn_ver = QPushButton('Ver')
        btn_ver.clicked.connect(self.ver_factura)
        btn_layout.addWidget(btn_ver)
        
        btn_imprimir = QPushButton('Imprimir')
        btn_imprimir.clicked.connect(self.imprimir_factura)
        btn_layout.addWidget(btn_imprimir)
        
        btn_cerrar = QPushButton('Cerrar')
        btn_cerrar.clicked.connect(self.close)
        btn_layout.addWidget(btn_cerrar)
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def cargar_facturas(self):
        """Carga todas las facturas"""
        session = Session()
        try:
            facturas = session.query(Factura).all()
            self.tabla.setRowCount(len(facturas))
            
            for row, factura in enumerate(facturas):
                self.tabla.setItem(row, 0, QTableWidgetItem(str(factura.id)))
                self.tabla.setItem(row, 1, QTableWidgetItem(factura.numero_factura or ''))
                self.tabla.setItem(row, 2, QTableWidgetItem(factura.cliente.nombre_razon_social if factura.cliente else ''))
                self.tabla.setItem(row, 3, QTableWidgetItem(factura.fecha_emision.strftime('%d/%m/%Y') if factura.fecha_emision else ''))
                self.tabla.setItem(row, 4, QTableWidgetItem(f'€{factura.base_imponible:.2f}'))
                self.tabla.setItem(row, 5, QTableWidgetItem(f'€{factura.iva:.2f}'))
                self.tabla.setItem(row, 6, QTableWidgetItem(f'€{factura.total:.2f}'))
        finally:
            session.close()
    
    def nueva_factura(self):
        """Crea nueva factura"""
        QMessageBox.information(self, 'Info', 'Función en desarrollo')
    
    def ver_factura(self):
        """Ve detalles de factura"""
        QMessageBox.information(self, 'Info', 'Función en desarrollo')
    
    def imprimir_factura(self):
        """Imprime factura"""
        QMessageBox.information(self, 'Info', 'Función en desarrollo')
