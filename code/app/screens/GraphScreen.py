import os
from pathlib import Path
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QDialog, QMessageBox

class GraphScreen(QWidget):
    def __init__(self, graph_html_paths):
        super().__init__()
        self.setWindowTitle("Statistics Graphs")
        self.setFixedSize(1300, 850)  

        # Set the stylesheet for the widget
        self.graph_html_paths = graph_html_paths  

        layout = QHBoxLayout()

        # Bar plots on the left
        left_column = QVBoxLayout()
        left_column.setAlignment(Qt.AlignTop)  
        for i in range(2):  # first 2 bar plots
            graph_view = QWebEngineView()
            graph_view.load(QUrl.fromLocalFile(os.path.abspath(self.graph_html_paths[i])))
            left_column.addWidget(graph_view)

        # Pie charts
        right_column = QVBoxLayout()
        right_column.setAlignment(Qt.AlignTop) 
        for i in range(2, 4):  # last 2 pie charts
            graph_view = QWebEngineView()
            graph_view.load(QUrl.fromLocalFile(os.path.abspath(self.graph_html_paths[i])))
            right_column.addWidget(graph_view)

        layout.addLayout(left_column)
        layout.addLayout(right_column)
        self.setLayout(layout)

    def closeEvent(self, event):
        # delete the HTML files when closing the window
        for html_file in self.graph_html_paths:
            try:
                # Check if the file exists before trying to delete it
                file_path = Path(html_file)
                if file_path.exists():
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Error deleting file {html_file}: {e}")

        event.accept()  # Accept the event to close the window
