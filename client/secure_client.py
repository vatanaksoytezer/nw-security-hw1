import sys
from PyQt5 import QtWidgets, uic
import socket
from threading import Thread 
from MainWindow import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        # Button callbacks
        self.rekeyButton.clicked.connect(self.rekeyButtonCallback)
        self.runClientButton.clicked.connect(self.runClientCallback)
        self.sendButton.clicked.connect(self.sendCommandCallback)

    def rekeyButtonCallback(self):
        self.textBrowser.append("Rekey issued from client")
        self.sendEncryptedCommand("rekey clicked")

    def sendCommandCallback(self):
        text = self.commandPlainTextEdit.toPlainText()
        self.textBrowser.append(text + " message sent to client")
        self.sendEncryptedCommand(text)

    def runClientCallback(self):
        self.textBrowser.append("Starting client ...")

    def sendEncryptedCommand(self, msg):
        # print("Sending encrypted message: ", msg)
        self.textBrowser.append("Sending encrypted message: " + msg)

    def closeEvent(self, event):
        pass
    
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':         
    main()
