# @autor: Juan Velásquez
# @fecha: 2023/11/17
# @descripción: Módulo principal de la librería

#Importar módulos propios de Python
from datetime import datetime

# Importar módulos de PyQt5
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer

# Importar módulos propios de la aplicación
from modules.conection import libreria # Base de datos

# Importar los módulos de ReportLab
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


# Clase Principal
class DlgReportes(QDialog):
    def __init__(self): # Constructor __init__
        super(DlgReportes, self).__init__()
        loadUi('./UIs/Reportes/reportes.ui', self)

        # Botones
        self.btnLibros.clicked.connect(self.reporteLibros)
        self.btnClientes.clicked.connect(self.reporteClientes)
        self.btnPedidos.clicked.connect(self.reportePedidos)
        self.btnSalir.clicked.connect(self.salir)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.borrarMensaje)


    def reporteLibros(self):
        from reportlab.lib.pagesizes import landscape

        # Generar la fecha y hora actual
        fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nombreArchivo = f"reporte_libros_{fecha}.pdf"
        titulo = "REPORTE DE LIBROS"
        encabezado = "ISBN\tTÍTULO\tAUTOR\tPUBLICACIÓN\tCATEGORÍA\tPRECIO\tCANTIDAD"

        # Incluir los encabezados en la lista de líneas
        lineas = [encabezado]

        cursor = libreria.cursor()
        st = ("SELECT l.isbn, l.titulo, CONCAT(a.nombres, ' ', a.apellidos) AS autor, l.fecha_pub, c.categoria, l.precio, l.cantidad_stock "
            "FROM libros l "
            "INNER JOIN categorias c ON l.categoria = c.id_categoria "
            "INNER JOIN libro_por_autor lpa ON l.isbn = lpa.isbn "
            "INNER JOIN autores a ON lpa.id_autor = a.id_autor")
        cursor.execute(st)
        registros = cursor.fetchall()

        # Recorrido de los registros para crear las líneas del reporte
        for registro in registros:
            linea = f"{registro[0]}\t{registro[1]}\t{registro[2]}\t{str(registro[3])}\t{registro[4]}\t{registro[5]}\t{registro[6]}"
            lineas.append(linea)

        pdf = canvas.Canvas(nombreArchivo, pagesize=letter)
        pdf.setTitle(titulo)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("Courier-Bold", 12)
        pdf.drawCentredString(290, 720, titulo)
        pdf.line(30, 710, 550, 710)

        text = pdf.beginText(40, 680)
        text.setFont("Courier", 10)

        for linea in lineas:
            text.textLine(linea)

        pdf.drawText(text)
        pdf.save()
        self.lblWarning.setText("¡Reporte de libros generado!")
        self.timer.start(3000)  # 3000 milisegundos = 3 segundos



    def reporteClientes(self):
        # Generar la fecha y hora actual
        fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nombreArchivo = f"reporte_clientes_{fecha}.pdf"
        titulo = "REPORTE DE CLIENTES"
        encabezado = "ID\tNOMBRES\tAPELLIDOS\tTELÉFONO\tDIRECCIÓN\tCORREO"

        # Incluir los encabezados en la lista de líneas
        lineas = [encabezado]

        cursor = libreria.cursor()
        st = ("SELECT identificacion, nombres, apellidos, telefono, direccion, correo_electronico FROM clientes")
        cursor.execute(st)
        registros = cursor.fetchall()

        # Recorrido de los registros para crear las líneas del reporte
        for registro in registros:
            linea = f"{registro[0]}\t{registro[1]}\t{registro[2]}\t{str(registro[3])}\t{registro[4]}\t{registro[5]}"
            lineas.append(linea)

        pdf = canvas.Canvas(nombreArchivo, pagesize=letter)
        pdf.setTitle(titulo)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("Courier-Bold", 12)
        pdf.drawCentredString(290, 720, titulo)
        pdf.line(30, 710, 550, 710)

        text = pdf.beginText(40, 680)
        text.setFont("Courier", 10)

        for linea in lineas:
            text.textLine(linea)

        pdf.drawText(text)
        pdf.save()
        self.lblWarning.setText("¡Reporte de clientes generado!")
        self.timer.start(3000)  # 3000 milisegundos = 3 segundos


    def reportePedidos(self):
        # Generar la fecha y hora actual
        fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nombreArchivo = f"reporte_pedidos_{fecha}.pdf"
        titulo = "REPORTE DE PEDIDOS"
        encabezado = "ID PEDIDO\tNRO PEDIDO\tCLIENTE\tLIBRO (ISBN)\tFECHA PEDIDO\tCANTIDAD\tSUBTOTAL"

        # Incluir los encabezados en la lista de líneas
        lineas = [encabezado]

        cursor = libreria.cursor()
        st = ("SELECT pc.id_pedido, pc.nro_pedido, CONCAT(cl.nombres, ' ', cl.apellidos) AS cliente, CONCAT(l.titulo, ' (', l.isbn, ')') AS libro, "
            "pc.fecha_pedido, pc.cantidad, pc.subtotal "
            "FROM tbl_pedido_cliente pc "
            "INNER JOIN clientes cl ON pc.id_cliente = cl.id_cliente "
            "INNER JOIN libros l ON pc.isbn = l.isbn")
        cursor.execute(st)
        registros = cursor.fetchall()

        # Recorrido de los registros para crear las líneas del reporte
        for registro in registros:
            linea = f"{registro[0]}\t{registro[1]}\t{registro[2]}\t{registro[3]}\t{str(registro[4])}\t{registro[5]}\t{registro[6]}"
            lineas.append(linea)

        pdf = canvas.Canvas(nombreArchivo, pagesize=letter)
        pdf.setTitle(titulo)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("Courier-Bold", 12)
        pdf.drawCentredString(290, 720, titulo)
        pdf.line(30, 710, 550, 710)

        text = pdf.beginText(40, 680)
        text.setFont("Courier", 10)

        for linea in lineas:
            text.textLine(linea)

        pdf.drawText(text)
        pdf.save()
        self.lblWarning.setText("¡Reporte de pedidos generado!")
        self.timer.start(3000)  # 3000 milisegundos = 3 segundos


    def borrarMensaje(self):
        self.lblWarning.setText("")  # Borra el mensaje
        self.timer.stop()  # Detiene el temporizador


    def salir(self):
        self.close() 