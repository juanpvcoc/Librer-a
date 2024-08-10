# @autor: Juan Velásquez
# @fecha: 2023/11/17
# @descripción: Módulo para modificar pedidos

# Importar módulos de PyQt5
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QDate
from PyQt5.uic import loadUi

# Importar módulos propios de la aplicación
from modules.conection import libreria # Base de datos
from modules.comboBox import estados


class DlgModificarPedido(QDialog):
    def __init__(self, datosPedido):
        super(DlgModificarPedido, self).__init__()
        loadUi('./UIs/Pedidos/modificarPedido.ui', self)
        self.idPedido = datosPedido.get('id_pedido', None)

        self.datosOriginales = {}
        self.obtenerDatosOriginales()
        self.txtIsbn.textChanged.connect(self.actualizarCantidadSubtotal)
        self.spCantidad.valueChanged.connect(self.actualizarSubtotal)

        # Conectar los cambios de los inputs a la función que habilita el botón de actualizar
        self.txtNro_pedido.textChanged.connect(self.habilitarActualizar)
        self.txtId_cliente.textChanged.connect(self.habilitarActualizar)
        self.txtIsbn.textChanged.connect(self.habilitarActualizar)
        self.dtFecha.dateChanged.connect(self.habilitarActualizar)
        self.spCantidad.valueChanged.connect(self.habilitarActualizar)
        self.spSubtotal.valueChanged.connect(self.habilitarActualizar)
        self.cbEstado.addItems(estados)
        self.cbEstado.currentTextChanged.connect(self.habilitarActualizar)

        # Botones
        self.btnActualizar.clicked.connect(self.actualizar)
        self.btnCancelar.clicked.connect(self.cancelar)

        self.habilitarActualizar()


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
                self.btnActualizar.setEnabled(True)
                self.lblWarning.setText("")  # Limpia el mensaje de error si el ISBN es válido
            else:
                self.btnActualizar.setEnabled(False)
                self.lblWarning.setText("ISBN no encontrado")  # Muestra un mensaje si el ISBN no existe

        except libreria.Error as e:
            self.lblWarning.setText(f"Error al obtener precio: {e}")
            self.btnActualizar.setEnabled(False)
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


    def actualizarStockLibro(self, isbn, cantidad):
        try:
            cursor = libreria.cursor()
            cursor.execute("SELECT cantidad_stock FROM libros WHERE isbn = %s", (isbn,))
            stockActual = cursor.fetchone()[0]

            nuevoStock = stockActual - cantidad

            # Actualizar el stock en la tabla de libros usando el nombre correcto de la columna
            cursor.execute("UPDATE libros SET cantidad_stock = %s WHERE isbn = %s", (nuevoStock, isbn))
            libreria.commit()

            # Si el stock es cero, cambiar el estado del libro a "inactivo"
            if nuevoStock == 0:
                cursor.execute("UPDATE libros SET estado = 'INACTIVO' WHERE isbn = %s", (isbn,))
                libreria.commit()

        except Exception as e:
            self.lblWarning.setText(f"Error al actualizar el stock del libro: {e}")


    def obtenerDatosOriginales(self):
        self.datosOriginales['nro_pedido'] = self.txtNro_pedido.text()
        self.datosOriginales['id_cliente'] = self.txtId_cliente.text()
        self.datosOriginales['isbn'] = self.txtIsbn.text()
        self.datosOriginales['fecha'] = self.dtFecha.date().toString('yyyy-MM-dd')
        self.datosOriginales['cantidad'] = self.spCantidad.value()
        self.datosOriginales['subtotal'] = self.spSubtotal.value()
        self.datosOriginales['estado'] = self.cbEstado.currentText()


    def camposModificados(self):
        for campo, valor in self.datosOriginales.items():
            if campo == 'fecha':
                fechaActual = self.dtFecha.date().toString('yyyy-MM-dd')
                if fechaActual != valor:
                    return True
            elif campo == 'estado':
                if self.cbEstado.currentText() != valor:
                    return True
            elif campo == 'cantidad' and self.spCantidad.value() != valor:
                return True
            elif campo == 'subtotal' and self.spSubtotal.value() != valor:
                return True
        return False


    def habilitarActualizar(self):
        self.btnActualizar.setEnabled(self.camposModificados())  # Habilitar el botón de actualizar si hay cambios


    def cargarDatosPedido(self, datosPedido):
        self.txtidPedido.setText(datosPedido.get('id_pedido', ''))
        self.txtNro_pedido.setText(datosPedido.get('nro_pedido', ''))
        self.txtId_cliente.setText(datosPedido.get('id_cliente', ''))
        self.txtIsbn.setText(datosPedido.get('isbn', ''))
        self.dtFecha.setDate(QDate.fromString(datosPedido.get('fecha_pedido', ''), 'yyyy-MM-dd'))
        self.spCantidad.setValue(int(datosPedido.get('cantidad', '')))
        self.spSubtotal.setValue(int(datosPedido.get('subtotal', '')))
        self.cbEstado.setCurrentText(datosPedido.get('estado', ''))


    def actualizar(self):
        nro_pedido = self.txtNro_pedido.text()
        id_cliente = self.txtId_cliente.text()
        isbn = self.txtIsbn.text()
        fecha = self.dtFecha.date().toString('yyyy-MM-dd')
        cantidad = self.spCantidad.value()
        subtotal = self.spSubtotal.value()
        estado = self.cbEstado.currentText()

        if not (nro_pedido and id_cliente and isbn and fecha and cantidad and subtotal):
            self.lblWarning.setText("Por favor rellene todos los campos")
            return

        try:
            cursor = libreria.cursor()
            st = (
                "UPDATE tbl_pedido_cliente SET nro_pedido = %s, id_cliente = %s, isbn = %s, fecha_pedido = %s, cantidad = %s, "
                "subtotal = %s, estado = %s WHERE id_pedido = %s"
            )

            cursor.execute(st, (nro_pedido, id_cliente, isbn, fecha, cantidad, subtotal, estado, self.idPedido))
            libreria.commit()
            self.actualizarStockLibro(isbn, cantidad) # Actualizar el stock del libro y cambiar el estado si es necesario
            self.close()

        except Exception as e:
            self.lblWarning.setText(f"Error al modificar el pedido: {e}")


    def cancelar(self):
        self.close()