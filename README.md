# Travel Intelligence Engine

## 📌 Opis projektu
**Travel Intelligence Engine** to zaawansowane, interaktywne narzędzie analityczno-biznesowe (Business Intelligence Dashboard) służące do wielokryterialnej optymalizacji decyzji podróżniczych. Aplikacja dynamicznie pobiera w czasie rzeczywistym rzeczywiste dane rynkowe (ceny hoteli oraz minimalne ceny połączeń lotniczych) z zewnętrznych systemów rezerwacyjnych i na podstawie autorskiego algorytmu **IAW (Index of Analytical Weight)** rekomenduje użytkownikowi optymalny cel podróży spośród europejskich stolic.

System został zaprojektowany w architekturze klient-serwer (separacja warstwy logicznej od prezentacji), wykorzystując nowoczesne biblioteki ekosystemu Python, takie jak **FastAPI, Pandas, NumPy, Matplotlib oraz CustomTkinter**.

---

## 🛠️ Architektura i technologie

### Backend (Warstwa Logiczna & API)
* **Python / FastAPI:** Odpowiada za wystawienie produkcyjnego interfejsu API, walidację danych wejściowych przy użyciu modeli Pydantic oraz koordynację procesu analitycznego.
* **Pandas:** Wykorzystywany do strukturyzacji surowych odpowiedzi JSON z serwerów zewnętrznych, oczyszczania zbiorów danych oraz filtracji brakujących rekordów rynkowych.
* **NumPy:** Służy do wektorowego obliczania bezwzględnych statystyk opisowych (średnie arytmetyczne, odchylenia standardowe) w module optymalizacyjnym.
* **Requests:** Odpowiada za asynchroniczne, dynamiczne odpytywanie zewnętrznych punktów końcowych (RapidAPI / Booking.com) z zachowaniem 60-sekundowych bezpieczników sieciowych (timeout).

### Frontend (Warstwa Prezentacji & GUI)
* **CustomTkinter:** Nowoczesny wrapper biblioteki Tkinter zapewniający estetyczny, responsywny i czytelny interfejs graficzny dla polskiego użytkownika biznesowego.
* **TkinterMapView:** Interaktywny komponent mapy kafelkowej (bazujący na podkładach CartoDB), umożliwiający geograficzną wizualizację przeanalizowanych stolic wraz z kodowaniem kolorystycznym opłacalności wyjazdu.
* **Matplotlib:** Wykorzystany do dynamicznej wizualizacji struktury kosztów (wykres kołowy / Pie Chart) zaimplementowany bezpośrednio wewnątrz dedykowanego okna raportu rynkowego.

---

## 🗂️ Struktura projektu
```text
📦 travel-intelligence-engine
├── 📂 backend
│   ├── analytics.py       # Moduł pobierania danych (API) i algorytm optymalizacji IAW
│   └── main.py            # Serwer FastAPI, definicje modeli Pydantic i endpointy API
├── 📂 frontend
│   ├── app.py             # Główna aplikacja GUI (CustomTkinter) i walidacja formularzy
│   └── components.py      # Autorskie komponenty: wielopoziomowy dropdown i PremiumMapView
├── requirements.txt       # Zamrożone produkcyjne wersje zależności (PEP 8)
└── README.md              # Dokumentacja techniczna projektu
```

## 📊 Algorytm Optymalizacyjny IAW (Index of Analytical Weight)

Serce analityczne aplikacji stanowi autorska synteza wielokryterialna, oparta wyłącznie na ustandaryzowanych wskaźnikach bezwzględnych (niezależnych od wielkości i popularności turystycznej danego miasta):

1. **Warstwa Finansowa (Oszczędność):** Wylicza bezwzględny stosunek łącznych kosztów (średnia cena hotelu + cena lotu z API) do zadeklarowanego budżetu. Wewnątrz budżetu system progresywnie premiuje oszczędności (skala 60–100 pkt). W przypadku przekroczenia limitu finansowego, na miasto nakładana jest płynna, proporcjonalna kara punktowa, a wynik końcowy jest redukowany o połowę, uniemożliwiając droższym kierunkom wyprzedzenie opcji dostępnych budżetowo.
2. **Warstwa Komfortu:** Bazuje w 70% na ustandaryzowanej ocenie gości Booking.com (skala 1–10) oraz w 30% na oficjalnej klasie standardu (gwiazdki 1–5). Wolumen opinii został wycięty, by nie faworyzować sztucznie największych metropolii.
3. **Synteza Wagowa:** Ostateczny scoring (0-100 pkt) jest dynamicznie obliczany jako średnia ważona na podstawie suwaków preferencji (waga budżetu vs waga komfortu) ustawionych przez użytkownika w GUI.

---

## 💡 Instrukcja użytkowania
1. Wprowadź maksymalny budżet w PLN w polu tekstowym.
2. Wprowadź datę przylotu oraz powrotu w formacie YYYY-MM-DD.
3. Ustaw suwaki wag priorytetów dla budżetu oraz komfortu według własnych preferencji.
4. Rozwiń listę miast, zaznacz wybrane stolice i kliknij przycisk **URUCHOM ANALIZĘ RYNKU**.
5. Po zakończeniu obliczeń wynik rekomendacji wyświetli się w panelu bocznym, a na mapie pojawią się kolorowe pinezki.
6. Kliknij dowolną pinezkę na mapie, aby otworzyć wycentrowane okno popup ze szczegółowym raportem rynkowym oraz wykresem kołowym struktury wydatków Matplotlib.

---

## 🚀 Uruchomienie i instalacja

### Wymagania wstępne
Python 3.9 lub nowszy, menedżer pakietów pip.

### Instrukcja krok po kroku
```bash
# 1. Instalacja wszystkich zamrożonych zależności
pip install -r requirements.txt

# 2. Uruchomienie serwera backendowego (w osobnym terminalu)
cd backend
python main.py

# 3. Uruchomienie aplikacji klienckiej frontend (w nowym oknie terminala)
cd ../frontend
python app.py
```
