# @autor: Juan Velásquez
# @fecha: 2023/11/17
# @descripción: Módulo para modificar los datos del cliente

# Importar módulos de PyQt5
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

# Importar módulos propios de la aplicación
from modules.conection import libreria # Base de datos
from modules.comboBox import estados


class DlgModificarClientes(QDialog):
    def __init__(self, datosCliente):
        super(DlgModificarClientes, self).__init__()
        loadUi('./UIs/Clientes/modificarCliente.ui', self)
        self.idCliente = datosCliente.get('id_cliente', None)

        # Conectar los cambios de los inputs a la función que habilita el botón de actualizar
        self.txtIdentificacion.textChanged.connect(self.habilitarActualizar)
        self.txtNombres.textChanged.connect(self.habilitarActualizar)
        self.txtApellidos.textChanged.connect(self.habilitarActualizar)
        self.txtTelefono.textChanged.connect(self.habilitarActualizar)
        self.txtDireccion.textChanged.connect(self.habilitarActualizar)
        self.txtCorreo.textChanged.connect(self.habilitarActualizar)
        self.cbEstado.currentTextChanged.connect(self.habilitarActualizar)

        # Botones
        self.btnActualizar.clicked.connect(self.actualizar)
        self.btnCancelar.clicked.connect(self.cancelar)

        # Variables para almacenar los datos originales del Cliente
        self.datosOriginales = {}
        self.obtenerDatosOriginales()


    def obtenerDatosOriginales(self):
        self.datosOriginales['identificacion'] = self.txtIdentificacion.text()
        self.datosOriginales['nombres'] = self.txtNombres.text()
        self.datosOriginales['apellidos'] = self.txtApellidos.text()
        self.datosOriginales['telefono'] = self.txtTelefono.text()
        self.datosOriginales['direccion'] = self.txtDireccion.text()
        self.datosOriginales['correo_electronico'] = self.txtCorreo.text()
        self.datosOriginales['estado'] = self.cbEstado.currentText()


    def camposModificados(self):
        for campo, valor in self.datosOriginales.items():
            if campo == 'estado':
                if self.cbEstado.currentText() != valor:
                    return True
            elif hasattr(self, f"txt{campo.capitalize()}") and getattr(self, f"txt{campo.capitalize()}").text() != valor:
                if campo != 'correo_electronico':
                    return True
        return False


    def habilitarActualizar(self):
        self.btnActualizar.setEnabled(self.camposModificados())  # Habilitar el botón de actualizar si hay cambios


    def cargarDatosCliente(self, datosCliente):
        self.txtidCliente.setText(datosCliente.get('id_cliente', ''))
        self.txtIdentificacion.setText(datosCliente.get('identificacion', ''))
        self.txtNombres.setText(datosCliente.get('nombres', ''))
        self.txtApellidos.setText(datosCliente.get('apellidos', ''))
        self.txtTelefono.setText(datosCliente.get('telefono', ''))
        self.txtDireccion.setText(datosCliente.get('direccion', ''))
        self.txtCorreo.setText(datosCliente.get('correo_electronico', ''))
        self.cbEstado.addItems(estados)
        self.cbEstado.setCurrentText(datosCliente.get('estado', ''))


    def actualizar(self):
        identificacion = self.txtIdentificacion.text()
        nombres = self.txtNombres.text()
        apellidos = self.txtApellidos.text()
        telefono = self.txtTelefono.text()
        direccion = self.txtDireccion.text()
        correo = self.txtCorreo.text()
        estado = self.cbEstado.currentText()

        if not (identificacion and nombres and apellidos and telefono and direccion and correo):
            self.lblWarning.setText("Por favor rellene todos los campos")
            return

        try:
            cursor = libreria.cursor()
            st = ("UPDATE clientes SET identificacion = %s, nombres = %s, apellidos = %s, telefono = %s, direccion = %s, correo_electronico = %s, estado = %s WHERE id_cliente = %s")

            cursor.execute(st, (identificacion, nombres, apellidos, telefono, direccion, correo, estado, self.idCliente))
            libreria.commit()
            self.close()

        except Exception as e:
            self.lblWarning.setText(f"Error al modificar el cliente: {e}")


    def cancelar(self):
        self.close()