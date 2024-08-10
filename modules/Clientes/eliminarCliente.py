# @autor: Juan Velásquez
# @fecha: 2023/11/17
# @descripción: Módulo para eliminar clientes

# Importar módulos de PyQt5
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi


class DlgEliminarClientes(QDialog):
    def __init__(self):
        super(DlgEliminarClientes, self).__init__()
        loadUi('./UIs/Clientes/eliminarCliente.ui', self)
        self.id_cliente = None

        # Botones
        self.btnConfirmar.clicked.connect(self.confirmar)
        self.btnCancelar.clicked.connect(self.cancelar)


    def cargarDatosCliente(self, datosCliente):
        self.lblEliminar.setText(f"Eliminar cliente {datosCliente.get('cliente', '')}")
        self.id_cliente = datosCliente.get('id_cliente', None)


    def confirmar(self):
        self.accept()

    def cancelar(self):
        self.reject()

    def getID(self):
        return self.id_cliente