# @autor: Juan Velásquez
# @fecha: 2023/11/17
# @descripción: Módulo principal de los pedidos

# Importar módulos propios de Python
import datetime

# Importar módulos de PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QHeaderView
from PyQt5.uic import loadUi

# Importar módulos propios de la aplicación
from modules.conection import libreria


# Clase Principal
class DlgPedidos(QDialog):
    def __init__(self): # Constructor __init__
        super(DlgPedidos, self).__init__()
        loadUi('./UIs/Pedidos/pedidos.ui', self)

        self.tblPedidos.itemSelectionChanged.connect(self.actualizarBotones) # Conectar la señal de selección de la tabla a la función que actualiza los botones
        self.actualizarBotones() # Llamada inicial para deshabilitar los botones al inicio

        # Botones
        self.btnBuscar.clicked.connect(self.buscarPedido)
        self.btnActualizar.clicked.connect(self.cargarDatos)
        self.btnAgregar.clicked.connect(self.agregarPedido)
        self.btnModificar.clicked.connect(self.editarPedido)
        self.btnEliminar.clicked.connect(self.modalEliminar)
        self.btnSalir.clicked.connect(self.salir)

        # Columnas de la tabla
        nombreColumnas = [
            'ID',
            'N° pedido',
            'ID cliente',
            'ISBN',
            'Fecha pedido',
            'Cantidad',
            'Subtotal',
            'Estado'
        ]

        self.tblPedidos.setColumnCount(len(nombreColumnas)) # Establece el número de columnas
        self.tblPedidos.setHorizontalHeaderLabels(nombreColumnas) # Establece el nombre de las columnas

        # Adaptar columnas al ancho de la tabla
        self.tblPedidos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tblPedidos.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)

        self.cargarDatos()


    # Carga de datos en la tabla
    def cargarDatos(self):
        cursor = libreria.cursor()
        st = (f"SELECT id_pedido, nro_pedido, id_cliente, isbn, fecha_pedido, cantidad, subtotal, estado FROM tbl_pedido_cliente")
        cursor.execute(st)
        filas = cursor.fetchall()

        numFilas = len(filas)
        self.tblPedidos.setRowCount(numFilas)
        f = 0

        if filas:
            for fila in filas:
                self.tblPedidos.setItem(f, 0, QtWidgets.QTableWidgetItem(str(fila[0])))
                self.tblPedidos.setItem(f, 1, QtWidgets.QTableWidgetItem(str(fila[1])))
                self.tblPedidos.setItem(f, 2, QtWidgets.QTableWidgetItem(str(fila[2])))
                self.tblPedidos.setItem(f, 3, QtWidgets.QTableWidgetItem(str(fila[3])))
                self.tblPedidos.setItem(f, 4, QtWidgets.QTableWidgetItem(str(fila[4])))
                self.tblPedidos.setItem(f, 5, QtWidgets.QTableWidgetItem(str(fila[5])))
                self.tblPedidos.setItem(f, 6, QtWidgets.QTableWidgetItem(str(fila[6])))
                self.tblPedidos.setItem(f, 7, QtWidgets.QTableWidgetItem(str(fila[7])))
                f += 1

        # self.tblPedidos.resizeColumnToContents(0)
        # self.tblPedidos.resizeColumnToContents(1)
        # self.tblPedidos.resizeColumnToContents(2)
        # self.tblPedidos.resizeColumnToContents(3)
        # self.tblPedidos.resizeColumnToContents(4)
        # self.tblPedidos.resizeColumnToContents(5)
        # self.tblPedidos.resizeColumnToContents(6)
        # self.tblPedidos.resizeColumnToContents(7)


    def actualizarBotones(self):
        # Obtener la cantidad de elementos seleccionados
        itemSeleccionado = self.tblPedidos.selectedItems()
        habilitarBoton = len(itemSeleccionado) > 0

        # Habilitar/deshabilitar los botones de editar y eliminar cuando se selecciona una fila
        self.btnModificar.setEnabled(habilitarBoton)
        self.btnEliminar.setEnabled(habilitarBoton)


    def buscarPedido(self):
        buscar = self.txtBusqueda.text().lower()

        cursor = libreria.cursor()
        st = """SELECT * FROM tbl_pedido_cliente WHERE LOWER(nro_pedido) LIKE %s """
        params = ('%' + buscar + '%',)

        cursor.execute(st, params)
        filas = cursor.fetchall()
        self.tblPedidos.setRowCount(0)  # Limpiar la tabla

        if filas:
            posicionFila = 0
            self.tblPedidos.setRowCount(len(filas))  # Establecer el número de filas según los resultados de la búsqueda
            for fila in filas:
                posicionColumna = 0
                for col in fila:
                    if isinstance(col, datetime.date):
                        col = col.strftime('%Y-%m-%d')
                    elif posicionColumna == 3 and not col:  # Verificar la categoría
                        col = 'Sin categoría'
                    else:
                        col = str(col) if col else ''

                    self.tblPedidos.setItem(posicionFila, posicionColumna, QtWidgets.QTableWidgetItem(str(col)))
                    posicionColumna += 1
                posicionFila += 1


    def agregarPedido(self):
        from modules.Pedidos.agregarPedido import DlgAgregarPedido
        dlgAgregarPedido = DlgAgregarPedido()
        dlgAgregarPedido.exec_()


    def editarPedido(self):
        from modules.Pedidos.modificarPedido import DlgModificarPedido
        filaElegida = self.tblPedidos.currentRow()
        if filaElegida >= 0:
            idPedido = self.tblPedidos.item(filaElegida, 0).text()
            nro_pedido = self.tblPedidos.item(filaElegida, 1).text()
            id_cliente = self.tblPedidos.item(filaElegida, 2).text()
            isbn = self.tblPedidos.item(filaElegida, 3).text()
            fecha_pedido = self.tblPedidos.item(filaElegida, 4).text()
            cantidad = self.tblPedidos.item(filaElegida, 5).text()
            subtotal = self.tblPedidos.item(filaElegida, 6).text()
            estado = self.tblPedidos.item(filaElegida, 7).text()

            datosPedido = {
                'id_pedido': idPedido,
                'nro_pedido': nro_pedido,
                'id_cliente': id_cliente,
                'isbn': isbn,
                'fecha_pedido': fecha_pedido,
                'cantidad': cantidad,
                'subtotal': subtotal,
                'estado': estado
            }

            dlgModificarPedido = DlgModificarPedido(datosPedido)
            dlgModificarPedido.cargarDatosPedido(datosPedido)
            dlgModificarPedido.exec_()


    def modalEliminar(self):
        from modules.Pedidos.eliminarPedido import DlgEliminarPedido
        filaElegida = self.tblPedidos.currentRow()
        if filaElegida >= 0:  
            idPedido = self.tblPedidos.item(filaElegida, 0).text()
            nro_pedido = self.tblPedidos.item(filaElegida, 1).text()

            datosPedido = {
                'id_pedido': idPedido,
                'nro_pedido': nro_pedido
            }

            dlgEliminarPedido = DlgEliminarPedido()
            dlgEliminarPedido.cargarDatosPedido(datosPedido)
            if dlgEliminarPedido.exec_() == QDialog.Accepted:
                borrarId = dlgEliminarPedido.getID() 
                self.eliminarPedido(borrarId)


    def eliminarPedido(self, idPedido):
        if idPedido is not None:  
            cursor = libreria.cursor()
            st = f"DELETE FROM tbl_pedido_cliente WHERE id_pedido = '{idPedido}'"
            cursor.execute(st)
            libreria.commit()


    def salir(self):
        self.close()