# @autor: Juan Velásquez
# @fecha: 2023/11/17
# @descripción: Módulo de inicio de sesión

# Importar módulos de PyQt5
from PyQt5.QtWidgets import QDialog, QHeaderView
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi

# Importar módulos propios de la aplicación
from modules.conection import libreria # Base de datos


class DlgUsuarios(QDialog):
    def __init__(self):
        super(DlgUsuarios, self).__init__()
        loadUi('./UIs/Usuarios/modalUsuarios.ui', self)

        self.tblUsuarios.itemSelectionChanged.connect(self.actualizarBotones) # Conectar la señal de selección de la tabla a la función que actualiza los botones
        self.actualizarBotones() # Llamada inicial para deshabilitar los botones al inicio

        # Botones
        self.btnActualizar.clicked.connect(self.cargarDatos)
        self.btnBuscar.clicked.connect(self.buscarUsuario)
        self.btnAgregar.clicked.connect(self.agregar)
        self.btnModificar.clicked.connect(self.modificar)
        self.btnEliminar.clicked.connect(self.modalEliminar)
        self.btnSalir.clicked.connect(self.salir)

        # Columnas de la tabla
        nombreColumnas = [
            'ID',
            'Usuario',
            'Nombre',
            'Contraseña'
        ]

        self.tblUsuarios.setColumnCount(len(nombreColumnas)) # Establecer el número de columnas
        self.tblUsuarios.setHorizontalHeaderLabels(nombreColumnas) # Establecer el nombre de las columnas

        # Adaptar columnas al ancho de la tabla
        self.tblUsuarios.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tblUsuarios.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)

        self.cargarDatos()


    def actualizarBotones(self):
        # Obtener la cantidad de elementos seleccionados
        itemSeleccionado = self.tblUsuarios.selectedItems()
        habilitarBoton = len(itemSeleccionado) > 0

        # Habilitar/deshabilitar los botones de editar y eliminar cuando se selecciona una fila
        self.btnModificar.setEnabled(habilitarBoton)
        self.btnEliminar.setEnabled(habilitarBoton)


    def agregar(self):
        from modules.Usuarios.crearUsuarios import DlgCrearUsuarios
        dlgCrearUsuarios = DlgCrearUsuarios()
        dlgCrearUsuarios.exec_()


    def modificar(self):
        from modules.Usuarios.editarUsuarios import DlgModificarUsuarios
        filaElegida = self.tblUsuarios.currentRow()
        if filaElegida >= 0:
            id = self.tblUsuarios.item(filaElegida, 0).text()
            usuario = self.tblUsuarios.item(filaElegida, 1).text()
            nombre = self.tblUsuarios.item(filaElegida, 2).text()
            clave = self.tblUsuarios.item(filaElegida, 3).text()

            datosUsuario = {
                'id': id,
                'usuario': usuario,
                'nombre': nombre,
                'clave': clave
            }

            dlgModificarUsuarios = DlgModificarUsuarios(datosUsuario)
            dlgModificarUsuarios.cargarDatosUsuario(datosUsuario)
            dlgModificarUsuarios.exec_()


    def modalEliminar(self):
        from modules.Usuarios.eliminarUsuario import DlgEliminarUsuario
        filaElegida = self.tblUsuarios.currentRow()
        if filaElegida >= 0:  
            id = self.tblUsuarios.item(filaElegida, 0).text()
            usuario = self.tblUsuarios.item(filaElegida, 1).text()

            datosUsuario = {
                'id': id,
                'usuario': usuario
            }

            dlgEliminarUsuario = DlgEliminarUsuario()
            dlgEliminarUsuario.cargarDatosUsuario(datosUsuario)
            if dlgEliminarUsuario.exec_() == QDialog.Accepted:
                borrarId = dlgEliminarUsuario.getID() 
                self.eliminarUsuario(borrarId)


    def eliminarUsuario(self, id):
        if id is not None:  
            cursor = libreria.cursor()
            st = f"DELETE FROM usuarios WHERE id = '{id}'"
            cursor.execute(st)
            libreria.commit()
    
    
    # Carga de datos en la tabla
    def cargarDatos(self):
        cursor = libreria.cursor()
        st = """SELECT id, usuario, nombre, clave FROM usuarios ORDER BY nombre"""
        cursor.execute(st)
        filas = cursor.fetchall()
        numFilas = len(filas)
        self.tblUsuarios.setRowCount(numFilas)
        f = 0

        if filas:
            for fila in filas:
                self.tblUsuarios.setItem(f, 0, QtWidgets.QTableWidgetItem(str(fila[0])))
                self.tblUsuarios.setItem(f, 1, QtWidgets.QTableWidgetItem(fila[1]))
                self.tblUsuarios.setItem(f, 2, QtWidgets.QTableWidgetItem(fila[2]))
                self.tblUsuarios.setItem(f, 3, QtWidgets.QTableWidgetItem(fila[3]))
                f += 1

        # self.tblUsuarios.resizeColumnToContents(0)
        # self.tblUsuarios.resizeColumnToContents(1)
        # self.tblUsuarios.resizeColumnToContents(2)
        # self.tblUsuarios.resizeColumnToContents(3)


    def buscarUsuario(self):
        buscar = self.txtBusqueda.text().lower()

        cursor = libreria.cursor()
        st = """SELECT id, usuario, nombre, clave FROM usuarios WHERE (LOWER(nombre) LIKE %s OR LOWER(usuario) LIKE %s ) """
        params = ('%' + buscar + '%', '%' + buscar + '%')

        cursor.execute(st, params)
        filas = cursor.fetchall()
        self.tblUsuarios.setRowCount(0)  # Limpiar la tabla

        if filas:
            posicionFila = 0
            self.tblUsuarios.setRowCount(len(filas))  # Establecer el número de filas según los resultados de la búsqueda
            for fila in filas:
                posicionColumna = 0
                for col in fila:
                    col = str(col) if col else ''  # Convertir a cadena si no es None
                    self.tblUsuarios.setItem(posicionFila, posicionColumna, QtWidgets.QTableWidgetItem(str(col)))
                    posicionColumna += 1
                posicionFila += 1


    def salir(self):
        self.close()