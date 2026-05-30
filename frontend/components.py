import tkinter as tk
from tkinter import ttk
import tkintermapview


class CapitalSelector(tk.LabelFrame):
    """
    Komponent z przewijaną listą (Scrollbar), zawierający
    checkboxy dla wszystkich 44 stolic europejskich.
    """

    def __init__(self, parent, cities_list, **kwargs):
        super().__init__(parent, text=" Wybierz stolice do analizy ", padx=10, pady=10, **kwargs)

        # Tworzymy płótno (canvas) i scrollbar, aby zmieścić 44 miasta bez rozciągania okna
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0, width=200, height=250)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Słownik, w którym będziemy trzymać stan każdego checkboxa (True/False)
        self.checkbox_vars = {}

        # Automatycznie generujemy checklistę na podstawie bazy danych z backendu
        for city in sorted(cities_list):
            var = tk.BooleanVar(value=False)
            self.checkbox_vars[city] = var
            cb = ttk.Checkbutton(self.scrollable_frame, text=city, variable=var)
            cb.pack(anchor="w", pady=2)

    def get_selected_cities(self):
        """Zwraca listę nazw tylko tych miast, które użytkownik zaznaczył."""
        return [city for city, var in self.checkbox_vars.items() if var.get()]


class LiveMapView(tk.LabelFrame):
    """
    Komponent żywej, interaktywnej mapy OpenStreetMap
    zintegrowany bezpośrednio z oknem Tkintera.
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, text=" Mapa Atrakcyjności Wyjazdów (Live) ", padx=5, pady=5, **kwargs)

        # Inicjalizacja widoku mapy
        self.map_widget = tkintermapview.TkinterMapView(self, corner_radius=0)
        self.map_widget.pack(fill="both", expand=True)

        # Ustawiamy startowy widok na środek Europy i optymalny zoom
        self.map_widget.set_position(52.5200, 13.4050)  # Współrzędne Berlina jako geometryczny środek
        self.map_widget.set_zoom(4)

        # Lista do śledzenia postawionych markerów (pinezek), by móc je łatwo czyścić
        self.markers = []

    def clear_markers(self):
        """Usuwa wszystkie dotychczasowe pinezki z mapy przed nowym zapytaniem."""
        for marker in self.markers:
            marker.delete()
        self.markers.clear()

    def add_city_marker(self, city_name, lat, lon, iaw_score, price, flight):
        """
        Stawia dynamiczny marker na mapie. Kolor i opis zależą
        od wyników zwróconych przez algorytm NumPy.
        """
        # Dobieramy kolor tekstu na podstawie wskaźnika IAW (Optymalizacja wizualna)
        if iaw_score >= 75:
            marker_color = "#2ecc71"  # Zielony (Super cel)
        elif iaw_score >= 45:
            marker_color = "#e67e22"  # Pomarańczowy (Średni)
        else:
            marker_color = "#e74c3c"  # Czerwony (Nieopłacalny/Drogi)

        text_info = f"{city_name}\nIAW: {iaw_score}/100\nHotel śr: {price} PLN\nLot: {flight} PLN"

        # Tworzenie fizycznego markera na obiekcie mapy
        new_marker = self.map_widget.set_marker(
            lat, lon,
            text=text_info,
            marker_color_circle=marker_color,
            text_color=marker_color
        )
        self.markers.append(new_marker)