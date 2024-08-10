# @autor: Juan Velásquez
# @fecha: 2023/11/17
# @descripción: Módulo para modificar autores

# Importar módulos de PyQt5
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QDate
from PyQt5.uic import loadUi

# Importar módulos propios de la aplicación
from modules.conection import libreria # Base de datos
from modules.comboBox import estados


class DlgModificarAutor(QDialog):
    def __init__(self, datosPedido):
        super(DlgModificarAutor, self).__init__()
        loadUi('./UIs/Autores/modificarAutor.ui', self)
        self.idAutor = datosPedido.get('id_autor', None)

        self.datosOriginales = {}
        self.obtenerDatosOriginales()

        # Conectar los cambios de los inputs a la función que habilita el botón de actualizar
        self.txtNombres.textChanged.connect(self.habilitarActualizar)
        self.txtApellidos.textChanged.connect(self.habilitarActualizar)
        self.cbEstado.addItems(estados)
        self.cbEstado.currentTextChanged.connect(self.habilitarActualizar)

        # Botones
        self.btnActualizar.clicked.connect(self.actualizar)
        self.btnCancelar.clicked.connect(self.cancelar)

        self.habilitarActualizar()


    def obtenerDatosOriginales(self):
        self.datosOriginales['nombres'] = self.txtNombres.text()
        self.datosOriginales['apellidos'] = self.txtApellidos.text()
        self.datosOriginales['estado'] = self.cbEstado.currentText()


    def camposModificados(self):
        for campo, valor in self.datosOriginales.items():
            if campo == 'estado':
                if self.cbEstado.currentText() != valor:
                    return True
            elif campo in ['nombres', 'apellidos'] and getattr(self, f"txt{campo.capitalize()}").text() != valor:
                return True
        return False


    def habilitarActualizar(self):
        self.btnActualizar.setEnabled(self.camposModificados())  # Habilitar el botón de actualizar si hay cambios



    def cargarDatosAutor(self, datosPedido):
        self.txtidAutor.setText(datosPedido.get('id_autor', ''))
        self.txtNombres.setText(datosPedido.get('nombres', ''))
        self.txtApellidos.setText(datosPedido.get('apellidos', ''))
        self.cbEstado.setCurrentText(datosPedido.get('estado', ''))


    def actualizar(self):
        nombres = self.txtNombres.text()
        apellidos = self.txtApellidos.text()
        estado = self.cbEstado.currentText()

        if not (nombres and apellidos):
            self.lblWarning.setText("Por favor rellene todos los campos")
            return

        try:
            cursor = libreria.cursor()
            st = (
                "UPDATE autores SET nombres = %s, apellidos = %s, estado = %s WHERE id_autor = %s"
            )

            cursor.execute(st, (nombres, apellidos, estado, self.idAutor))
            libreria.commit()
            self.close()

        except Exception as e:
            self.lblWarning.setText(f"Error al modificar los datos del autor: {e}")


    def cancelar(self):
        self.close()