# @autor: Juan Velásquez
# @fecha: 2023/11/17
# @descripción: Módulo principal de la librería

# Importar módulos de PyQt5
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi


# Clase Principal
class DlgPrincipal(QMainWindow):
    def __init__(self, usuario): # Constructor __init__
        super(DlgPrincipal, self).__init__()
        loadUi('./UIs/principal.ui', self)
        self.usuario = usuario # Define el atributo 'usuario' en el constructor para enviarlo a los demás módulos
        self.lblUser.setText(f"Bienvenido, {usuario["nombre"]}")

        # Botones
        self.btnLibros.clicked.connect(self.libros)
        self.btnAutores.clicked.connect(self.autores)
        self.btnPedidos.clicked.connect(self.pedidos)
        self.btnClientes.clicked.connect(self.clientes)
        self.btnUsuarios.clicked.connect(self.usuarios)
        self.btnReportes.clicked.connect(self.reportes)
        self.btnSalir.clicked.connect(self.salir)


    def libros(self):
        from modules.Libros.library import DlgLibreria
        dlgLibreria = DlgLibreria()
        dlgLibreria.exec_()


    def autores(self):
        from modules.Autores.autores import DlgAutores
        dlgAutores = DlgAutores()
        dlgAutores.exec_()


    def pedidos(self):
            from modules.Pedidos.pedidos import DlgPedidos
            dlgPedidos = DlgPedidos()
            dlgPedidos.exec_()


    def clientes(self):
            from modules.Clientes.clientes import DlgClientes
            dlgClientes = DlgClientes()
            dlgClientes.exec_()


    def usuarios(self):
        from modules.Usuarios.usuarios import DlgUsuarios
        dlgUsuarios = DlgUsuarios()
        dlgUsuarios.exec_()


    def reportes(self):
        from modules.Reportes.reportes import DlgReportes
        dlgReportes = DlgReportes()
        dlgReportes.exec_()


    def salir(self):
        self.close()  # Cerrar solo la ventana actual