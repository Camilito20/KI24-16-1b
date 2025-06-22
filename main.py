from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QFileDialog
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QRect

import sys

class ImageSelectorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Practis")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        #subir imagen
        self.button = QPushButton("Abrir imagen")
        self.button.clicked.connect(self.open_image)
        layout.addWidget(self.button)

        #Cambiar imagen que ya esta colocada
        self.boton = QPushButton("Cambiar imagen")
        self.boton.setVisible(False)
        self.boton.clicked.connect(self.open_image)
        layout.addWidget(self.boton)

        #Mostrar imagen
        self.label_imagen = QLabel()
        self.label_imagen.setAlignment(Qt.AlignCenter)
        self.label_imagen.setStyleSheet("border: 1px soild black")  # Tamaño fijo para el área de la imagen
        layout.addWidget(self.label_imagen)

        cordenadas_Layout = QHBoxLayout()
        self.edit_x = QLineEdit(placeholderText="X")
        self.edit_y = QLineEdit(placeholderText="Y")
        self.edit_ancho = QLineEdit(placeholderText="Ancho")
        self.edit_Alto = QLineEdit(placeholderText="Alto")

        for edit in [self.edit_x, self.edit_y, self.edit_ancho, self.edit_Alto]:
            edit.setMaximumWidth(100)
            cordenadas_Layout.addWidget(edit)

        self.Corte_imagen = QPushButton("Cortar la imagen")
        self.Corte_imagen.clicked.connect(self.cut_image)
        cordenadas_Layout.addWidget(self.Corte_imagen)

        layout.addLayout(cordenadas_Layout)
        central_widget.setLayout(layout)

        self.original_pixmap = None

    def open_image(self):
        # Abrir diálogo para seleccionar archivo
        self.button.setVisible(False)
        self.boton.setVisible(True)

        file_name, _ = QFileDialog.getOpenFileName(
            self, "Abrir imagen", "", "Image files (*.jpg *.png *.bmp)"
        )
        if file_name:
            self.original_pixmap = QPixmap(file_name)
            self.label_imagen.setPixmap(self.original_pixmap)

    def display_imagen(self, pixmap):
        scaled_pixmap = pixmap.scaled(
            self.label_imagen.width() -10,
            self.label_imagen.height() -10,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.label_imagen.setPixmap(scaled_pixmap)

    def cut_image(self):
        if not self.open_image:
            return
        
        try:
            x = int(self.edit_x.text())
            y = int(self.edit_y.text())
            Ancho = int(self.edit_ancho.text())
            Alto = int(self.edit_Alto.text())

            if (x < 0 or y < 0 or 
                Ancho <= 0 or Alto <= 0 or
                x + Ancho > self.original_pixmap.width() or
                y + Alto > self.original_pixmap.height()):
                raise ValueError("Coordenadas fuera de rango")

            corte_hecho = self.original_pixmap.copy(x, y, Ancho, Alto)
            self.display_imagen(corte_hecho)

        except ValueError as e:
            print(f"Error: {e}. Ingresa valores numéricos válidos.")
    
        

app = QApplication(sys.argv)
window = ImageSelectorWindow()
window.show()
sys.exit(app.exec_())