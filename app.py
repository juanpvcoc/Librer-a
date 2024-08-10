# @autor: Juan Velásquez
# @fecha: 2023/11/17
# @descripción: Módulo de inicio de sesión

# Importar módulos propios de Python
import sys

# Importar módulos de PyQt5
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi

# Importar la conexión con base de datos
from modules.conection import libreria
from modules.principal import DlgPrincipal


# Clase Principal
class DlgInicio(QDialog):
    def __init__(self): # Constructor __init__
        super(DlgInicio, self).__init__()
        loadUi('./UIs/login.ui', self)

        self.btnIniciar.clicked.connect(self.iniciarSesion)

    def iniciarSesion(self):
        txtUser = self.txtUser.text()
        txtPass = self.txtPass.text()

        st = (f"SELECT * FROM usuarios WHERE usuario = '{txtUser}' AND clave = '{txtPass}'")
        cursor = libreria.cursor()
        cursor.execute(st)
        registro = cursor.fetchall()

        if registro:
            usuario = {
                'id': registro[0][0],
                'usuario': registro[0][1], 
                'clave': registro[0][2],
                'nombre': registro[0][3]
            }

            self.cajero = DlgPrincipal(usuario)
            self.cajero.show()
            self.close()
            # self.lblMessage.setText("Inicio de sesión exitoso")

        else:
            self.lblMessage.setText("Usuario o contraseña incorrectos")


# Programa principal de ejecución.
if __name__ == '__main__':
    app = QApplication(sys.argv) # Crea una instancia de QApplication
    dlgInicio = DlgInicio()
    dlgInicio.show()
    sys.exit(app.exec_())