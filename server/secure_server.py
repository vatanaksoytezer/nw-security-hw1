import sys
from PyQt5 import QtWidgets, uic
import socket
from threading import Thread 
from MainWindow import Ui_MainWindow
from Crypto.Hash import SHA512
from Crypto.Cipher import AES
import hmac
import base64
import hashlib

class AESCipher(object):

    def __init__(self, key): 
        self.bs = AES.block_size
        self.key = key # 32 bits

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = self.key[16:32]
        cipher = AES.new(self.key[0:16], AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key[0:16], AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

class Server():
    def __init__(self, mainwindow):
        self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "127.0.0.1"
        self.port = 65437
        # Non blocking connection
        # self.serv.settimeout(0.0)
        self.running = True
        self.isConnected = False
        self.mainwindow = mainwindow
        self.textBrowser = mainwindow.textBrowser
        # self.currentKey = b""
        self.array_length = 500
        self.hash_array_1 = [0] * (self.array_length+1)
        self.hash_array_2 = [0] * (self.array_length+1)
        self.hash_array_1_index = 0
        self.hash_array_2_index = self.array_length

        self.generateInitialKey()

    def run(self):
        if(self.running):
            self.serv.bind((self.host, self.port))
            self.serv.listen()
            self.conn, addr = self.serv.accept()
            try:
                with self.conn:
                    self.textBrowser.append("Connected by " + str(addr[0]) + ", " + str(addr[1]))
                    while self.running:
                        self.isConnected = True
                        try:
                            data = self.conn.recv(1024)
                            raw_data = data[:-64]
                            hmac = data[-64:].decode("utf-8")
                            msg = self.decrypt(raw_data)
                            self_mac = self.get_signature_str(msg)
                            if(self_mac == hmac):
                                self.textBrowser.append("Hash matched, reading message of hash: " + self_mac)
                                self.textBrowser.append("Message received from client: " + msg)
                                if msg == "rekey":
                                    self.mainwindow.rekey()
                            else:
                                self.textBrowser.append("Authentication Error")
                        except:
                            pass
            except:
                print("Cannot connect client")

    def sendData(self, msg):
        if(self.isConnected and self.running):
            self.conn.sendall(self.encrypt(msg))
        else:
            print("Server not connected to any client")

    def terminate(self):
        print("Terminating server")
        self.running = False
        if(self.isConnected):
            self.conn.close()

    def encrypt(self, msg):
        aes = AESCipher(self.currentKey)
        signature = self.get_signature_str(msg)
        encrypted = aes.encrypt(msg)
        return (encrypted + bytes(signature, 'utf-8'))
    
    def decrypt(self, msg):
        aes = AESCipher(self.currentKey)
        decrypted = aes.decrypt(msg)
        return decrypted

    def generateInitialKey(self):
        # Generate seed
        seed1, seed2 = 1, 7
        # Seeds to bytes
        seed_bytes_1 = bytes(str(seed1), 'ascii')
        seed_bytes_2 = bytes(str(seed2), 'ascii')
        # Populate keys
        key_1 = SHA512.new(seed_bytes_1)
        key_2 = SHA512.new(seed_bytes_2)
        self.hash_array_1[0] = key_1
        self.hash_array_2[0] = key_2
        for i in range(self.array_length):
            key_1 = SHA512.new(key_1.digest())
            key_2 = SHA512.new(key_2.digest())
            self.hash_array_1[i+1] = key_1
            self.hash_array_2[i+1] = key_2
        # Assign first key
        self.currentKey = bytes([_a ^ _b for _a, _b in zip(self.hash_array_1[self.hash_array_1_index].digest(), 
            self.hash_array_2[self.hash_array_2_index].digest())])
        # Show current key
        self.mainwindow.currentKeyEmptyLabel.setText(self.currentKey.hex())
        self.mainwindow.aesEncryptEmpytLabel.setText(self.currentKey[0:16].hex())
        self.mainwindow.aesIVEmptyLabel.setText(self.currentKey[16:32].hex())
        self.mainwindow.shaEmptyLabel.setText(self.currentKey[32:].hex())
        

    def rekey(self):
        self.hash_array_1_index += 1
        self.hash_array_2_index -= 1
        # Show previous key
        self.mainwindow.prevKeyEmptyLabel.setText(self.currentKey.hex())
        # Assign current key
        self.currentKey = bytes([_a ^ _b for _a, _b in zip(self.hash_array_1[self.hash_array_1_index].digest(), 
            self.hash_array_2[self.hash_array_2_index].digest())])
        # Show current key
        self.mainwindow.currentKeyEmptyLabel.setText(self.currentKey.hex())
        self.mainwindow.aesEncryptEmpytLabel.setText(self.currentKey[0:16].hex())
        self.mainwindow.aesIVEmptyLabel.setText(self.currentKey[16:32].hex())
        self.mainwindow.shaEmptyLabel.setText(self.currentKey[32:].hex())

    def test_msg(self):
        msg = "Hello World"
        encrypted = self.encrypt(msg)
        decrypted = self.decrypt(encrypted)
        print("Decrypted: ", decrypted)

    def get_signature_str(self, msg):
        mac = hmac.new(self.currentKey[32:], bytes(msg, 'utf-8'), hashlib.sha256).hexdigest()
        return mac

    def get_signature_bytes(self, msg):
        mac = hmac.new(self.currentKey[32:], msg, hashlib.sha256).hexdigest()
        return mac

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
        self.sendEncryptedCommand("rekey")
        self.rekey()

    def rekey(self):
        if(self.serverRunning == True):
            self.textBrowser.append("Rekeying ...")
            self.server.rekey()
        else:
             self.textBrowser.append("Server not running")

    def sendCommandCallback(self):
        text = self.commandPlainTextEdit.toPlainText()
        self.sendEncryptedCommand(text)

    def runServerCallback(self):
        if(not self.serverRunning):
            self.server = Server(self)
            self.serverThread = Thread(target = self.server.run, args =()) 
            self.serverThread.start()
            # ? Check if server started
            self.serverRunning = True
            self.textBrowser.append("Server started")
            self.runServerButton.setStyleSheet("background-color : green")
            self.runServerButton.setText("Server Running")
        else:
            self.textBrowser.append("Server already running")

    def sendEncryptedCommand(self, msg):
        self.textBrowser.append("Sending encrypted message: " + msg)
        if(self.serverRunning):
            self.server.sendData(msg)
        else:
            self.textBrowser.append("Server not running")

    def closeEvent(self, event):
        if(self.serverRunning):
            self.server.terminate()
            self.serverRunning = False
            # TODO (Vatan): Fix assertion error
            self.serverThread._stop()
            # self.serverThread.join()
    
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':         
    main()
