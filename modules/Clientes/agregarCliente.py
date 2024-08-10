# @autor: Juan Velásquez
# @fecha: 2023/11/17
# @descripción: Módulo para crear clientes

# Importar módulos de PyQt5
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

# Importar módulos propios de la aplicación
from modules.conection import libreria # Base de datos
from modules.comboBox import estados


class DlgAgregarClientes(QDialog):
    def __init__(self):
        super(DlgAgregarClientes, self).__init__()
        loadUi('./UIs/Clientes/agregarCliente.ui', self)

        # Conectar señales a la función de validación
        self.txtIdentificacion.textChanged.connect(self.validarCampos)
        self.txtNombres.textChanged.connect(self.validarCampos)
        self.txtApellidos.textChanged.connect(self.validarCampos)
        self.txtTelefono.textChanged.connect(self.validarCampos)
        self.txtDireccion.textChanged.connect(self.validarCampos)
        self.txtCorreo.textChanged.connect(self.validarCampos)
        self.cbEstado.addItems(estados)
        self.cbEstado.currentTextChanged.connect(self.validarCampos)

        self.validarCampos()  # Llamada inicial para deshabilitar el botón al inicio

        # Botones
        self.btnAgregar.clicked.connect(self.agregar)
        self.btnCancelar.clicked.connect(self.cancelar)

    def validarCampos(self):
        identificacion = self.txtIdentificacion.text()
        nombres = self.txtNombres.text()
        apellidos = self.txtApellidos.text()
        telefono = self.txtTelefono.text()
        direccion = self.txtDireccion.text()
        correo = self.txtCorreo.text()
        estado = self.cbEstado.currentText()

        # Verificar si algún campo está vacío
        camposVacios = [campo for campo in [identificacion, nombres, apellidos, telefono, direccion, correo, estado] if not campo]

        # Si hay campos vacíos, deshabilitar el botón y mostrar un mensaje
        if camposVacios:
            self.btnAgregar.setEnabled(False)
        else:
            self.btnAgregar.setEnabled(True)

    def agregar(self):
        identificacion = self.txtIdentificacion.text()
        nombres = self.txtNombres.text()
        apellidos = self.txtApellidos.text()
        telefono = self.txtTelefono.text()
        direccion = self.txtDireccion.text()
        correo = self.txtCorreo.text()
        estado = self.cbEstado.currentText()

        try:
            cursor = libreria.cursor()
            st = (
                f"INSERT INTO clientes (identificacion, nombres, apellidos, telefono, direccion, correo_electronico, estado) "
                f"VALUES ('{identificacion}', '{nombres}', '{apellidos}', '{telefono}', '{direccion}', '{correo}', '{estado}')"
            )
            cursor.execute(st)
            libreria.commit()
            self.close()
        except Exception as e:
            print(f"Error al agregar el cliente: {e}")

    def cancelar(self):
        self.close()  # Cerrar solo la ventana actual