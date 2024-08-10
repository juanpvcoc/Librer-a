# @autor: Juan Velásquez
# @fecha: 2023/11/17
# @descripción: Módulo para agregar libros

# Importar módulos de PyQt5
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

# Importar módulos propios de la aplicación
from modules.conection import libreria # Base de datos
from modules.comboBox import categorias, estados


class DlgAgregar(QDialog):
    def __init__(self):
        super(DlgAgregar, self).__init__()
        loadUi('./UIs/Libros/modalAgregar.ui', self)

        # Conectar señales a la función de validación
        self.txtIsbn.textChanged.connect(self.validarCampos)
        self.txtTitulo.textChanged.connect(self.validarCampos)
        self.dtFechaPub.dateChanged.connect(self.validarCampos)
        self.cbCategoria.addItems(categorias) # Carga las categorías
        self.cbCategoria.currentTextChanged.connect(self.validarCampos)
        self.txtPrecio.textChanged.connect(self.validarCampos)
        self.txtPortada.textChanged.connect(self.validarCampos)
        self.spCantidadStock.valueChanged.connect(self.validarCampos)
        self.cbEstado.addItems(estados)
        self.cbEstado.currentTextChanged.connect(self.validarCampos)

        self.validarCampos()  # Llamada inicial para deshabilitar el botón al inicio

        # Botones
        self.btnAgregar.clicked.connect(self.agregar)
        self.btnCancelar.clicked.connect(self.cancelar)


    def validarCampos(self):
        # Obtener los valores de los campos
        isbn = self.txtIsbn.text()
        titulo = self.txtTitulo.text()
        fechaPub = self.dtFechaPub.date().toString('yyyy-MM-dd')
        categoria = self.cbCategoria.currentText()
        precio = self.txtPrecio.text()
        portada = self.txtPortada.text()
        cantidadStock = str(self.spCantidadStock.value()) 
        estado = self.cbEstado.currentText()

        # Verificar si algún campo está vacío
        camposVacios = [campo for campo in [isbn, titulo, fechaPub, categoria, precio, portada, cantidadStock, estado] if not campo]

        # Si hay campos vacíos, deshabilitar el botón y mostrar un mensaje
        if camposVacios:
            self.btnAgregar.setEnabled(False)
        else:
            self.btnAgregar.setEnabled(True)


    def agregar(self):
            isbn = self.txtIsbn.text()
            titulo = self.txtTitulo.text()
            fechaPub = self.dtFechaPub.date().toString('yyyy-MM-dd')  # Obtiene la fecha del QDateEdit
            categoria = self.cbCategoria.currentText()
            precio = self.txtPrecio.text()
            portada = self.txtPortada.text()
            cantidadStock = str(self.spCantidadStock.value())
            estado = self.cbEstado.currentText()

            try:
                cursor = libreria.cursor()
                consultaCategoria = f"SELECT id_categoria FROM categorias WHERE categoria = '{categoria}'" # Consulta para verificar si la categoría existe
                cursor.execute(consultaCategoria)
                resultado = cursor.fetchone()

                if resultado:
                    idCategoria = resultado[0]

                    # Insertar el libro en la base de datos utilizando idCategoria
                    insertarLibro = (f"INSERT INTO libros (isbn, titulo, fecha_pub, categoria, precio, portada, cantidad_stock, estado) "
                                    f"VALUES ('{isbn}', '{titulo}', '{fechaPub}', '{idCategoria}', '{precio}', '{portada}', '{cantidadStock}', '{estado}')")
                    cursor.execute(insertarLibro)
                    libreria.commit()
                    self.close()
                else:
                    self.lblWarning.setText("Por favor seleccione una categoría")

            except Exception as e:
                self.lblWarning.setText(f"Error al agregar el libro: {str(e)}")


    def cancelar(self):
        self.close()  # Cerrar solo la ventana actual