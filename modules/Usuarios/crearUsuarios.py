# @autor: Juan Velásquez
# @fecha: 2023/11/17
# @descripción: Módulo para crear usuarios

# Importar módulos de PyQt5
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

# Importar módulos propios de la aplicación
from modules.conection import libreria # Base de datos


class DlgCrearUsuarios(QDialog):
    def __init__(self):
        super(DlgCrearUsuarios, self).__init__()
        loadUi('./UIs/Usuarios/crearUsuarios.ui', self)

        # Botones
        self.btnAgregar.clicked.connect(self.agregar)
        self.btnCancelar.clicked.connect(self.cancelar)


    def agregar(self):
        usuario = self.txtUser.text()
        nombre = self.txtNombre.text()
        clave = self.txtPass.text()

        cursor = libreria.cursor()
        st = (f"INSERT INTO usuarios (usuario, clave, nombre) VALUES ('{usuario}', '{clave}', '{nombre}')")
        cursor.execute(st)
        libreria.commit()
        self.close()


    def cancelar(self):
        self.close()