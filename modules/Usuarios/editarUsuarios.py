# @autor: Juan Velásquez
# @fecha: 2023/11/17
# @descripción: Módulo para modificar usuarios

# Importar módulos de PyQt5
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

# Importar módulos propios de la aplicación
from modules.conection import libreria # Base de datos


class DlgModificarUsuarios(QDialog):
    def __init__(self, datosUsuario):
        super(DlgModificarUsuarios, self).__init__()
        loadUi('./UIs/Usuarios/editarUsuarios.ui', self)
        self.idUser = datosUsuario.get('id', None)

        # Conectar los cambios de los inputs a la función que habilita el botón de actualizar
        self.txtUser.textChanged.connect(self.habilitarActualizar)
        self.txtNombre.textChanged.connect(self.habilitarActualizar)
        self.txtPass.textChanged.connect(self.habilitarActualizar)

        # Botones
        self.btnModificar.clicked.connect(self.modificar)
        self.btnCancelar.clicked.connect(self.cancelar)

        # Variables para almacenar los datos originales del usuario
        self.datosOriginales = {}
        self.obtenerDatosOriginales()


    def obtenerDatosOriginales(self):
        self.datosOriginales['usuario'] = self.txtUser.text()
        self.datosOriginales['nombre'] = self.txtNombre.text()
        self.datosOriginales['clave'] = self.txtPass.text()


    def camposModificados(self):
        for campo, valor in self.datosOriginales.items():
            attr_name = f"txt{campo.capitalize()}"
            if hasattr(self, attr_name) and getattr(self, attr_name).text() != valor:
                return True
        return False


    def habilitarActualizar(self):
        self.btnModificar.setEnabled(self.camposModificados())  # Habilitar el botón de actualizar si hay cambios


    def cargarDatosUsuario(self, datosUsuario):
        self.txtUser.setText(datosUsuario.get('usuario', ''))
        self.txtNombre.setText(datosUsuario.get('nombre', ''))
        self.txtPass.setText(datosUsuario.get('clave', ''))


    def modificar(self):
        usuario = self.txtUser.text()
        nombre = self.txtNombre.text()
        clave = self.txtPass.text()

        if self.idUser:  # Verificar que hay un ID de usuario válido
            cursor = libreria.cursor()

            # Consulta para actualizar los datos del usuario
            st = f"UPDATE usuarios SET "

            updates = []
            if usuario:
                updates.append(f"usuario = '{usuario}'")
            if nombre:
                updates.append(f"nombre = '{nombre}'")
            if clave:
                updates.append(f"clave = '{clave}'")

            st += ", ".join(updates)
            st += f" WHERE id = {self.idUser}"

            cursor.execute(st)
            libreria.commit()
            self.close()
        else:
            self.lblWarning.setText("ID de usuario inválido")


    def cancelar(self):
        self.close()