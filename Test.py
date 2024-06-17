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
import pandas as pd


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

    # Set the tesseract path in the script before calling image_to_string
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path


    def openFolderDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(None, "Select Photo", r"C:\Users\rawli\OneDrive\Music\Pictures\Screenshots", "Images (*.png *.jpg)", options=options)
        if fileName:
            logging.info(fileName)
            self.PhotoNamelineEdit.setText(fileName)  # store the full path

            # Open the image file
            img = Image.open(fileName)

            # Use Tesseract to do OCR on the image
            text = pytesseract.image_to_string(img)

            # Split the text into lines
            lines = text.split('\n')

            # Create a DataFrame with the lines
            df = pd.DataFrame(lines, columns=['Text'])

            # Remove blank rows
            df = df[df['Text'].str.strip() != '']

            # Add a new column with the first word from each line
            df['NewColumn'] = df['Text'].apply(lambda x: x.split()[0] if x.split() else '')

            # Write the text to an Excel file
            df.to_excel(r'C:\Users\rawli\OneDrive\Documents\Groceries\Test1.xlsx', index=False, header=False)  # Write the DataFrame to an Excel file












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