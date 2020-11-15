import sys
from PyQt5 import QtWidgets, uic
import socket
from threading import Thread 
from MainWindow import Ui_MainWindow

class Server():
    def __init__(self, textBrowser):
        self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "127.0.0.1"
        self.port = 65437
        # Non blocking connection
        # self.serv.settimeout(0.0)
        self.running = True
        self.isConnected = False
        self.textBrowser = textBrowser

    def run(self):
        if(self.running):
            self.serv.bind((self.host, self.port))
            self.serv.listen()
            self.conn, addr = self.serv.accept()
            try:
                with self.conn:
                    self.textBrowser.append("Connected by" + str(addr[0]) + ", " + str(addr[1]))
                    while self.running:
                        self.isConnected = True
                        try:
                            data = self.conn.recv(1024)
                            dataStr = data.decode("utf-8")
                            self.textBrowser.append("Received " + dataStr)
                            # TODO: If rekey -> call rekey function
                        except:
                            pass
            except:
                print("Cannot connect client")

    def sendData(self, msg):
        if(self.isConnected and self.running):
            msg = self.encrypt(msg)
            self.conn.sendall(str.encode(msg, "utf-8"))
        else:
            print("Server not connected to any client")

    def terminate(self):
        print("Terminating server")
        self.running = False
        if(self.isConnected):
            self.conn.close()

    # TODO: To be filled
    def decrypt(self, msg):
        return msg

    # TODO: To be filled
    def encrypt(self, msg):
        return msg


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        # Button callbacks
        self.rekeyButton.clicked.connect(self.rekeyButtonCallback)
        self.runServerButton.clicked.connect(self.runServerCallback)
        self.sendButton.clicked.connect(self.sendCommandCallback)
        # Server
        self.serverRunning = False
        self.server = None

    def rekeyButtonCallback(self):
        self.textBrowser.append("Rekey issued from server")
        self.sendEncryptedCommand("rekey clicked")

    def sendCommandCallback(self):
        text = self.commandPlainTextEdit.toPlainText()
        # self.textBrowser.append(text + " message sent to client")
        self.sendEncryptedCommand(text)

    def runServerCallback(self):
        if(not self.serverRunning):
            self.textBrowser.append("Starting server ...")
            self.server = Server(self.textBrowser)
            self.serverThread = Thread(target = self.server.run, args =()) 
            self.serverThread.start()
            # ? Check if server started
            self.serverRunning = True
            # TODO: Add green server status button
        else:
            self.textBrowser.append("Server already running")

    def sendEncryptedCommand(self, msg):
        self.textBrowser.append("Sending encrypted message: " + msg)
        # TODO: Fix send message from server
        if(self.serverRunning):
            self.server.sendData(msg)
        else:
            self.textBrowser.append("Server not running")

    def closeEvent(self, event):
        if(self.serverRunning):
            self.server.terminate()
            self.serverRunning = False
            # TODO: Fix assertion error
            self.serverThread._stop()
            # self.serverThread.join()
    
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':         
    main()
