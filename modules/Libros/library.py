# @autor: Juan Velásquez
# @fecha: 2023/11/17
# @descripción: Módulo principal de la librería

# Importar módulos de PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QHeaderView
from PyQt5.uic import loadUi

# Importar módulos propios de la aplicación
from modules.conection import libreria # Base de datos
from modules.comboBox import categorias, buscarPor


# Clase Principal
class DlgLibreria(QDialog):
    def __init__(self): # Constructor __init__
        super(DlgLibreria, self).__init__()
        loadUi('./UIs/Libros/library.ui', self)

        self.tblLibros.itemSelectionChanged.connect(self.actualizarBotones) # Conectar la señal de selección de la tabla a la función que actualiza los botones
        self.actualizarBotones() # Llamada inicial para deshabilitar los botones al inicio

        # Botones
        self.btnBuscar.clicked.connect(self.buscarLibro)
        self.btnActualizar.clicked.connect(self.cargarDatos)
        self.btnAgregar.clicked.connect(self.ventanaAgregar)
        self.btnEditar.clicked.connect(self.ventanaEditar)
        self.btnEliminar.clicked.connect(self.ventanaEliminar)
        self.btnSalir.clicked.connect(self.salir)

        # Botones de filtro
        self.cbCategorias.addItems(categorias)
        self.cbCategorias.currentIndexChanged.connect(self.aplicarFiltro) # ComboBox
        self.cbBuscarPor.addItems(buscarPor)
        self.cbActivo.stateChanged.connect(self.aplicarFiltro) # CheckBox

        # Columnas de la tabla
        nombreColumnas = [
            'ISBN',
            'Título',
            'Publicado en',
            'Categoría',
            'Precio',
            'Portada',
            'Cantidad',
            'Estado'
        ]

        self.tblLibros.setColumnCount(len(nombreColumnas)) # Establecer el número de columnas
        self.tblLibros.setHorizontalHeaderLabels(nombreColumnas) # Establecer el nombre de las columnas

        # Adaptar columnas al ancho de la tabla
        self.tblLibros.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tblLibros.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)

        self.cargarDatos()


    def actualizarBotones(self):
        itemSeleccionado = self.tblLibros.selectedItems()
        habilitarBoton = len(itemSeleccionado) > 0

        # Habilitar/deshabilitar los botones de editar y eliminar cuando se selecciona una fila
        self.btnEditar.setEnabled(habilitarBoton)
        self.btnEliminar.setEnabled(habilitarBoton)


    # Ventanas modales
    def ventanaAgregar(self):
        from modules.Libros.modalAgregar import DlgAgregar
        dlgAgregar = DlgAgregar()
        dlgAgregar.exec_()


    def ventanaEditar(self):
        from modules.Libros.modalEditar import DlgEditar

        filaElegida = self.tblLibros.currentRow()
        if filaElegida >= 0:  # Verifica si hay una fila seleccionada
            isbn = self.tblLibros.item(filaElegida, 0).text()
            titulo = self.tblLibros.item(filaElegida, 1).text()
            fechaPub = self.tblLibros.item(filaElegida, 2).text()
            categoria = self.tblLibros.item(filaElegida, 3).text()
            precio = self.tblLibros.item(filaElegida, 4).text()
            portada = self.tblLibros.item(filaElegida, 5).text()
            cantidad = self.tblLibros.item(filaElegida, 6).text()
            estado = self.tblLibros.item(filaElegida, 7).text()

            datosLibro = {
                'isbn': isbn,
                'titulo': titulo,
                'fecha_pub': fechaPub,
                'categoria': categoria,
                'precio': precio,
                'portada': portada,
                'cantidad': cantidad,
                'estado': estado
            }
        else:
            datosLibro = {}

        dlgEditar = DlgEditar()
        dlgEditar.cargarDatosLibro(datosLibro)  # Pasa los datos del libro a la ventana modal
        dlgEditar.exec_()


    def ventanaEliminar(self):
        from modules.Libros.modalEliminar import DlgEliminar

        filaElegida = self.tblLibros.currentRow()
        if filaElegida >= 0:  
            isbn = self.tblLibros.item(filaElegida, 0).text()
            titulo = self.tblLibros.item(filaElegida, 1).text()

            datosLibro = {
                'isbn': isbn,
                'titulo': titulo
            }

            dlgEliminar = DlgEliminar()
            dlgEliminar.cargarDatosLibro(datosLibro)
            if dlgEliminar.exec_() == QDialog.Accepted:  # Verifica si se presionó el botón Confirmar
                borrarIsbn = dlgEliminar.getISBN()  # Obtener el ISBN del modal
                self.eliminarLibro(borrarIsbn)  # Llama al método eliminarLibro con el ISBN


    def eliminarLibro(self, isbn):
        if isbn is not None:  
            cursor = libreria.cursor()
            st = f"DELETE FROM libros WHERE isbn = '{isbn}'"
            cursor.execute(st)
            libreria.commit()


    # Carga de datos en la tabla
    def cargarDatos(self):
        cursor = libreria.cursor()
        st = """SELECT l.isbn, l.titulo, l.fecha_pub, c.categoria, l.precio, l.portada, l.cantidad_stock, l.estado 
                FROM libros l 
                LEFT JOIN categorias c ON l.categoria = c.id_categoria
                ORDER BY l.titulo"""
        cursor.execute(st)
        filas = cursor.fetchall()
        numFilas = len(filas)
        self.tblLibros.setRowCount(numFilas)
        f = 0

        if filas:
            for fila in filas:
                self.tblLibros.setItem(f, 0, QtWidgets.QTableWidgetItem(str(fila[0])))
                self.tblLibros.setItem(f, 1, QtWidgets.QTableWidgetItem(fila[1]))
                fecha_pub = fila[2].strftime('%Y-%m-%d') if fila[2] else '' # Ajustar formato de fecha
                self.tblLibros.setItem(f, 2, QtWidgets.QTableWidgetItem(fecha_pub))
                categoria = fila[3] if fila[3] else 'Sin categoría' # Verificar la categoría
                self.tblLibros.setItem(f, 3, QtWidgets.QTableWidgetItem(categoria))
                self.tblLibros.setItem(f, 4, QtWidgets.QTableWidgetItem(str(fila[4])))
                self.tblLibros.setItem(f, 5, QtWidgets.QTableWidgetItem(str(fila[5])))
                cantidad = str(fila[6])  # Convertir la cantidad a cadena
                self.tblLibros.setItem(f, 6, QtWidgets.QTableWidgetItem(cantidad))
                self.tblLibros.setItem(f, 7, QtWidgets.QTableWidgetItem(fila[7]))
                f += 1

        # Ajustar automáticamente el ancho de la columna del título al contenido más largo. El índice (0) representa la columna del título
        # self.tblLibros.resizeColumnToContents(0)
        # self.tblLibros.resizeColumnToContents(1)
        # self.tblLibros.resizeColumnToContents(2)
        # self.tblLibros.resizeColumnToContents(3)
        # self.tblLibros.resizeColumnToContents(4)
        # self.tblLibros.resizeColumnToContents(5)
        # self.tblLibros.resizeColumnToContents(6)
        # self.tblLibros.resizeColumnToContents(7)


    def buscarLibro(self):
        buscar = self.txtBusqueda.text().lower()
        filtroBusqueda = self.cbBuscarPor.currentText()

        if filtroBusqueda == "Libros":
            self.aplicarFiltro(buscar)
        elif filtroBusqueda == "Autores":
            self.aplicarFiltroAutores()


    def aplicarFiltro(self, buscar):
        cursor = libreria.cursor()
        st = """SELECT l.isbn, l.titulo, l.fecha_pub, c.categoria, l.precio, l.portada, l.cantidad_stock, l.estado 
                FROM libros l 
                LEFT JOIN categorias c ON l.categoria = c.id_categoria 
                WHERE (LOWER(l.titulo) LIKE %s OR l.isbn LIKE %s)"""

        params = ('%' + str(buscar) + '%', '%' + str(buscar) + '%')

        # Si el checkbox está marcado, agregar la condición para libros activos
        if self.cbActivo.isChecked():
            st += " AND l.estado = 'Activo'"

        # Si se selecciona una categoría, agregar la condición de la categoría
        if self.cbCategorias.currentIndex() > 0:
            categoria_seleccionada = self.cbCategorias.currentText()
            st += " AND LOWER(c.categoria) = %s"
            params += (categoria_seleccionada.lower(),)

        cursor.execute(st, params)
        filas = cursor.fetchall()
        self.tblLibros.setRowCount(0)  # Limpiar la tabla

        if filas:
            posicionFila = 0
            self.tblLibros.setRowCount(len(filas))
            for fila in filas:
                posicionColumna = 0
                for col in fila:
                    if posicionColumna == 2: # Ajustar formato de fecha
                        col = col.strftime('%Y-%m-%d') if col else ''
                    elif posicionColumna == 3 and not col:  # Verificar la categoría
                        col = 'Sin categoría'

                    self.tblLibros.setItem(posicionFila, posicionColumna, QtWidgets.QTableWidgetItem(str(col)))
                    posicionColumna += 1
                posicionFila += 1


    def aplicarFiltroAutores(self):
        buscar = self.txtBusqueda.text().lower()
        cursor = libreria.cursor()
        st = """SELECT l.isbn, l.titulo, l.fecha_pub, c.categoria, l.precio, l.portada, l.cantidad_stock, l.estado, a.nombres, a.apellidos
                FROM libros l 
                LEFT JOIN categorias c ON l.categoria = c.id_categoria 
                LEFT JOIN libro_por_autor la ON l.isbn = la.isbn
                LEFT JOIN autores a ON la.id_autor = a.id_autor
                WHERE LOWER(a.nombres) LIKE %s OR LOWER(a.apellidos) LIKE %s """

        params = ('%' + buscar + '%', '%' + buscar + '%')

        if self.cbActivo.isChecked():
            st += " AND l.estado = 'ACTIVO'"

        cursor.execute(st, params)
        filas = cursor.fetchall()
        self.tblLibros.setRowCount(0)  # Limpiar la tabla

        if filas:
            posicionFila = 0
            self.tblLibros.setRowCount(len(filas))
            for fila in filas:
                posicionColumna = 0
                for col in fila:
                    if posicionColumna == 2: # Ajustar formato de fecha
                        col = col.strftime('%Y-%m-%d') if col else ''
                    elif posicionColumna == 3 and not col:  # Verificar la categoría
                        col = 'Sin categoría'

                    self.tblLibros.setItem(posicionFila, posicionColumna, QtWidgets.QTableWidgetItem(str(col)))
                    posicionColumna += 1
                posicionFila += 1


    def salir(self):
        self.close()  # Cerrar solo la ventana actual