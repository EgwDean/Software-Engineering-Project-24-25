import sys
import os

# find screens
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import matplotlib.pyplot as plt
from io import BytesIO
from PyQt5.QtGui import QImage, QPixmap
from screens.GraphScreen import GraphScreen


class Graph:
    def __init__(self, data):
        self.data = data  # data is a list of tuples (e.g., brand, count)
    
    def create_graph(self):
        brands = [item[0] for item in self.data]
        counts = [item[4] for item in self.data]  # Assuming the 'Total Listings' is at index 4
        
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(brands, counts, color='skyblue')
        ax.set_xlabel('Brands')
        ax.set_ylabel('Total Listings')
        ax.set_title('Listings by Brand')

        # Save the plot to a QPixmap
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img = QImage()
        img.loadFromData(buf.read())
        pixmap = QPixmap(img)
        plt.close(fig)  # Close the plot to free resources

        return pixmap
