from PyQt5.QtWidgets import QWidget

class DetailsScreen(QWidget):
    def __init__(self, listing_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Details for Listing {listing_id}")
        self.setMinimumSize(200, 100)
        # Empty window for now