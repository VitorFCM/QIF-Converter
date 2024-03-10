from PyQt5.QtWidgets import QDesktopWidget, QLabel, QDialogButtonBox, QLabel, QVBoxLayout, QApplication, QLineEdit, QWidget, QFormLayout, QPushButton, QDialog
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
import sys
import os.path
from QIFtoCSV import convertQIF2CSV

class AlertDialog(QDialog):
    def __init__(self, windowTitle, description):
        super().__init__()

        self.setWindowTitle(windowTitle)

        QBtn = QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        flo = QFormLayout()
        flo.addWidget(QLabel(description))
        flo.addWidget(self.buttonBox)

        self.setLayout(flo)

class lineEditDemo(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.resize(600, 500)
        self.center()

        # Criar um QLabel para a imagem de fundo
        self.background_label = QLabel(self)

        # Carregar a imagem de fundo
        pixmap = QPixmap('./tetas.jpg')  # Substitua pelo caminho da sua imagem
        self.background_label.setPixmap(pixmap)

        # Configurar a geometria do QLabel para cobrir toda a janela
        self.background_label.setGeometry(0, 0, self.width(), self.height())

        self.text_input = QLineEdit()

        button = QPushButton("Converter")
        button.clicked.connect(self.get)

        flo = QFormLayout()
        flo.addRow("Diretorio do arquivo", self.text_input)
        flo.addRow(button)

        self.setLayout(flo)
        self.setWindowTitle("Convert QIF to CSV")

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def get(self):
        path = self.text_input.text()

        alertDialogTitle = "Alerta de erro"
        alertDialogDescription = "O diretorio informado nao corresponde a um arquivo"

        if os.path.isfile(path) == True:
            CSV_file_name = convertQIF2CSV(path)
            alertDialogTitle = "Sucesso na conversao"
            alertDialogDescription = "O arquivo CSV foi salvo em: " + CSV_file_name

        dialog = AlertDialog(alertDialogTitle, alertDialogDescription)
        dialog.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('icotetas.ico'))
    win = lineEditDemo()
    win.show()
    sys.exit(app.exec_())
