from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import pyqtSlot, QObject


class MapBridge(QObject):
    def __init__(self, map_widget):
        super().__init__()
        self.map_widget = map_widget

    @pyqtSlot(float, float, str)
    def markerClicked(self, lat, lng, title):
        # Find the pin by lat/lng/title and call its on_click
        for pin in self.map_widget.pins:
            if pin.latitude == lat and pin.longitude == lng and pin.title == title:
                pin.on_click()
                break


class Map(QWebEngineView):
    def __init__(self, latitude=51.505, longitude=-0.09, zoom=13, parent=None):
        super().__init__(parent)
        self.latitude = latitude
        self.longitude = longitude
        self.zoom = zoom
        self.pins = []
        self.bridge = MapBridge(self)
        self.channel = QWebChannel()
        self.channel.registerObject('pyObj', self.bridge)
        self.page().setWebChannel(self.channel)
        self.load_map()

    def load_map(self):
        html = self._generate_map_html(self.latitude, self.longitude, self.zoom, self.pins)
        self.setHtml(html)

    def place(self, pin):
        """Add a pin to the map and reload it."""
        print(f"Placing pin: {pin.title} at ({pin.latitude}, {pin.longitude})")  # Debug
        self.pins.append(pin)
        self.load_map()

    def center_map(self, latitude, longitude):
        """Center the map at the given latitude and longitude."""
        self.latitude = latitude
        self.longitude = longitude
        self.load_map()

    def clear_pins(self):
        """Clear all pins from the map."""
        print("Clearing all pins from the map.")  # Debug
        self.pins = []
        self.load_map()

    def _generate_map_html(self, lat, lng, zoom, pins):
        markers_js = ""
        for i, pin in enumerate(pins):
            markers_js += f"""
                var marker{i} = L.marker([{pin.latitude}, {pin.longitude}]).addTo(map);
                // marker{i}.bindPopup("{pin.title}");
                marker{i}.on('click', function() {{
                    pyObj.markerClicked({pin.latitude}, {pin.longitude}, "{pin.title}");
                }});
            """

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8" />
            <title>Leaflet Map</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>html, body, #map {{ height: 100%; margin: 0; }}</style>
            <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
        </head>
        <body>
            <div id="map"></div>
            <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
            <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
            <script>
                var map = L.map('map').setView([{lat}, {lng}], {zoom});
                L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                    attribution: '© OpenStreetMap contributors'
                }}).addTo(map);

                new QWebChannel(qt.webChannelTransport, function(channel) {{
                    window.pyObj = channel.objects.pyObj;
                }});

                {markers_js}
            </script>
        </body>
        </html>
        """