from PyQt5.QtWidgets import QFileDialog, QMessageBox, QAbstractButton, QLabel, QVBoxLayout, QPushButton, QDialog
from PIL import ImageQt
from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage
import numpy as np
import pytesseract
import logging
import qrcode
import cv2
import os


class Ui_CreateQRCode(object):
    def setupUi(self, CreateQRCode):
        CreateQRCode.setObjectName("CreateQRCode")
        CreateQRCode.resize(800, 600)
        CreateQRCode.setStyleSheet("background-color: rgb(208, 208, 208);")
        self.centralwidget = QtWidgets.QWidget(CreateQRCode)
        self.centralwidget.setObjectName("centralwidget")
        self.SelectPhotoButton = QtWidgets.QPushButton(self.centralwidget)
        self.SelectPhotoButton.setGeometry(QtCore.QRect(280, 130, 231, 71))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.SelectPhotoButton.setFont(font)
        self.SelectPhotoButton.setStyleSheet("background-color: rgb(0, 255, 127);")
        self.SelectPhotoButton.setObjectName("SelectPhotoButton")
        self.SelectPhotoButton.clicked.connect(self.openFolderDialog)
        self.GenerateQRCodeButton = QtWidgets.QPushButton(self.centralwidget)
        self.GenerateQRCodeButton.setGeometry(QtCore.QRect(220, 310, 341, 71))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.GenerateQRCodeButton.setFont(font)
        self.GenerateQRCodeButton.setStyleSheet("background-color: rgb(170, 170, 255);")
        self.GenerateQRCodeButton.setObjectName("GenerateQRCodeButton")
        self.GenerateQRCodeButton.clicked.connect(self.generateQRCode)
        self.PhotoNamelineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.PhotoNamelineEdit.setGeometry(QtCore.QRect(280, 230, 231, 31))
        self.PhotoNamelineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.PhotoNamelineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.PhotoNamelineEdit.setObjectName("PhotoNamelineEdit")
        CreateQRCode.setCentralWidget(self.centralwidget)

        self.retranslateUi(CreateQRCode)
        QtCore.QMetaObject.connectSlotsByName(CreateQRCode)

    def retranslateUi(self, CreateQRCode):
        _translate = QtCore.QCoreApplication.translate
        CreateQRCode.setWindowTitle(_translate("CreateQRCode", "Select Photo and Create Barcode"))
        self.SelectPhotoButton.setText(_translate("CreateQRCode", "Select Photo"))
        self.GenerateQRCodeButton.setText(_translate("CreateQRCode", "Generate QR Code"))
        
    def openFolderDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(None, "Select Photo", r"C:\Users\rawli\OneDrive\Music\Pictures\Screenshots", "Images (*.png *.jpg)", options=options)
        if fileName:
            logging.info(fileName)
            self.PhotoNamelineEdit.setText(fileName)  # store the full path

    def generateQRCode(self):
        imagePath = self.PhotoNamelineEdit.text()
        imageText = self.extractTextFromImage(imagePath)
        self.createQRCode(imageText)

    def extractTextFromImage(self, imagePath):
        img = cv2.imread(imagePath)
        if img is None:
            logging.info(f"Could not open or find the image: {imagePath}")
            return ""
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return pytesseract.image_to_string(img)

    def createQRCode(self, text):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(r"C:\Users\rawli\OneDrive\Music\Pictures\qrcode.png")
        logging.info(" image saved successfully")

        # Convert the QR code to an image
        img = qr.make_image(fill='black', back_color='white')
        img.save("qrcode.png")
        logging.info("QR Code created successfully")
        
        # Assuming 'img' is your PIL Image object
        img_rgb = img.convert('RGB')
        logging.info("Image converted to RGB successfully")

        data = np.array(img_rgb)
        logging.info("Image data converted to numpy array successfully")

        # Try a different QImage format
        qimage = QImage(data, data.shape[1], data.shape[0], QImage.Format_RGB32)
        logging.info("QImage created successfully")

        # Convert the QImage to a QPixmap
        try:
            pixmap = QPixmap.fromImage(qimage)
            logging.info("QImage converted to QPixmap successfully")
        except Exception as e:
            logging.info(f"An error occurred while converting QImage to QPixmap: {e}")

        # Check if QPixmap is valid
        if pixmap.isNull():
            logging.info("Pixmap is null")
        else:
            logging.info("Pixmap is not null")            

        # Create a QLabel and set the QPixmap as its pixmap
        label = QLabel()
        label.setPixmap(pixmap)
        logging.info("QLabel set up successfully")

        # Create a layout and add the QLabel to it
        layout = QVBoxLayout()
        layout.addWidget(label)

        # Create a QDialog
        dialog = QDialog()
        dialog.setWindowTitle("QR Code")
        dialog.setLayout(layout)  # Set the layout for the QDialog
        logging.info("QDialog set up successfully")



        # # Create a QMessageBox
        # self.msg = QMessageBox()
        # self.msg.setWindowTitle("QR Code")
        # self.msg.setText("Your QR Code:")
        # self.msg.setInformativeText(label.text())  # Set the QLabel as the informative text
        # self.msg.setIcon(QMessageBox.NoIcon)  # Remove the icon
        # self.msg.setLayout(layout)  # Set the layout for the QMessageBox
        # logging.info("QMessageBox set up successfully")

        # Add an OK button
        button = QPushButton("OK")
        button.clicked.connect(dialog.accept)  # Connect the button's clicked signal to the dialog's accept slot
        layout.addWidget(button)
        logging.info("OK button added successfully")

        try:
            dialog.exec_()
        except Exception as e:
            logging.error(f"An error occurred while executing the dialog: {e}")



        # # # Connect the OK button to the accept slot to close the QMessageBox when clicked
        # # ok_button = self.msg.button(QMessageBox.Ok)
        # # ok_button.clicked.connect(self.msg.accept)
        # # logging.info("OK button connected successfully")

        # # Check if QApplication is running
        # if not QtWidgets.QApplication.instance():
        #     logging.info("No QApplication instance running")
        # else:
        #     logging.info("QApplication instance is running")

        # # Check if this code is being run on the main thread
        # import threading
        # if threading.current_thread() is threading.main_thread():
        #     logging.info("Running on main thread")
        # else:
        #     logging.info("Not running on main thread")

        # # Try executing the QMessageBox
        # try:
        #     self.msg.exec_()
        #     logging.info("QMessageBox executed successfully")
        # except Exception as e:
        #     logging.info(f"An error occurred while executing QMessageBox: {e}")

if __name__ == "__main__":
    import sys
    logging.basicConfig(filename="test.log", level=logging.INFO)
    try:
        logging.info("Starting CreateBarcode application")
        app = QtWidgets.QApplication(sys.argv)
        CreateQRCode = QtWidgets.QMainWindow()
        ui = Ui_CreateQRCode()
        ui.setupUi(CreateQRCode)
        CreateQRCode.show()
        sys.exit(app.exec_())
    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
    finally:
        logging.info("Exiting CreateBarcode application")