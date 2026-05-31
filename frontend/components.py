import tkinter as tk
import customtkinter as ctk
import tkintermapview
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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


class MarketReportPopup(ctk.CTkToplevel):
    def __init__(self, parent, title_text, info_text, hotel_price, flight_price):
        super().__init__(parent)

        self.title(title_text)
        self.geometry("460x420")
        self.resizable(False, False)
        self.configure(fg_color="#f8f9fa")

        self.transient(parent)
        self.grab_set()

        self.update_idletasks()
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        popup_width = 460
        popup_height = 420

        center_x = parent_x + (parent_width // 2) - (popup_width // 2)
        center_y = parent_y + (parent_height // 2) - (popup_height // 2)
        self.geometry(f"{popup_width}x{popup_height}+{center_x}+{center_y}")

        lbl_info = ctk.CTkLabel(
            self, text=info_text, font=("Segoe UI", 12),
            justify="left", text_color="#2c3e50"
        )
        lbl_info.pack(padx=25, pady=(20, 10), anchor="w")

        chart_frame = ctk.CTkFrame(self, fg_color="transparent")
        chart_frame.pack(fill="both", expand=True, padx=25, pady=(0, 15))

        fig = Figure(figsize=(4, 2), dpi=100, facecolor="#f8f9fa")
        ax = fig.add_subplot(111)

        labels = ['Hotel', 'Lot']
        sizes = [hotel_price, flight_price]
        colors = ['#2980b9', '#e67e22']

        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90,
               textprops={'fontsize': 9, 'fontname': 'Segoe UI', 'weight': 'bold'})
        ax.axis('equal')
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        btn_close = ctk.CTkButton(
            self, text="ZAMKNIJ", font=("Segoe UI", 11, "bold"),
            fg_color="#34495e", hover_color="#2c3e50", height=35,
            command=self.destroy
        )
        btn_close.pack(pady=(0, 20), padx=25, fill="x")


class PremiumMapView(ctk.CTkFrame):
    def __init__(self, parent, app_instance, **kwargs):
        super().__init__(parent, corner_radius=15, **kwargs)

        self.app_instance = app_instance
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
        MarketReportPopup(
            parent=self.app_instance,
            title_text="Raport Rynkowy",
            info_text=marker.report_text,
            hotel_price=marker.hotel_price,
            flight_price=marker.flight_price
        )

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
            marker_color = "#2ecc71" if iaw_score >= 75 else ("#f39c12" if iaw_score >= 45 else "#e74c3c")
            new_marker = self.map_widget.set_marker(
                lat, lon, marker_color_circle="#ffffff", marker_color_outside=marker_color, command=self.on_marker_click
            )

        new_marker.report_text = info_text
        new_marker.hotel_price = price
        new_marker.flight_price = flight
        self.markers.append(new_marker)