import tkinter as tk
from tkinter import ttk, messagebox
import requests
import sys
import os

# Poprawka ścieżki, aby Python widział pliki z folderu backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.analytics import CITIES_CONFIG
from components import CapitalSelector, LiveMapView


class TravelIntelligenceApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Travel Intelligence Engine - Panel Menadżerski")
        self.geometry("1100x650")
        self.minimum_size_width = 1100
        self.minimum_size_height = 650

        # Stylizacja interfejsu (Clam dla nowoczesnego wyglądu systemowego)
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # --- UKŁAD OKNA (Główny Grid) ---
        # Lewy panel sterowania (szerokość stała), prawy panel z mapą (elastyczny)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 1. LEWY PANEL (FORMULARZ)
        self.left_panel = ttk.Frame(self, padding=15)
        self.left_panel.grid(row=0, column=0, sticky="nsew")

        # Suwak: Waga Budżetu
        ttk.Label(self.left_panel, text="Priorytet Niskich Kosztów (Budżet):", font=("Arial", 10, "bold")).pack(
            anchor="w", pady=(0, 2))
        self.budget_slider = tk.Scale(self.left_panel, from_=1.0, to=5.0, resolution=0.5, orient="horizontal",
                                      fg="#2c3e50")
        self.budget_slider.set(3.0)
        self.budget_slider.pack(fill="x", pady=(0, 15))

        # Suwak: Waga Komfortu
        ttk.Label(self.left_panel, text="Priorytet Standardu (Komfort):", font=("Arial", 10, "bold")).pack(anchor="w",
                                                                                                           pady=(0, 2))
        self.comfort_slider = tk.Scale(self.left_panel, from_=1.0, to=5.0, resolution=0.5, orient="horizontal",
                                       fg="#2c3e50")
        self.comfort_slider.set(3.0)
        self.comfort_slider.pack(fill="x", pady=(0, 15))

        # Komponent wyboru miast (zaciąga klucze z CITIES_CONFIG)
        self.selector = CapitalSelector(self.left_panel, list(CITIES_CONFIG.keys()))
        self.selector.pack(fill="both", expand=True, pady=(0, 15))

        # Przycisk uruchomienia analizy rynkowej
        self.btn_analyze = ttk.Button(self.left_panel, text="URUCHOM ANALIZĘ", command=self.wykonaj_analize)
        self.btn_analyze.pack(fill="x", ipady=10)

        # 2. PRAWY PANEL (ŻYWA MAPA)
        self.map_view = LiveMapView(self)
        self.map_view.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    def wykonaj_analize(self):
        """Pobiera parametry z GUI, odpytuje lokalne API i nanosi wyniki na mapę."""
        wybrane_miasta = self.selector.get_selected_cities()

        if not wybrane_miasta:
            messagebox.showwarning("Brak danych", "Zaznacz przynajmniej jedną stolicę z listy!")
            return

        # Przygotowanie paczki JSON dla serwera FastAPI
        # Terminy ustawione sztywno na wrzesień 2026 (zgodnie z planem wakacyjnym)
        payload = {
            "cities": wybrane_miasta,
            "arrival_date": "2026-09-03",
            "departure_date": "2026-09-13",
            "budget_weight": float(self.budget_slider.get()),
            "comfort_weight": float(self.comfort_slider.get())
        }

        # Czyszczenie starych pinezek przed rysowaniem nowych
        self.map_view.clear_markers()

        try:
            # Wysyłamy żądanie POST do działającego w tle backendu na localhoście
            response = requests.post("http://127.0.0.1:8000/api/analiza", json=payload, timeout=15)

            if response.status_code == 200:
                json_res = response.json()
                data_dict = json_res.get("data", {})

                # Iterujemy po miastach, które przysłał nam serwer
                for city, metrics in data_dict.items():
                    lat, lon = metrics["coords"]

                    # Dodanie dynamicznej pinezki na mapie OpenStreetMap
                    self.map_view.add_city_marker(
                        city_name=city,
                        lat=lat,
                        lon=lon,
                        iaw_score=metrics["iaw_score"],
                        price=metrics["mean_hotel_price"],
                        flight=metrics["min_flight_price"]
                    )

                messagebox.showinfo("Sukces", f"Analiza ukończona! Przetworzono miast: {len(data_dict)}")
            else:
                messagebox.onerror("Błąd serwera", f"API zwróciło kod błędu: {response.status_code}")

        except requests.exceptions.ConnectionError:
            messagebox.showerror("Błąd komunikacji",
                                 "Nie można połączyć się z backendem!\nUpewnij się, że plik backend/main.py jest uruchomiony.")


if __name__ == "__main__":
    app = TravelIntelligenceApp()
    app.mainloop()