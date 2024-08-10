# @autor: Juan Velásquez
# @fecha: 2023/11/17
# @descripción: Módulo principal de los clientes


# Importar módulos propios de Python
import datetime

# Importar módulos de PyQt5
from PyQt5.QtWidgets import QDialog, QHeaderView
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi

# Importar módulos propios de la aplicación
from modules.conection import libreria # Base de datos


class DlgClientes(QDialog):
    def __init__(self):
        super(DlgClientes, self).__init__()
        loadUi('./UIs/Clientes/clientes.ui', self)

        self.tblClientes.itemSelectionChanged.connect(self.actualizarBotones) # Conectar la señal de selección de la tabla a la función que actualiza los botones
        self.actualizarBotones() # Llamada inicial para deshabilitar los botones al inicio

        # Botones
        self.btnActualizar.clicked.connect(self.cargarDatos)
        self.btnBuscar.clicked.connect(self.buscarCliente)
        self.btnAgregar.clicked.connect(self.agregar)
        self.btnModificar.clicked.connect(self.modificar)
        self.btnEliminar.clicked.connect(self.modalEliminar)
        self.btnSalir.clicked.connect(self.salir)

        # Columnas de la tabla
        nombreColumnas = [
            'ID Cliente',
            'Identificación',
            'Nombres',
            'Apellidos',
            'Teléfono',
            'Dirección',
            'Correo',
            'Estado'
        ]

        self.tblClientes.setColumnCount(len(nombreColumnas)) # Establecer el número de columnas
        self.tblClientes.setHorizontalHeaderLabels(nombreColumnas) # Establecer el nombre de las columnas

        # Adaptar columnas al ancho de la tabla
        self.tblClientes.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tblClientes.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)

        self.cargarDatos()


    def actualizarBotones(self):
        # Obtener la cantidad de elementos seleccionados
        itemSeleccionado = self.tblClientes.selectedItems()
        habilitarBoton = len(itemSeleccionado) > 0

        # Habilitar/deshabilitar los botones de editar y eliminar cuando se selecciona una fila
        self.btnModificar.setEnabled(habilitarBoton)
        self.btnEliminar.setEnabled(habilitarBoton)


    def agregar(self):
        from modules.Clientes.agregarCliente import DlgAgregarClientes
        dlgAgregarClientes = DlgAgregarClientes()
        dlgAgregarClientes.exec_()


    def modificar(self):
        from modules.Clientes.modificarCliente import DlgModificarClientes
        filaElegida = self.tblClientes.currentRow()
        if filaElegida >= 0:
            idCliente = self.tblClientes.item(filaElegida, 0).text()
            identificacion = self.tblClientes.item(filaElegida, 1).text()
            nombres = self.tblClientes.item(filaElegida, 2).text()
            apellidos = self.tblClientes.item(filaElegida, 3).text()
            telefono = self.tblClientes.item(filaElegida, 4).text()
            direccion = self.tblClientes.item(filaElegida, 5).text()
            correo = self.tblClientes.item(filaElegida, 6).text()
            estado = self.tblClientes.item(filaElegida, 7).text()

            datosCliente = {
                'id_cliente': idCliente,
                'identificacion': identificacion,
                'nombres': nombres,
                'apellidos': apellidos,
                'telefono': telefono,
                'direccion': direccion,
                'correo_electronico': correo,
                'estado': estado
            }

            dlgModificarClientes = DlgModificarClientes(datosCliente)
            dlgModificarClientes.cargarDatosCliente(datosCliente)
            dlgModificarClientes.exec_()


    def modalEliminar(self):
        from modules.Clientes.eliminarCliente import DlgEliminarClientes
        filaElegida = self.tblClientes.currentRow()
        if filaElegida >= 0:  
            idCliente = self.tblClientes.item(filaElegida, 0).text()
            identificacion = self.tblClientes.item(filaElegida, 1).text()

            datosCliente = {
                'id_cliente': idCliente,
                'identificacion': identificacion
            }

            dlgEliminarClientes = DlgEliminarClientes()
            dlgEliminarClientes.cargarDatosCliente(datosCliente)
            if dlgEliminarClientes.exec_() == QDialog.Accepted:
                borrarId = dlgEliminarClientes.getID() 
                self.eliminarUsuario(borrarId)


    def eliminarUsuario(self, idCliente):
        if idCliente is not None:  
            cursor = libreria.cursor()
            st = f"DELETE FROM clientes WHERE id_cliente = '{idCliente}'"
            cursor.execute(st)
            libreria.commit()
    
    
    # Carga de datos en la tabla
    def cargarDatos(self):
        cursor = libreria.cursor()
        st = """SELECT * FROM clientes ORDER BY nombres"""
        cursor.execute(st)
        filas = cursor.fetchall()
        numFilas = len(filas)
        self.tblClientes.setRowCount(numFilas)
        f = 0

        if filas:
            for fila in filas:
                self.tblClientes.setItem(f, 0, QtWidgets.QTableWidgetItem(str(fila[0])))
                self.tblClientes.setItem(f, 1, QtWidgets.QTableWidgetItem(str(fila[1])))
                self.tblClientes.setItem(f, 2, QtWidgets.QTableWidgetItem(str(fila[2])))
                self.tblClientes.setItem(f, 3, QtWidgets.QTableWidgetItem(str(fila[3])))
                self.tblClientes.setItem(f, 4, QtWidgets.QTableWidgetItem(str(fila[4])))
                self.tblClientes.setItem(f, 5, QtWidgets.QTableWidgetItem(str(fila[5])))
                self.tblClientes.setItem(f, 6, QtWidgets.QTableWidgetItem(str(fila[6])))
                self.tblClientes.setItem(f, 7, QtWidgets.QTableWidgetItem(str(fila[7])))
                f += 1

        # self.tblClientes.resizeColumnToContents(0)
        # self.tblClientes.resizeColumnToContents(1)
        # self.tblClientes.resizeColumnToContents(2)
        # self.tblClientes.resizeColumnToContents(3)
        # self.tblClientes.resizeColumnToContents(4)
        # self.tblClientes.resizeColumnToContents(5)
        # self.tblClientes.resizeColumnToContents(6)
        # self.tblClientes.resizeColumnToContents(7)


    def buscarCliente(self):
        buscar = self.txtBusqueda.text().lower()

        cursor = libreria.cursor()
        st = """SELECT id_cliente, identificacion, nombres, apellidos, telefono, direccion, correo_electronico, estado FROM clientes WHERE (LOWER(nombres) LIKE %s OR LOWER(apellidos) LIKE %s OR identificacion LIKE %s) """
        params = ('%' + buscar + '%', '%' + buscar + '%', '%' + buscar + '%')

        cursor.execute(st, params)
        filas = cursor.fetchall()
        self.tblClientes.setRowCount(0)  # Limpiar la tabla

        if filas:
            posicionFila = 0
            self.tblClientes.setRowCount(len(filas))  # Establecer el número de filas según los resultados de la búsqueda
            for fila in filas:
                posicionColumna = 0
                for col in fila:
                    col = str(col) if col else ''  # Convertir a cadena si no es None
                    self.tblClientes.setItem(posicionFila, posicionColumna, QtWidgets.QTableWidgetItem(str(col)))
                    posicionColumna += 1
                posicionFila += 1


    def salir(self):
        self.close()