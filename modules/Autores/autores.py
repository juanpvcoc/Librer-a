# @autor: Juan Velásquez
# @fecha: 2023/11/17
# @descripción: Módulo principal de los autores

# Importar módulos de PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QDialog, QHeaderView
from PyQt5.uic import loadUi

# Importar módulos propios de la aplicación
from modules.conection import libreria # Base de datos


# Clase Principal
class DlgAutores(QDialog):
    def __init__(self): # Constructor __init__
        super(DlgAutores, self).__init__()
        loadUi('./UIs/Autores/autores.ui', self)

        self.tblAutores.itemSelectionChanged.connect(self.actualizarBotones) # Conectar la señal de selección de la tabla a la función que actualiza los botones
        self.actualizarBotones() # Llamada inicial para deshabilitar los botones al inicio

        # Botones
        self.btnBuscar.clicked.connect(self.buscarAutor)
        self.btnActualizar.clicked.connect(self.cargarDatos)
        self.btnAgregar.clicked.connect(self.agregarAutor)
        self.btnModificar.clicked.connect(self.modificarAutor)
        self.btnEliminar.clicked.connect(self.modalEliminar)
        self.btnSalir.clicked.connect(self.salir)

        # Columnas de la tabla
        nombreColumnas = [
            'ID Autor',
            'Nombres',
            'Apellidos',
            'Estado'
        ]

        self.tblAutores.setColumnCount(len(nombreColumnas)) # Establece el número de columnas
        self.tblAutores.setHorizontalHeaderLabels(nombreColumnas) # Establece el nombre de las columnas

        # Adaptar columnas al ancho de la tabla
        self.tblAutores.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tblAutores.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)

        self.cargarDatos()


    # Carga de datos en la tabla
    def cargarDatos(self):
        cursor = libreria.cursor()
        st = (f"SELECT * FROM autores")
        cursor.execute(st)
        filas = cursor.fetchall()

        numFilas = len(filas)
        self.tblAutores.setRowCount(numFilas)
        f = 0

        if filas:
            for fila in filas:
                self.tblAutores.setItem(f, 0, QtWidgets.QTableWidgetItem(str(fila[0])))
                self.tblAutores.setItem(f, 1, QtWidgets.QTableWidgetItem(str(fila[1])))
                self.tblAutores.setItem(f, 2, QtWidgets.QTableWidgetItem(str(fila[2])))
                self.tblAutores.setItem(f, 3, QtWidgets.QTableWidgetItem(str(fila[3])))
                f += 1

        # self.tblAutores.resizeColumnToContents(0)
        # self.tblAutores.resizeColumnToContents(1)
        # self.tblAutores.resizeColumnToContents(2)
        # self.tblAutores.resizeColumnToContents(3)


    def actualizarBotones(self):
        # Obtener la cantidad de elementos seleccionados
        itemSeleccionado = self.tblAutores.selectedItems()
        habilitarBoton = len(itemSeleccionado) > 0

        # Habilitar/deshabilitar los botones de editar y eliminar cuando se selecciona una fila
        self.btnModificar.setEnabled(habilitarBoton)
        self.btnEliminar.setEnabled(habilitarBoton)


    def buscarAutor(self):
        buscar = self.txtBusqueda.text().lower()

        if not buscar:  # Si la búsqueda está vacía, cargar todos los registros nuevamente
            self.cargarDatos()
            return

        cursor = libreria.cursor()
        st = """SELECT * FROM autores WHERE LOWER(nombres) LIKE %s OR LOWER(apellidos) LIKE %s"""
        params = ('%' + buscar + '%', '%' + buscar + '%')

        cursor.execute(st, params)
        filas = cursor.fetchall()
        self.tblAutores.setRowCount(0)  # Limpiar la tabla

        if filas:
            posicionFila = 0
            self.tblAutores.setRowCount(len(filas))  # Establecer el número de filas según los resultados de la búsqueda
            for fila in filas:
                posicionColumna = 0
                for col in fila:
                    self.tblAutores.setItem(posicionFila, posicionColumna, QtWidgets.QTableWidgetItem(str(col)))
                    posicionColumna += 1
                posicionFila += 1


    def agregarAutor(self):
        from modules.Autores.agregarAutor import DlgAgregarAutor
        dlgAgregarAutor = DlgAgregarAutor()
        dlgAgregarAutor.exec_()


    def modificarAutor(self):
        from modules.Autores.modificarAutor import DlgModificarAutor
        filaElegida = self.tblAutores.currentRow()
        if filaElegida >= 0:
            idAutor = self.tblAutores.item(filaElegida, 0).text()
            nombres = self.tblAutores.item(filaElegida, 1).text()
            apellidos = self.tblAutores.item(filaElegida, 2).text()
            estado = self.tblAutores.item(filaElegida, 3).text()

            datosAutor = {
                'id_autor': idAutor,
                'nombres': nombres,
                'apellidos': apellidos,
                'estado': estado
            }

            dlgModificarAutor = DlgModificarAutor(datosAutor)
            dlgModificarAutor.cargarDatosAutor(datosAutor)
            dlgModificarAutor.exec_()


    def modalEliminar(self):
        from modules.Autores.eliminarAutor import DlgEliminarAutor
        filaElegida = self.tblAutores.currentRow()
        if filaElegida >= 0:  
            idAutor = self.tblAutores.item(filaElegida, 0).text()
            nombres = self.tblAutores.item(filaElegida, 1).text()
            apellidos = self.tblAutores.item(filaElegida, 2).text()

            datosAutor = {
                'id_autor': idAutor,
                'nombres': nombres,
                'apellidos': apellidos
            }

            dlgEliminarAutor = DlgEliminarAutor()
            dlgEliminarAutor.cargarDatosAutor(datosAutor)
            if dlgEliminarAutor.exec_() == QDialog.Accepted:
                borrarId = dlgEliminarAutor.getID() 
                self.eliminarAutor(borrarId)


    def eliminarAutor(self, idAutor):
        if idAutor is not None:  
            cursor = libreria.cursor()
            st = f"DELETE FROM autores WHERE id_autor = '{idAutor}'"
            cursor.execute(st)
            libreria.commit()


    def salir(self):
        self.close()