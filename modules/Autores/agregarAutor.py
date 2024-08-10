# @autor: Juan Velásquez
# @fecha: 2023/11/17
# @descripción: Módulo para agregar autores

# Importar módulos de PyQt5
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QDate
from PyQt5.uic import loadUi

# Importar módulos propios de la aplicación
from modules.conection import libreria # Base de datos
from modules.comboBox import estados


class DlgAgregarAutor(QDialog):
    def __init__(self):
        super(DlgAgregarAutor, self).__init__()
        loadUi('./UIs/Autores/agregarAutor.ui', self)

        # Conectar señales a la función de validación
        self.txtNombres.textChanged.connect(self.validarCampos)
        self.txtApellidos.textChanged.connect(self.validarCampos)
        self.cbEstado.addItems(estados)
        self.cbEstado.currentTextChanged.connect(self.validarCampos)

        self.validarCampos()  # Llamada inicial para deshabilitar el botón al inicio

        # Botones
        self.btnAgregar.clicked.connect(self.agregar)
        self.btnCancelar.clicked.connect(self.cancelar)


    def validarCampos(self):        
        nombres = self.txtNombres.text()
        apellidos = self.txtApellidos.text()

        # Verifica si algún campo está vacío
        camposVacios = [campo for campo in [nombres, apellidos] if not campo]

        # Si hay campos vacíos, deshabilitar el botón y mostrar un mensaje
        if camposVacios:
            self.btnAgregar.setEnabled(False)
        else:
            self.btnAgregar.setEnabled(True)


    def agregar(self):
        nombres = self.txtNombres.text()
        apellidos = self.txtApellidos.text()
        estado = self.cbEstado.currentText()

        try:
            cursor = libreria.cursor()
            st = (f"INSERT INTO autores (nombres, apellidos, estado) VALUES ('{nombres}', '{apellidos}', '{estado}')")
            cursor.execute(st)
            libreria.commit()
            self.close()

        except Exception as e:
            self.lblWarning.setText(f"Error al agregar autor: {e}")


    def cancelar(self):
        self.close()