import plotly.express as px
import plotly.graph_objects as go
import os

class Graph:
    def __init__(self, data):
        self.data = data

    def create_graphs(self):
        html_paths = []

        # 1. Bar plot: Listings by Brand
        html_paths.append(self._bar_plot(index=0, title="Listings by Brand", xlabel="Brand"))

        # 2. Bar plot: Listings by Model
        html_paths.append(self._bar_plot(index=1, title="Listings by Model", xlabel="Model"))

        # 3. Pie chart: Listings by Vehicle Type
        html_paths.append(self._pie_chart(index=2, title="Vehicle Types"))

        # 4. Pie chart: Listings by Status
        html_paths.append(self._pie_chart(index=3, title="Status"))

        return html_paths

    def _bar_plot(self, index, title, xlabel):
        labels = [item[index] for item in self.data]
        counts = [item[4] for item in self.data]

        fig = px.bar(
            x=labels, y=counts, 
            labels={'x': xlabel, 'y': 'Total Listings'},
            title=title
        )
        fig.update_layout(
            xaxis_tickangle=-45,
            plot_bgcolor="white",
            title_font_size=16,
            title_x=0.5
        )

        # Save the plot as an HTML file
        output_path = f"bar_plot_{index}.html"
        fig.write_html(output_path)
        return output_path

    def _pie_chart(self, index, title):
        from collections import defaultdict
        summary = defaultdict(int)
        for row in self.data:
            summary[row[index]] += row[4]

        labels = list(summary.keys())
        sizes = list(summary.values())

        fig = go.Figure(data=[go.Pie(labels=labels, values=sizes, hole=0.3)])
        fig.update_layout(
            title=title,
            title_font_size=16,
            title_x=0.5,
            plot_bgcolor="white"
        )

        # Save the pie chart as an HTML file 
        output_path = f"pie_chart_{index}.html"
        fig.write_html(output_path)
        return output_path
