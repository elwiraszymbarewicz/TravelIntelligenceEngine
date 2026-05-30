import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import requests
import sys
import os
import re
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.analytics import CITIES_CONFIG
from components import ModernDropdownMultiselect, PremiumMapView

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


class TravelIntelligenceApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Travel Intelligence Engine - Dashboard Menadżerski Pro")
        self.geometry("1250x750")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.left_panel = ctk.CTkFrame(self, width=340, corner_radius=0, fg_color="#ffffff")
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.left_panel.pack_propagate(False)

        lbl_title = ctk.CTkLabel(self.left_panel, text="Travel Engine Pro", font=("Segoe UI", 22, "bold"),
                                 text_color="#2c3e50")
        lbl_title.pack(anchor="w", padx=25, pady=(30, 5))
        lbl_subtitle = ctk.CTkLabel(self.left_panel, text="System Optymalizacji Podróży", font=("Segoe UI", 12),
                                    text_color="#7f8c8d")
        lbl_subtitle.pack(anchor="w", padx=25, pady=(0, 25))

        self.btn_analyze = ctk.CTkButton(
            self.left_panel, text="URUCHOM ANALIZĘ RYNKU",
            font=("Segoe UI", 13, "bold"), height=45, corner_radius=8,
            fg_color="#273746", hover_color="#1c2833",
            command=self.wykonaj_analize
        )
        self.btn_analyze.pack(side="bottom", fill="x", padx=25, pady=30)

        self.form_container = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.form_container.pack(fill="both", expand=True, padx=25)

        ctk.CTkLabel(self.form_container, text="Twój maksymalny budżet (PLN):", font=("Segoe UI", 11, "bold"),
                     text_color="#34495e").pack(anchor="w", pady=(0, 5))
        self.ent_budget = ctk.CTkEntry(self.form_container, placeholder_text="np. 4500", font=("Segoe UI", 12),
                                       height=35)
        self.ent_budget.insert(0, "4500")
        self.ent_budget.pack(fill="x", pady=(0, 15))

        # AKTUALNY PRZEDZIAŁ CZASOWY (OKNO MAX 3 MIESIĘCY OD DZIŚ)
        ctk.CTkLabel(self.form_container, text="Ramy czasowe podróży (YYYY-MM-DD):", font=("Segoe UI", 11, "bold"),
                     text_color="#34495e").pack(anchor="w", pady=(0, 5))

        self.date_frame = ctk.CTkFrame(self.form_container, fg_color="transparent")
        self.date_frame.pack(fill="x", pady=(0, 15))
        self.date_frame.grid_columnconfigure(0, weight=1)
        self.date_frame.grid_columnconfigure(1, weight=1)

        # Dzisiejsza data to 30 maja 2026. Ustawiamy domyślny, bezpieczny, bliski termin (np. 15 czerwca)
        self.ent_arrival = ctk.CTkEntry(self.date_frame, placeholder_text="Od: YYYY-MM-DD", font=("Segoe UI", 11),
                                        height=32)
        self.ent_arrival.insert(0, "2026-06-15")
        self.ent_arrival.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        self.ent_departure = ctk.CTkEntry(self.date_frame, placeholder_text="Do: YYYY-MM-DD", font=("Segoe UI", 11),
                                          height=32)
        self.ent_departure.insert(0, "2026-06-22")
        self.ent_departure.grid(row=0, column=1, padx=(5, 0), sticky="ew")

        ctk.CTkLabel(self.form_container, text="Waga Priorytetu: Budżet", font=("Segoe UI", 11, "bold"),
                     text_color="#34495e").pack(anchor="w", pady=(0, 5))
        self.budget_slider = ctk.CTkSlider(self.form_container, from_=1.0, to=5.0, number_of_steps=8,
                                           button_color="#2980b9", button_hover_color="#3498db")
        self.budget_slider.set(3.0)
        self.budget_slider.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(self.form_container, text="Waga Priorytetu: Komfort", font=("Segoe UI", 11, "bold"),
                     text_color="#34495e").pack(anchor="w", pady=(0, 5))
        self.comfort_slider = ctk.CTkSlider(self.form_container, from_=1.0, to=5.0, number_of_steps=8,
                                            button_color="#2980b9", button_hover_color="#3498db")
        self.comfort_slider.set(3.0)
        self.comfort_slider.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(self.form_container, text="Zakres Geograficzny Analizy", font=("Segoe UI", 11, "bold"),
                     text_color="#34495e").pack(anchor="w", pady=(0, 5))
        self.selector = ModernDropdownMultiselect(self.form_container, list(CITIES_CONFIG.keys()))
        self.selector.pack(fill="x", pady=(0, 15))
        self.selector.btn_toggle.configure(command=self.bezpieczny_toggle_listy)

        self.verdict_frame = ctk.CTkFrame(self.form_container, fg_color="#f8f9fa", border_width=1,
                                          border_color="#e2e8f0", corner_radius=8)
        self.verdict_frame.pack(fill="x", pady=(10, 0), ipady=15)

        self.lbl_verdict_title = ctk.CTkLabel(self.verdict_frame, text="Rekomendacja Systemowa",
                                              font=("Segoe UI", 11, "bold"), text_color="#7f8c8d")
        self.lbl_verdict_title.pack(anchor="w", padx=15, pady=(10, 2))

        self.lbl_verdict_val = ctk.CTkLabel(self.verdict_frame, text="Oczekiwanie na analizę...",
                                            font=("Segoe UI", 13, "italic"), text_color="#94a3b8")
        self.lbl_verdict_val.pack(anchor="w", padx=15)

        self.map_view = PremiumMapView(self)
        self.map_view.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def bezpieczny_toggle_listy(self):
        self.selector.toggle_dropdown()
        if self.selector.is_open:
            self.verdict_frame.pack_forget()
        else:
            self.verdict_frame.pack(fill="x", pady=(10, 0), ipady=15)

    def wykonaj_analize(self):
        if self.selector.is_open:
            self.bezpieczny_toggle_listy()

        wybrane_miasta = self.selector.get_selected_cities()
        if not wybrane_miasta:
            messagebox.showwarning("Brak danych", "Zaznacz przynajmniej jedną stolicę z rozwijanej listy!")
            return

        try:
            user_budget = float(self.ent_budget.get())
            if user_budget <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Błędny budżet", "Wpisz poprawną kwotę maksymalnego budżetu (np. 5000)!")
            return

        date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
        arrival_str = self.ent_arrival.get().strip()
        departure_str = self.ent_departure.get().strip()

        if not date_pattern.match(arrival_str) or not date_pattern.match(departure_str):
            messagebox.showerror("Zły format daty", "Daty muszą być wpisane w formacie YYYY-MM-DD (np. 2026-06-15)!")
            return

        # --- WALIDACJA OKNA 3 MIESIĘCY OD DZIŚ (PRODUKCYJNY STANDARD RESTRYKCJI) ---
        try:
            arrival_date = datetime.strptime(arrival_str, "%Y-%m-%d")
            departure_date = datetime.strptime(departure_str, "%Y-%m-%d")
            today = datetime.now()
            max_future_date = today + timedelta(days=90)

            if arrival_date.date() < today.date():
                messagebox.showerror("Niedozwolona data przeszła",
                                     "System Booking.com nie obsługuje wyszukiwania wstecz. Wybierz aktualne ramy czasowe!")
                return

            if arrival_date > max_future_date or departure_date > max_future_date:
                messagebox.showerror(
                    "Przekroczono limit okna czasowego",
                    "Aplikacja ogranicza zakres wyszukiwania do maksymalnie 3 miesięcy od dziś.\n\n"
                    "Wybierz daty mieszczące się w okresie do końca sierpnia 2026 roku!"
                )
                return

            if arrival_date > departure_date:
                messagebox.showerror("Błąd logiczny",
                                     "Data rozpoczęcia podróży nie może być późniejsza niż data powrotu!")
                return
        except ValueError:
            messagebox.showerror("Błąd", "Niepoprawna struktura daty. Sprawdź kalendarz!")
            return

        payload = {
            "cities": wybrane_miasta,
            "arrival_date": arrival_str,
            "departure_date": departure_str,
            "budget_weight": round(float(self.budget_slider.get()), 1),
            "comfort_weight": round(float(self.comfort_slider.get()), 1),
            "user_budget": user_budget
        }

        self.map_view.clear_markers()
        self.lbl_verdict_val.configure(text="Obliczanie danych...", text_color="#e67e22", font=("Segoe UI", 13, "bold"))
        self.update_idletasks()

        try:
            response = requests.post("http://127.0.0.1:8000/api/analiza", json=payload, timeout=60)

            if response.status_code == 200:
                json_res = response.json()
                data_dict = json_res.get("data", {})

                if not data_dict:
                    self.lbl_verdict_val.configure(text="Brak wolnych miejsc", text_color="#7f8c8d")
                    messagebox.showinfo("Brak ofert",
                                        "W wybranym terminie hotele w wybranych miastach nie posiadają wolnych pokoi.")
                    return

                best_city = None
                max_score = -1.0

                for city, metrics in data_dict.items():
                    if metrics["iaw_score"] > max_score:
                        max_score = metrics["iaw_score"]
                        best_city = city

                for city, metrics in data_dict.items():
                    lat, lon = metrics["coords"]
                    is_best = (city == best_city)

                    self.map_view.add_city_marker(
                        city_name=city,
                        lat=lat,
                        lon=lon,
                        iaw_score=metrics["iaw_score"],
                        price=metrics["mean_hotel_price"],
                        flight=metrics["min_flight_price"],
                        is_best=is_best
                    )

                zwyciezca_metrics = data_dict[best_city]
                laczny_koszt = zwyciezca_metrics["mean_hotel_price"] + zwyciezca_metrics["min_flight_price"]

                if laczny_koszt > user_budget:
                    brakujaca_kwota = int(laczny_koszt - user_budget)
                    self.lbl_verdict_val.configure(
                        text=f"🥇 {best_city} ({max_score}/100 pkt)\n⚠️ Przekracza budżet o {brakujaca_kwota} PLN!",
                        text_color="#e74c3c", font=("Segoe UI", 13, "bold")
                    )
                else:
                    self.lbl_verdict_val.configure(
                        text=f"🥇 {best_city} ({max_score}/100 pkt)\nKoszt: {int(laczny_koszt)} PLN (W budżecie)",
                        text_color="#2980b9", font=("Segoe UI", 13, "bold")
                    )

                messagebox.showinfo("Sukces", f"Analiza ukończona! Najlepszy cel podróży: {best_city}")
            else:
                messagebox.showerror("Błąd serwera", f"API zwróciło kod błędu: {response.status_code}")
                self.lbl_verdict_val.configure(text="Błąd analizy", text_color="#e74c3c")

        except requests.exceptions.Timeout:
            messagebox.showwarning("Timeout", "Serwer potrzebuje więcej czasu.")
            self.lbl_verdict_val.configure(text="Przekroczono czas", text_color="#e74c3c")
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Błąd", "Brak połączenia z backend/main.py!")
            self.lbl_verdict_val.configure(text="Brak połączenia", text_color="#e74c3c")


if __name__ == "__main__":
    app = TravelIntelligenceApp()
    app.mainloop()