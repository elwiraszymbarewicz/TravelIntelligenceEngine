import tkinter as tk
import customtkinter as ctk
import tkintermapview


class ModernDropdownMultiselect(ctk.CTkFrame):
    def __init__(self, parent, cities_list, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)

        self.cities_list = sorted(cities_list)
        self.checkbox_vars = {}
        self.is_open = False

        self.btn_toggle = ctk.CTkButton(
            self, text="Wybierz stolice... ▼",
            font=("Segoe UI", 12, "bold"),
            fg_color="#34495e", hover_color="#2c3e50",
            command=self.toggle_dropdown, height=38
        )
        self.btn_toggle.pack(fill="x")

        self.list_frame = ctk.CTkScrollableFrame(
            self, height=220, fg_color="#ffffff",
            border_width=1, border_color="#bdc3c7"
        )

        for city in self.cities_list:
            self.checkbox_vars[city] = tk.BooleanVar(value=False)
            self.checkbox_vars[city].trace_add("write", lambda *args: self.update_button_text())

            cb = ctk.CTkCheckBox(
                self.list_frame, text=city, variable=self.checkbox_vars[city],
                font=("Segoe UI", 11), text_color="#2c3e50",
                hover_color="#3498db", corner_radius=4
            )
            cb.pack(fill="x", anchor="w", pady=4, padx=5)

    def update_button_text(self):
        selected = self.get_selected_cities()
        if not selected:
            suffix = " ▲" if self.is_open else " ▼"
            self.btn_toggle.configure(text="Wybierz stolice..." + suffix)
            return

        if len(selected) <= 3:
            button_text = ", ".join(selected)
        else:
            button_text = f"{selected[0]}, {selected[1]}, {selected[2]} + {len(selected) - 3}"

        suffix = " ▲" if self.is_open else " ▼"
        self.btn_toggle.configure(text=button_text + suffix)

    def toggle_dropdown(self):
        if self.is_open:
            self.list_frame.pack_forget()
            self.is_open = False
        else:
            self.list_frame.pack(fill="x", pady=(5, 0))
            self.is_open = True
        self.update_button_text()

    def close_dropdown(self):
        if self.is_open:
            self.toggle_dropdown()

    def get_selected_cities(self):
        return [city for city in self.cities_list if self.checkbox_vars[city].get()]


class PremiumMapView(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, corner_radius=15, **kwargs)

        self.map_widget = tkintermapview.TkinterMapView(self, corner_radius=15)
        self.map_widget.pack(fill="both", expand=True, padx=2, pady=2)
        self.map_widget.set_tile_server("https://a.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png")
        self.map_widget.set_position(53.0000, 18.0000)
        self.map_widget.set_zoom(5)
        self.markers = []

    def clear_markers(self):
        for marker in self.markers:
            marker.delete()
        self.markers.clear()

    def on_marker_click(self, marker):
        tk.messagebox.showinfo("Raport Rynkowy", marker.data)

    def add_city_marker(self, city_name, lat, lon, iaw_score, price, flight, is_best=False):
        prefix = "🏆 REKOMENDACJA SYSTEMOWA 🏆\n" if is_best else ""
        info_text = (
            f"{prefix}"
            f"Kierunek: {city_name}\n"
            f"───────────────────\n"
            f"★ Wskaźnik IAW: {iaw_score}/100\n"
            f"✈ Średnia cena lotu: {int(flight)} PLN\n"
            f"🏨 Średni koszt hotelu: {int(price)} PLN"
        )

        if is_best:
            new_marker = self.map_widget.set_marker(
                lat, lon, marker_color_circle="#ffffff", marker_color_outside="#2980b9", command=self.on_marker_click
            )
        else:
            if iaw_score >= 75:
                marker_color = "#2ecc71"
            elif iaw_score >= 45:
                marker_color = "#f39c12"
            else:
                marker_color = "#e74c3c"

            new_marker = self.map_widget.set_marker(
                lat, lon, marker_color_circle="#ffffff", marker_color_outside=marker_color, command=self.on_marker_click
            )

        new_marker.data = info_text
        self.markers.append(new_marker)