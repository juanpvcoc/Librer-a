# @autor: Juan Velásquez
# @fecha: 2023/11/17
# @descripción: Módulo para agregar pedidos

# Importar módulos de PyQt5
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QDate
from PyQt5.uic import loadUi

# Importar módulos propios de la aplicación
from modules.conection import libreria # Base de datos
from modules.comboBox import estados


class DlgAgregarPedido(QDialog):
    def __init__(self):
        super(DlgAgregarPedido, self).__init__()
        loadUi('./UIs/Pedidos/agregarPedido.ui', self)

        # Conectar señales a la función de validación
        self.txtNPedido.textChanged.connect(self.validarCampos)
        self.txtidCliente.textChanged.connect(self.validarCampos)
        self.txtIsbn.textChanged.connect(self.validarCampos)
        self.spCantidad.textChanged.connect(self.validarCampos)
        self.spSubtotal.textChanged.connect(self.validarCampos)
        self.cbEstado.addItems(estados)
        self.cbEstado.currentTextChanged.connect(self.validarCampos)

        self.validarCampos()  # Llamada inicial para deshabilitar el botón al inicio

        # Botones
        self.btnAgregar.clicked.connect(self.agregar)
        self.btnCancelar.clicked.connect(self.cancelar)

        self.dtFecha.setDate(QDate.currentDate()) # Establece la fecha actual en el campo dtFecha
        self.txtIsbn.textChanged.connect(self.actualizarCantidadSubtotal) # Conecta señales a la función de actualización de cantidad y subtotal
        self.spCantidad.valueChanged.connect(self.actualizarSubtotal)  # Actualiza el precio según la cantidad ingresada


    def actualizarCantidadSubtotal(self):
        isbn = self.txtIsbn.text()

        try:
            cursor = libreria.cursor()
            cursor.execute("SELECT precio FROM libros WHERE isbn = %s", (isbn,))
            data = cursor.fetchone()

            if data:  # Comprueba si hay resultados de la consulta
                precio = data[0]
                self.spCantidad.setValue(1)
                self.spSubtotal.setValue(precio)
                self.btnAgregar.setEnabled(True)
                self.lblWarning.setText("")  # Limpia el mensaje de error si el ISBN es válido
            else:
                self.btnAgregar.setEnabled(False)
                self.lblWarning.setText("ISBN no encontrado")  # Muestra un mensaje si el ISBN no existe

        except libreria.Error as e:
            self.lblWarning.setText(f"Error al obtener precio: {e}")
            self.btnAgregar.setEnabled(False)
            self.lblWarning.setText("Error al obtener precio del ISBN")
            self.spCantidad.setValue(0)
            self.spSubtotal.setValue(0)


    def actualizarSubtotal(self):
        isbn = self.txtIsbn.text()
        cantidad = self.spCantidad.value()

        try:
            cursor = libreria.cursor()
            cursor.execute("SELECT precio FROM libros WHERE isbn = %s", (isbn,))
            precio = cursor.fetchone()[0]

            subtotal = precio * cantidad
            self.spSubtotal.setValue(subtotal)

        except Exception as e:
            self.lblWarning.setText(f"Error al actualizar el subtotal: {e}")


    def validarCampos(self):
        nro_pedido = self.txtNPedido.text()
        id_cliente = self.txtidCliente.text()
        isbn = self.txtIsbn.text()
        cantidad = str(self.spCantidad.value()) 
        subtotal = str(self.spSubtotal.value())

        # Verifica si algún campo está vacío
        camposVacios = [campo for campo in [nro_pedido, id_cliente, isbn, cantidad, subtotal] if not campo]

        # Si hay campos vacíos, deshabilitar el botón y mostrar un mensaje
        if camposVacios:
            self.btnAgregar.setEnabled(False)
        else:
            self.btnAgregar.setEnabled(True)

    def agregar(self):
        nro_pedido = self.txtNPedido.text()
        id_cliente = self.txtidCliente.text()
        isbn = self.txtIsbn.text()
        fechaPedido = self.dtFecha.date().toString('yyyy-MM-dd')
        cantidad = self.spCantidad.value()  # Obtenemos la cantidad seleccionada
        estado = self.cbEstado.currentText()

        try:
            cursor = libreria.cursor()

            # Obtener el precio y la cantidad de stock del libro
            cursor.execute("SELECT precio, cantidad_stock FROM libros WHERE isbn = %s", (isbn,))
            data = cursor.fetchone()

            if data:  # Comprueba si hay resultados de la consulta
                precio = data[0]
                stockActual = data[1]

                if cantidad > stockActual:
                    self.lblWarning.setText("No hay suficiente stock disponible")
                    return

                # Calcular el subtotal (precio * cantidad)
                subtotal = precio * cantidad

                # Actualizar la cantidad de stock del libro
                nuevoStock = stockActual - cantidad
                cursor.execute("UPDATE libros SET cantidad_stock = %s WHERE isbn = %s", (nuevoStock, isbn))

                # Verificar si el stock actualizado es cero y cambiar el estado del libro a "inactivo"
                if nuevoStock == 0:
                    cursor.execute("UPDATE libros SET estado = 'INACTIVO' WHERE isbn = %s", (isbn,))
                    libreria.commit()

                # Inserción del pedido en la base de datos
                st = "INSERT INTO tbl_pedido_cliente (nro_pedido, id_cliente, isbn, fecha_pedido, cantidad, subtotal, estado) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(st, (nro_pedido, id_cliente, isbn, fechaPedido, cantidad, subtotal, estado))
                libreria.commit()
                self.close()

            else:
                self.lblWarning.setText("ISBN no encontrado")

        except Exception as e:
            self.lblWarning.setText(f"Error al agregar pedido: {e}")



    def cancelar(self):
        self.close()