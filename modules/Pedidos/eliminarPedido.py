# @autor: Juan Velásquez
# @fecha: 2023/11/17
# @descripción: Módulo para eliminar pedidos

# Importar módulos de PyQt5
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi


class DlgEliminarPedido(QDialog):
    def __init__(self):
        super(DlgEliminarPedido, self).__init__()
        loadUi('./UIs/Pedidos/eliminarPedido.ui', self)
        self.id_pedido = None

        # Botones
        self.btnConfirmar.clicked.connect(self.confirmar)
        self.btnCancelar.clicked.connect(self.cancelar)


    def cargarDatosPedido(self, datosPedido):
        self.lblEliminar.setText(f"Eliminar pedido {datosPedido.get('nro_pedido', '')}")
        self.id_pedido = datosPedido.get('id_pedido', None)


    def confirmar(self):
        self.accept()

    def cancelar(self):
        self.reject()

    def getID(self):
        return self.id_pedido