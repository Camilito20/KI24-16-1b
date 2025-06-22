from PyQt5.QtWidgets import QFileDialog, QLabel, QPushButton, QVBoxLayout, QWidget, QApplication, QMainWindow
from PyQt5.QtGui import QPixmap  # ¡Falta esta importación!
import sys

class ImageSelectorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Selector de imágenes")
        self.setGeometry(400, 400, 900, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        self.label_imagen = QLabel()
        self.label_imagen.setFixedSize(500, 300)  # Tamaño fijo para el área de la imagen

        button = QPushButton("Abrir imagen")
        button.clicked.connect(self.open_image)

        layout.addWidget(self.label_imagen)
        layout.addWidget(button)
        central_widget.setLayout(layout)

    def open_image(self):
        # Abrir diálogo para seleccionar archivo
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Abrir imagen", "", "Image files (*.jpg *.png *.bmp)"
        )
        if file_name:
            pixmap = QPixmap(file_name).scaled(
                300, 200, aspectRatioMode=1
            )
            self.label_imagen.setPixmap(pixmap)

app = QApplication(sys.argv)
window = ImageSelectorWindow()
window.show()
sys.exit(app.exec_())