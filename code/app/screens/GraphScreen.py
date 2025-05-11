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
        self.setFixedSize(1300, 850)  # Μπορείς να το προσαρμόσεις

        # Αποθήκευση των paths των HTML γραφημάτων
        self.graph_html_paths = graph_html_paths  # Αποθήκευση των διαδρομών των HTML αρχείων

        layout = QHBoxLayout()

        # Αριστερή στήλη: Bar plots
        left_column = QVBoxLayout()
        left_column.setAlignment(Qt.AlignTop)  # Χρησιμοποιούμε το Qt για το alignment
        for i in range(2):  # Τα 2 bar plots
            graph_view = QWebEngineView()
            graph_view.load(QUrl.fromLocalFile(os.path.abspath(self.graph_html_paths[i])))
            left_column.addWidget(graph_view)

        # Δεξιά στήλη: Pie charts
        right_column = QVBoxLayout()
        right_column.setAlignment(Qt.AlignTop)  # Χρησιμοποιούμε το Qt για το alignment
        for i in range(2, 4):  # Τα 2 pie charts
            graph_view = QWebEngineView()
            graph_view.load(QUrl.fromLocalFile(os.path.abspath(self.graph_html_paths[i])))
            right_column.addWidget(graph_view)

        layout.addLayout(left_column)
        layout.addLayout(right_column)
        self.setLayout(layout)

    def closeEvent(self, event):
        # Διαγραφή των HTML αρχείων όταν κλείνει το παράθυρο
        for html_file in self.graph_html_paths:
            try:
                # Ελέγχουμε αν το αρχείο υπάρχει και το διαγράφουμε
                file_path = Path(html_file)
                if file_path.exists():
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Error deleting file {html_file}: {e}")

        event.accept()  # Εξασφαλίζουμε ότι το παράθυρο θα κλείσει μετά τη διαγραφή
