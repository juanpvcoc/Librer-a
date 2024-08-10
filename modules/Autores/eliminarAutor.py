# @autor: Juan Velásquez
# @fecha: 2023/11/17
# @descripción: Módulo para eliminar autores

# Importar módulos de PyQt5
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi


class DlgEliminarAutor(QDialog):
    def __init__(self):
        super(DlgEliminarAutor, self).__init__()
        loadUi('./UIs/Autores/eliminarAutor.ui', self)
        self.idAutor = None

        # Botones
        self.btnConfirmar.clicked.connect(self.confirmar)
        self.btnCancelar.clicked.connect(self.cancelar)


    def cargarDatosAutor(self, datosAutor):
        self.lblEliminar.setText(f"Eliminar autor: {datosAutor.get('nombres', '')} {datosAutor.get('apellidos', '')}")
        self.idAutor = datosAutor.get('id_autor', None)


    def confirmar(self):
        self.accept()

    def cancelar(self):
        self.reject()

    def getID(self):
        return self.idAutor