from PyQt5.QtWebEngineWidgets import QWebEngineView


class MapWidget(QWebEngineView):
    def __init__(self, latitude=51.505, longitude=-0.09, zoom=13, parent=None):
        super().__init__(parent)
        self.latitude = latitude
        self.longitude = longitude
        self.zoom = zoom
        self.pins = []
        self.load_map()

    def load_map(self):
        html = self._generate_map_html(self.latitude, self.longitude, self.zoom, self.pins)
        self.setHtml(html)

    def place(self, pin):
        self.pins.append(pin)
        self.load_map()

    def _generate_map_html(self, lat, lng, zoom, pins):
        markers_js = ""
        for i, pin in enumerate(pins):
            markers_js += f"""
                var marker{i} = L.marker([{pin.latitude}, {pin.longitude}]).addTo(map);
                marker{i}.bindPopup("{pin.title}");
                marker{i}.on('click', function() {{
                    console.log("Marker clicked: {pin.title}");
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
            <script>
                var map = L.map('map').setView([{lat}, {lng}], {zoom});
                L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                    attribution: '© OpenStreetMap contributors'
                }}).addTo(map);

                {markers_js}
            </script>
        </body>
        </html>
        """
