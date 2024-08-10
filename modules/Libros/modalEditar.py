# @autor: Juan Velásquez
# @fecha: 2023/11/17
# @descripción: Módulo para editar libros

# Importar módulos propios de Python
from datetime import datetime

# Importar módulos de PyQt5
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import QDate

# Importar módulos propios de la aplicación
from modules.conection import libreria # Base de datos
from modules.comboBox import categorias, estados


class DlgEditar(QDialog):
    def __init__(self):
        super(DlgEditar, self).__init__()
        loadUi('./UIs/Libros/modalEditar.ui', self)

        # Conectar los cambios de los inputs a la función que habilita el botón de actualizar
        self.txtIsbn.textChanged.connect(self.habilitarActualizar)
        self.txtTitulo.textChanged.connect(self.habilitarActualizar)
        self.dtFechaPub.dateChanged.connect(self.habilitarActualizar)
        self.cbCategoria.currentTextChanged.connect(self.habilitarActualizar)
        self.txtPrecio.textChanged.connect(self.habilitarActualizar)
        self.txtPortada.textChanged.connect(self.habilitarActualizar)
        self.spCantidadStock.valueChanged.connect(self.habilitarActualizar)
        self.cbEstado.currentTextChanged.connect(self.habilitarActualizar)

        # Botones
        self.btnActualizar.clicked.connect(self.actualizar)
        self.btnCancelar.clicked.connect(self.cancelar)

        # Variables para almacenar los datos originales del libro
        self.datosOriginales = {}
        self.obtenerDatosOriginales()


    def obtenerDatosOriginales(self):
        # Obtener datos originales del libro al cargar la ventana
        self.datosOriginales['isbn'] = self.txtIsbn.text()
        self.datosOriginales['titulo'] = self.txtTitulo.text()
        self.datosOriginales['fecha_pub'] = self.dtFechaPub.date().toString('yyyy-MM-dd')
        self.datosOriginales['categoria'] = self.cbCategoria.currentText()
        self.datosOriginales['precio'] = self.txtPrecio.text()
        self.datosOriginales['portada'] = self.txtPortada.text()
        self.datosOriginales['cantidad_stock'] = self.spCantidadStock.value()
        self.datosOriginales['estado'] = self.cbEstado.currentText()


    def camposModificados(self):
        for campo, valor in self.datosOriginales.items():
            if campo == 'fecha_pub':
                fechaActual = self.dtFechaPub.date().toString('yyyy-MM-dd')
                if fechaActual != valor:
                    return True
            elif campo == 'categoria':
                if self.cbCategoria.currentText() != valor:
                    return True
            elif campo == 'cantidad':
                if str(self.spCantidadStock.value()) != valor:  # Reemplazando por QSpinBox
                    return True
            else:
                if hasattr(self, f"txt{campo.capitalize()}") and getattr(self, f"txt{campo.capitalize()}").text() != valor:
                    return True
        return False


    def habilitarActualizar(self):
        self.btnActualizar.setEnabled(self.camposModificados()) # Habilitar el botón de actualizar si hay cambios


    def cargarDatosLibro(self, datosLibro):
        self.txtIsbn.setText(datosLibro.get('isbn', ''))
        self.txtTitulo.setText(datosLibro.get('titulo', ''))

        fechaPub = datosLibro.get('fecha_pub')
        if fechaPub:  
            fechaDate = datetime.strptime(fechaPub, '%Y-%m-%d')  
            self.dtFechaPub.setDate(fechaDate)
        else:
            self.dtFechaPub.setDate(QDate.currentDate())

        self.cbCategoria.addItems(categorias)
        self.cbCategoria.setCurrentText(datosLibro.get('categoria', ''))
        self.txtPrecio.setText(datosLibro.get('precio', ''))
        self.txtPortada.setText(datosLibro.get('portada', ''))
        cantidad = datosLibro.get('cantidad', 0)  # Obtener la cantidad de stock
        self.spCantidadStock.setValue(int(cantidad))
        self.cbEstado.addItems(estados)
        self.cbEstado.setCurrentText(datosLibro.get('estado', ''))


    def actualizar(self):
        isbn = self.txtIsbn.text()
        titulo = self.txtTitulo.text()
        fechaPub = self.dtFechaPub.date().toString('yyyy-MM-dd')
        precio = self.txtPrecio.text()
        portada = self.txtPortada.text()
        cantidadStock = str(self.spCantidadStock.value())  # Obtener el valor del QSpinBox
        estado = self.cbEstado.currentText()
        nombreCategoria = self.cbCategoria.currentText() # Obtener la categoría del campo de texto
        cursor = libreria.cursor()
        categoria = f"SELECT id_categoria FROM categorias WHERE categoria = '{nombreCategoria}'" # Consulta para obtener el ID de la categoría

        # Ejecutar la consulta
        cursor.execute(categoria)
        resultado = cursor.fetchone()

        # Verificar si se encontró la categoría
        if resultado:
            idCategoria = resultado[0]
            st = "UPDATE libros SET "
            updates = []

            if titulo:
                updates.append(f"titulo = '{titulo}'")
            if fechaPub:
                updates.append(f"fecha_pub = '{fechaPub}'")
            if idCategoria: 
                updates.append(f"categoria = {idCategoria}")  # Utilizar el ID de la categoría
            if precio:
                updates.append(f"precio = '{precio}'")
            if portada:
                updates.append(f"portada = '{portada}'")
            if cantidadStock:
                updates.append(f"cantidad_stock = '{cantidadStock}'")
            if estado:
                updates.append(f"estado = '{estado}'")

            st += ", ".join(updates)
            st += f" WHERE isbn = '{isbn}'"

            cursor.execute(st)
            libreria.commit()
            self.close()
        else:
            self.lblWarning.setText("La categoría no existe en la base de datos")


    def cancelar(self):
        self.close()