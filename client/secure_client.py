import sys
from PyQt5 import QtWidgets, uic
import socket
from threading import Thread 
from MainWindow import Ui_MainWindow
from Crypto.Hash import SHA512
from Crypto.Cipher import AES
import random
import pyprimes
import hashlib
import hmac
import base64
import hashlib
from Crypto.Cipher import AES

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

        self.array_length = 500
        self.hash_array_1 = [0] * (self.array_length+1)
        self.hash_array_2 = [0] * (self.array_length+1)
        self.hash_array_1_index = 0
        self.hash_array_2_index = self.array_length

        self.generateInitialKey()

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
                # msg = self.decrypt(data.decode("utf-8"))
                print(data)
                msg = self.decrypt(data)
                self.textBrowser.append("Message received from server: " + msg)
                if msg == "rekey":
                    self.mainwindow.rekey()
            except:
                pass

    def sendData(self, msg):
        if(self.isConnected):
            # self.sock.sendall(str.encode(self.encrypt(msg), "utf-8"))
            self.sock.sendall(self.encrypt(msg))

    def terminate(self):
        self.isConnected = False

    def encrypt(self, msg):
        aes = AESCipher(self.currentKey)
        encrypted = aes.encrypt(msg)
        return encrypted
    
    def decrypt(self, msg):
        aes = AESCipher(self.currentKey)
        decrypted = aes.decrypt(msg)
        return decrypted

    def generateInitialKey(self):
        # Generate seed
        seed1, seed2 = 1, 7 # self.random_prime()
        # Seeds to bytes
        seed_bytes_1 = bytes(str(seed1), 'ascii') # int.to_bytes(seed1)
        seed_bytes_2 = bytes(str(seed2), 'ascii') # int.to_bytes(seed2)
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
        print(self.currentKey.hex())
        

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

    def random_prime(self):
        chck = False
        chck2 = False
        chck_equal = True
        while chck == False and chck2 == False and chck_equal == True:
            p = random.randrange(2 ** (127), 2 ** 128 - 1)
            p2 = random.randrange(2 ** (127), 2 ** 128 - 1)
            chck = pyprimes.isprime(p)
            chck2 = pyprimes.isprime(p2)
            if p == p2:
                chck_equal = True
            else:
                chck_equal = False
        return p, p2

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
        if(self.isClientUp):
            self.textBrowser.append("Rekeying ...")
            self.client.rekey()
        else:
            self.textBrowser.append("Client not running")

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
