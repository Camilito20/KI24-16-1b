from PyQt5.QtWidgets import QFileDialog, QLabel, QPushButton, QVBoxLayout, QWidget, QApplication, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

import sys

class ImageSelectorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Selector de imágenes")
        self.setGeometry(400, 100, 1080, 768)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        self.label_imagen = QLabel()
        self.label_imagen.setAlignment(Qt.AlignCenter)
        self.label_imagen.setFixedSize(1080, 768)  # Tamaño fijo para el área de la imagen
        self.button = QPushButton("Abrir imagen")
        self.boton = QPushButton("Cambiar imagen")
        self.boton.setVisible(False)
        self.button.clicked.connect(self.open_image)
        self.boton.clicked.connect(self.open_image)

        layout.addStretch()
        layout.addWidget(self.label_imagen)
        layout.addStretch()
        layout.addWidget(self.button)
        layout.addWidget(self.boton)
        central_widget.setLayout(layout)

    def open_image(self):
        # Abrir diálogo para seleccionar archivo
        self.button.setVisible(False)
        self.boton.setVisible(True)
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Abrir imagen", "", "Image files (*.jpg *.png *.bmp)"
        )
        if file_name:
            pixmap = QPixmap(file_name).scaled(
                1080, 768, aspectRatioMode=1
            )
            self.label_imagen.setPixmap(pixmap)
        
   

app = QApplication(sys.argv)
window = ImageSelectorWindow()
window.show()
sys.exit(app.exec_())