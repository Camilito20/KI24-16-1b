from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QFileDialog, QSlider, QSpinBox
)
from PyQt5.QtGui import QPixmap, QIntValidator, QColor, QImage, QPainter, QPen
from PyQt5.QtCore import Qt, QPoint

import sys

class ImageEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Practis - Editor Avanzado")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Botones para imagen
        self.button = QPushButton("Abrir imagen")
        self.button.clicked.connect(self.open_image)
        layout.addWidget(self.button)

        self.boton = QPushButton("Cambiar imagen")
        self.boton.setVisible(False)
        self.boton.clicked.connect(self.open_image)
        layout.addWidget(self.boton)

        # Mostrar imagen
        self.label_imagen = QLabel()
        self.label_imagen.setAlignment(Qt.AlignCenter)
        self.label_imagen.setStyleSheet("border: 1px solid black")
        layout.addWidget(self.label_imagen)

        # Controles para dibujar línea
        line_layout = QHBoxLayout()
        
        self.line_x1 = QLineEdit(placeholderText="x1")
        self.line_y1 = QLineEdit(placeholderText="y1")
        self.line_x2 = QLineEdit(placeholderText="x2")
        self.line_y2 = QLineEdit(placeholderText="y2")
        self.line_width = QLineEdit(placeholderText="Grosor")
        
        for edit in [self.line_x1, self.line_y1, self.line_x2, self.line_y2, self.line_width]:
            edit.setMaximumWidth(70)
            line_layout.addWidget(edit)
        
        self.draw_button = QPushButton("Dibujar Línea")
        self.draw_button.clicked.connect(self.draw_line)
        line_layout.addWidget(self.draw_button)
        
        layout.addLayout(line_layout)

        # Controles de brillo
        brillo_layout = QHBoxLayout()
        self.Brillo_imput = QLineEdit()
        self.Brillo_imput.setValidator(QIntValidator(-100, 100))
        self.Brillo_imput.setPlaceholderText("Ingrese valor de brillo (-100 a 100)")
        self.Brillo_imput.setAlignment(Qt.AlignCenter)
        self.boton_brillo = QPushButton("Aplicar brillo")
        self.boton_brillo.clicked.connect(self.apply_brightness)
        
        brillo_layout.addWidget(self.Brillo_imput)
        brillo_layout.addWidget(self.boton_brillo)
        layout.addLayout(brillo_layout)

        # Coordenadas de corte
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
        self.current_pixmap = None
        self.original_image = None  # Para guardar la QImage original

    def open_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Abrir imagen", "", "Image files (*.jpg *.png *.bmp)"
        )
        if file_name:
            self.button.setVisible(False)
            self.boton.setVisible(True)
            
            self.original_pixmap = QPixmap(file_name)
            self.current_pixmap = self.original_pixmap.copy()
            self.original_image = QImage(file_name)  # Guardamos la QImage para procesamiento
            self.display_image()

    def display_image(self):
        if self.current_pixmap:
            scaled_pixmap = self.current_pixmap.scaled(
                self.label_imagen.width() - 10,
                self.label_imagen.height() - 10,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.label_imagen.setPixmap(scaled_pixmap)

    def draw_line(self):
        if not self.current_pixmap:
            return
            
        try:
            # Obtener coordenadas y grosor
            x1 = int(self.line_x1.text())
            y1 = int(self.line_y1.text())
            x2 = int(self.line_x2.text())
            y2 = int(self.line_y2.text())
            width = int(self.line_width.text())
            
            # Validar valores
            if width <= 0:
                raise ValueError("El grosor debe ser positivo")
                
            # Crear una copia de la imagen original para dibujar
            temp_pixmap = self.original_pixmap.copy()
            
            # Dibujar la línea
            painter = QPainter(temp_pixmap)
            pen = QPen(QColor(0, 255, 0))  # Lápiz verde
            pen.setWidth(width)
            painter.setPen(pen)
            painter.drawLine(QPoint(x1, y1), QPoint(x2, y2))
            painter.end()
            
            # Actualizar la imagen actual
            self.current_pixmap = temp_pixmap
            self.display_image()
            
        except ValueError as e:
            print(f"Error: {e}. Ingresa valores numéricos válidos.")

    def apply_brightness(self):
        if not self.original_image or not self.Brillo_imput.text():
            return
            
        try:
            value = int(self.Brillo_imput.text())
        except ValueError:
            return
            
        # Asegurarnos que el valor está en el rango permitido
        value = max(-100, min(100, value))
        
        # Factor de brillo (0.0 a 2.0, donde 1.0 es normal)
        factor = 1.0 + value / 100.0
        
        # Crear una copia de la imagen original para trabajar
        modified_image = self.original_image.copy()
        
        # Aplicar ajuste de brillo a cada píxel
        for y in range(modified_image.height()):
            for x in range(modified_image.width()):
                color = modified_image.pixelColor(x, y)
                
                # Ajustar cada componente de color
                r = min(255, int(color.red() * factor))
                g = min(255, int(color.green() * factor))
                b = min(255, int(color.blue() * factor))
                
                # Mantener el mismo alpha
                a = color.alpha()
                
                # Establecer el nuevo color
                modified_image.setPixelColor(x, y, QColor(r, g, b, a))
        
        # Convertir QImage a QPixmap para mostrar
        self.current_pixmap = QPixmap.fromImage(modified_image)
        self.display_image()

    def cut_image(self):
        if not self.current_pixmap:
            return
        
        try:
            x = int(self.edit_x.text())
            y = int(self.edit_y.text())
            Ancho = int(self.edit_ancho.text())
            Alto = int(self.edit_Alto.text())

            if (x < 0 or y < 0 or 
                Ancho <= 0 or Alto <= 0 or
                x + Ancho > self.current_pixmap.width() or
                y + Alto > self.current_pixmap.height()):
                raise ValueError("Coordenadas fuera de rango")

            corte_hecho = self.current_pixmap.copy(x, y, Ancho, Alto)
            self.current_pixmap = corte_hecho
            self.display_image()

        except ValueError as e:
            print(f"Error: {e}. Ingresa valores numéricos válidos.")

    def resizeEvent(self, event):
        self.display_image()
        super().resizeEvent(event)

app = QApplication(sys.argv)
window = ImageEditorWindow()
window.show()
sys.exit(app.exec_())