# @autor: Juan Velásquez
# @fecha: 2023/11/17
# @descripción: Módulo para eliminar usuarios

# Importar módulos de PyQt5
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi


class DlgEliminarUsuario(QDialog):
    def __init__(self):
        super(DlgEliminarUsuario, self).__init__()
        loadUi('./UIs/Usuarios/eliminarUsuarios.ui', self)
        self.id = None

        # Botones
        self.btnConfirmar.clicked.connect(self.confirmar)
        self.btnCancelar.clicked.connect(self.cancelar)


    def cargarDatosUsuario(self, datosUsuario):
        self.lblEliminar.setText(f"Eliminar usuario {datosUsuario.get('usuario', '')}")
        self.id = datosUsuario.get('id', None)


    def confirmar(self):
        self.accept()

    def cancelar(self):
        self.reject()

    def getID(self):
        return self.id