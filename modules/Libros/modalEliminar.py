# @autor: Juan Velásquez
# @fecha: 2023/11/17
# @descripción: Módulo eliminar libros

# Importar módulos de PyQt5
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi


class DlgEliminar(QDialog):
    def __init__(self):
        super(DlgEliminar, self).__init__()
        loadUi('./UIs/Libros/modalEliminar.ui', self)
        self.isbn = None # Atributo para almacenar el ISBN

        # Botones
        self.btnConfirmar.clicked.connect(self.confirmar)
        self.btnCancelar.clicked.connect(self.cancelar)


    def cargarDatosLibro(self, datosLibro):
        self.lblEliminar.setText(f"Eliminar libro {datosLibro.get('titulo', '')}")  # Mostrar el nombre del libro en el label
        self.isbn = datosLibro.get('isbn', None)  # Almacena el ISBN del libro en el atributo


    def confirmar(self):
        self.accept()  # Acepta el diálogo para indicar que se ha confirmado la eliminación

    def cancelar(self):
        self.reject()  # Rechaza el diálogo para indicar que se ha cancelado la eliminación

    def getISBN(self):
        return self.isbn  # Retorna el ISBN almacenado