import sys
from PyQt5 import QtWidgets, uic
import socket
from threading import Thread 
from MainWindow import Ui_MainWindow

class Client():
    def __init__(self, mainwindow):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "127.0.0.1"
        self.port = 65437
        self.mainwindow = mainwindow
        # Non blocking connection
        # self.sock.settimeout(0.0)
        self.isConnected = False
        self.textBrowser = mainwindow.textBrowser
        try:
            self.sock.connect((self.host, self.port))   
            self.isConnected = True
        except:
            self.textBrowser.append("Cannot connect to server")

    # Receive data from server
    def run(self):
        while self.isConnected:
            try:
                data = self.sock.recv(1024)
                msg = self.decrypt(data.decode("utf-8"))
                self.textBrowser.append("Message received from client: " + msg)
                if msg == "rekey":
                    self.mainwindow.rekey()
            except:
                pass

    def sendData(self, msg):
        if(self.isConnected):
            self.sock.sendall(str.encode(self.encrypt(msg), "utf-8"))

    def terminate(self):
        self.isConnected = False

    # TODO (Erkut): Implement encrypt
    def encrypt(self, msg):
        return msg

    # TODO (Erkut): Implement decrypt
    def decrypt(self, msg):
        return msg

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        # Button callbacks
        self.rekeyButton.clicked.connect(self.rekeyButtonCallback)
        self.runClientButton.clicked.connect(self.runClientCallback)
        self.sendButton.clicked.connect(self.sendCommandCallback)
        self.client = None
        self.isClientUp = False

    def rekeyButtonCallback(self):
        # self.textBrowser.append("Rekey issued from client")
        self.sendEncryptedCommand("rekey")
        self.rekey()
    
    # TODO (Erkut): Implement rekey
    def rekey(self):
        self.textBrowser.append("Rekeying ...")

    def sendCommandCallback(self):
        text = self.commandPlainTextEdit.toPlainText()
        # self.textBrowser.append(text + " message sent to client")
        self.sendEncryptedCommand(text)

    def runClientCallback(self):
        if(not self.isClientUp):
            self.client = Client(self)
            self.clientThread = Thread(target = self.client.run, args =())
            self.clientThread.start()
            if(self.client.isConnected):
                self.textBrowser.append("Client stated")
                self.isClientUp = True
                # TODO (Vatan): Add green client status button
        else:
            self.textBrowser.append("Client already running")

    def sendEncryptedCommand(self, msg):
        self.textBrowser.append("Sending encrypted message: " + msg)
        if(self.isClientUp):
            self.client.sendData(msg)
        else:
            self.textBrowser.append("Client not connected cannot send message")

    def closeEvent(self, event):
        if(self.isClientUp):
            self.client.terminate()
            # TODO (Vatan): Fix assertion error
            self.clientThread._stop()
    
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':         
    main()
