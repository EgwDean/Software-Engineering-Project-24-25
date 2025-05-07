from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap

class GraphScreen(QWidget):
    def __init__(self, graph_pixmap):
        super().__init__()
        self.setWindowTitle("Statistics Graph")
        self.setFixedSize(800, 600)

        layout = QVBoxLayout()
        self.graph_label = QLabel(self)
        self.graph_label.setPixmap(graph_pixmap)
        layout.addWidget(self.graph_label)
        
        self.setLayout(layout)
