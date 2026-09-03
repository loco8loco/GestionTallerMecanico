"""
Ventana de Configuración (Solo Jefe)
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                              QLineEdit, QPushButton, QMessageBox, QFileDialog,
                              QGroupBox)
from database import Session, Configuracion

class ConfigWindow(QDialog):
    """Ventana de configuración de la aplicación"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.cargar_configuracion()
    
    def init_ui(self):
        """Inicializa la interfaz"""
        self.setWindowTitle('Configuración de la Aplicación')
        self.setFixedSize(600, 500)
        
        layout = QVBoxLayout()
        
        # Grupo: Información General
        grupo_general = QGroupBox('Información General')
        general_layout = QVBoxLayout()
        
        general_layout.addWidget(QLabel('Título de la Aplicación:'))
        self.input_titulo = QLineEdit()
        general_layout.addWidget(self.input_titulo)
        
        grupo_general.setLayout(general_layout)
        layout.addWidget(grupo_general)
        
        # Grupo: Apariencia
        grupo_apariencia = QGroupBox('Apariencia')
        apariencia_layout = QVBoxLayout()
        
        # Fondo de pantalla
        fondo_layout = QHBoxLayout()
        fondo_layout.addWidget(QLabel('Fondo de Pantalla:'))
        self.input_fondo = QLineEdit()
        self.input_fondo.setReadOnly(True)
        fondo_layout.addWidget(self.input_fondo)
        btn_fondo = QPushButton('Seleccionar...')
        btn_fondo.clicked.connect(self.seleccionar_fondo)
        fondo_layout.addWidget(btn_fondo)
        apariencia_layout.addLayout(fondo_layout)
        
        # Icono
        icono_layout = QHBoxLayout()
        icono_layout.addWidget(QLabel('Icono de la Aplicación:'))
        self.input_icono = QLineEdit()
        self.input_icono.setReadOnly(True)
        icono_layout.addWidget(self.input_icono)
        btn_icono = QPushButton('Seleccionar...')
        btn_icono.clicked.connect(self.seleccionar_icono)
        icono_layout.addWidget(btn_icono)
        apariencia_layout.addLayout(icono_layout)
        
        grupo_apariencia.setLayout(apariencia_layout)
        layout.addWidget(grupo_apariencia)
        
        # Botones
        btn_layout = QHBoxLayout()
        
        btn_guardar = QPushButton('Guardar Cambios')
        btn_guardar.clicked.connect(self.guardar_configuracion)
        btn_layout.addWidget(btn_guardar)
        
        btn_cerrar = QPushButton('Cerrar')
        btn_cerrar.clicked.connect(self.close)
        btn_layout.addWidget(btn_cerrar)
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def cargar_configuracion(self):
        """Carga la configuración actual"""
        session = Session()
        try:
            configs = session.query(Configuracion).all()
            for config in configs:
                if config.clave == 'titulo_app':
                    self.input_titulo.setText(config.valor or '')
                elif config.clave == 'fondo_pantalla':
                    self.input_fondo.setText(config.valor or 'No establecido')
                elif config.clave == 'icono_app':
                    self.input_icono.setText(config.valor or 'No establecido')
        finally:
            session.close()
    
    def seleccionar_fondo(self):
        """Selecciona imagen de fondo"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            'Seleccionar Fondo de Pantalla',
            '',
            'Imágenes (*.png *.jpg *.jpeg)'
        )
        if filename:
            self.input_fondo.setText(filename)
    
    def seleccionar_icono(self):
        """Selecciona icono"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            'Seleccionar Icono',
            '',
            'Imágenes (*.png *.ico)'
        )
        if filename:
            self.input_icono.setText(filename)
    
    def guardar_configuracion(self):
        """Guarda la configuración"""
        session = Session()
        try:
            # Guardar título
            config_titulo = session.query(Configuracion).filter_by(clave='titulo_app').first()
            if config_titulo:
                config_titulo.valor = self.input_titulo.text()
            
            # Guardar fondo
            config_fondo = session.query(Configuracion).filter_by(clave='fondo_pantalla').first()
            if config_fondo and self.input_fondo.text() != 'No establecido':
                config_fondo.valor = self.input_fondo.text()
            
            # Guardar icono
            config_icono = session.query(Configuracion).filter_by(clave='icono_app').first()
            if config_icono and self.input_icono.text() != 'No establecido':
                config_icono.valor = self.input_icono.text()
            
            session.commit()
            QMessageBox.information(self, 'Éxito', 'Configuración guardada correctamente')
            
        except Exception as e:
            session.rollback()
            QMessageBox.critical(self, 'Error', f'Error al guardar: {e}')
        finally:
            session.close()
