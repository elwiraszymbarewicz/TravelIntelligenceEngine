import pandas as pd
import numpy as np
import requests

CITIES_CONFIG = {
    "Warszawa": {"dest_id": "-534433", "airport": "WAW", "lat": 52.2297, "lon": 21.0122},
    "Praga": {"dest_id": "-553173", "airport": "PRG", "lat": 50.0755, "lon": 14.4378},
    "Budapeszt": {"dest_id": "-850553", "airport": "BUD", "lat": 47.4979, "lon": 19.0402},
    "Bratysława": {"dest_id": "-841052", "airport": "BTS", "lat": 48.1486, "lon": 17.1077},
    "Bukareszt": {"dest_id": "-2144365", "airport": "OTP", "lat": 44.4268, "lon": 26.1025},
    "Sofia": {"dest_id": "-838489", "airport": "SOF", "lat": 42.6977, "lon": 23.3219},
    "Belgrad": {"dest_id": "-753173", "airport": "BEG", "lat": 44.7866, "lon": 20.4489},
    "Zagrzeb": {"dest_id": "-100000", "airport": "ZAG", "lat": 45.8150, "lon": 15.9819},
    "Lublana": {"dest_id": "-85499", "airport": "LJU", "lat": 46.0569, "lon": 14.5058},
    "Sarajewo": {"dest_id": "-94432", "airport": "SJJ", "lat": 43.8563, "lon": 18.4131},
    "Podgorica": {"dest_id": "-93432", "airport": "TGD", "lat": 42.4304, "lon": 19.2594},
    "Tirana": {"dest_id": "-108432", "airport": "TIA", "lat": 41.3275, "lon": 19.8189},
    "Skopje": {"dest_id": "-95432", "airport": "SKP", "lat": 41.9973, "lon": 21.4280},
    "Prisztina": {"dest_id": "-92432", "airport": "PRN", "lat": 42.6629, "lon": 21.1655},
    "Kijów": {"dest_id": "-104432", "airport": "KBP", "lat": 50.4501, "lon": 30.5234},
    "Kiszyniów": {"dest_id": "-2134365", "airport": "KIV", "lat": 47.0105, "lon": 28.8638},
    "Mińsk": {"dest_id": "-1234365", "airport": "MSQ", "lat": 53.9006, "lon": 27.5590},
    "Wilno": {"dest_id": "-2620738", "airport": "VNO", "lat": 54.6872, "lon": 25.2797},
    "Ryga": {"dest_id": "-3212365", "airport": "RIX", "lat": 56.9496, "lon": 24.1052},
    "Tallinn": {"dest_id": "-2625365", "airport": "TLL", "lat": 59.4370, "lon": 24.7536},
    "Berlin": {"dest_id": "-1746443", "airport": "BER", "lat": 52.5200, "lon": 13.4050},
    "Paryż": {"dest_id": "-1456928", "airport": "PAR", "lat": 48.8566, "lon": 2.3522},
    "Londyn": {"dest_id": "-2601889", "airport": "LON", "lat": 51.5074, "lon": -0.1278},
    "Amsterdam": {"dest_id": "-2140479", "airport": "AMS", "lat": 52.3676, "lon": 4.9041},
    "Bruksela": {"dest_id": "-1955538", "airport": "BRU", "lat": 50.8503, "lon": 4.3517},
    "Dublin": {"dest_id": "-1502554", "airport": "DUB", "lat": 53.3498, "lon": -6.2603},
    "Luksemburg": {"dest_id": "-2110479", "airport": "LUX", "lat": 49.6116, "lon": 6.1319},
    "Wiedeń": {"dest_id": "-1995414", "airport": "VIE", "lat": 48.2082, "lon": 16.3738},
    "Berno": {"dest_id": "-2551414", "airport": "BRN", "lat": 46.9480, "lon": 7.4474},
    "Sztokholm": {"dest_id": "-2524279", "airport": "ARN", "lat": 59.3293, "lon": 18.0686},
    "Kopenhaga": {"dest_id": "-2751738", "airport": "CPH", "lat": 55.6761, "lon": 12.5683},
    "Oslo": {"dest_id": "-2701889", "airport": "OSL", "lat": 59.9139, "lon": 10.7522},
    "Helsinki": {"dest_id": "-2114365", "airport": "HEL", "lat": 60.1699, "lon": 24.9384},
    "Reykjavik": {"dest_id": "-2651414", "airport": "KEF", "lat": 64.1466, "lon": -21.9426},
    "Rzym": {"dest_id": "-126693", "airport": "ROM", "lat": 41.9028, "lon": 12.4964},
    "Madryt": {"dest_id": "-390625", "airport": "MAD", "lat": 40.4168, "lon": -3.7038},
    "Lizbona": {"dest_id": "-2165410", "airport": "LIS", "lat": 38.7223, "lon": -9.1393},
    "Ateny": {"dest_id": "-814365", "airport": "ATH", "lat": 37.9838, "lon": 23.7275},
    "Lekozja": {"dest_id": "-2104365", "airport": "LCA", "lat": 35.1856, "lon": 33.3823},
    "Valletta": {"dest_id": "-2054365", "airport": "MLA", "lat": 35.8989, "lon": 14.5146},
    "Andora": {"dest_id": "-111111", "airport": "ALV", "lat": 42.5063, "lon": 1.5218},
    "Monako": {"dest_id": "-123123", "airport": "NCE", "lat": 43.7384, "lon": 7.4246},
    "San Marino": {"dest_id": "-456456", "airport": "RMI", "lat": 43.9424, "lon": 12.4578},
    "Watykan": {"dest_id": "-126693", "airport": "ROM", "lat": 41.9029, "lon": 12.4534},
    "Vaduz": {"dest_id": "-234234", "airport": "ZRH", "lat": 47.1410, "lon": 9.5215},
    "Funchal": {"dest_id": "-2164475", "airport": "FNC", "lat": 32.6500, "lon": -16.9080}
}

API_HEADERS = {
    'x-rapidapi-key': "15f84234f2msh27775c0e0c0592bp1b7334jsn758d3e65313e",
    'x-rapidapi-host': "booking-com15.p.rapidapi.com"
}


def fetch_city_data(city_name: str, arrival_date: str, departure_date: str):
    if city_name not in CITIES_CONFIG:
        return None

    config = CITIES_CONFIG[city_name]
    hotel_url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchHotels"
    flight_url = "https://booking-com15.p.rapidapi.com/api/v1/flights/getMinPrice"

    hotel_params = {
        "dest_id": config["dest_id"], "search_type": "CITY",
        "arrival_date": arrival_date, "departure_date": departure_date,
        "adults": "1", "room_qty": "1", "page_number": "1", "currency_code": "PLN"
    }

    hotel_list = []
    try:
        response = requests.get(hotel_url, headers=API_HEADERS, params=hotel_params, timeout=60)
        if response.status_code == 200:
            json_data = response.json()
            raw_hotels = json_data.get('data', {}).get('hotels', [])

            for h in raw_hotels:
                prop = h.get('property', {})
                val = prop.get('priceBreakdown', {}).get('grossPrice', {}).get('value')
                rating = prop.get('reviewScore', 8.0)

                if val:
                    hotel_list.append({
                        "name": prop.get('name'),
                        "price": float(val),
                        "stars": int(prop.get('propertyClass', 0)),
                        "rating": float(rating)
                    })
    except Exception:
        return None

    if not hotel_list:
        return None

    df_hotels = pd.DataFrame(hotel_list)

    if 'price' not in df_hotels.columns:
        return None

    df_hotels = df_hotels.dropna(subset=['price'])

    if df_hotels.empty:
        return None

    flight_params = {"from_airport": "BER", "to_airport": config["airport"], "date": arrival_date,
                     "currency_code": "PLN"}
    min_flight_price = 0.0
    try:
        flight_resp = requests.get(flight_url, headers=API_HEADERS, params=flight_params, timeout=60)
        if flight_resp.status_code == 200:
            json_data = flight_resp.json()
            val = json_data.get('data', {}).get('minPrice', {}).get('value')
            if val:
                min_flight_price = float(val)
    except Exception:
        pass

    if min_flight_price <= 0:
        min_flight_price = 380.0

    return {
        "hotels_df": df_hotels,
        "min_flight_price": float(min_flight_price),
        "coords": (config["lat"], config["lon"])
    }


def calculate_iaw_index(city_data: dict, budget_weight: float, comfort_weight: float, user_budget: float):
    if city_data is None or "hotels_df" not in city_data:
        return None

    df_hotels = city_data["hotels_df"]
    flight_price = city_data["min_flight_price"]

    prices = df_hotels["price"].to_numpy()
    stars = df_hotels["stars"].to_numpy()
    ratings = df_hotels["rating"].to_numpy()

    mean_hotel_price = np.mean(prices)
    mean_stars = np.mean(stars)
    mean_rating = np.mean(ratings)

    total_cost = flight_price + mean_hotel_price
    budget_usage = total_cost / user_budget

    if total_cost <= user_budget:
        cost_score = 100.0 - (budget_usage * 40.0)
    else:
        cost_score = max(5.0, 50.0 - ((budget_usage - 1.0) * 50.0))

    rating_score = (np.clip(mean_rating, 1.0, 10.0) / 10.0) * 100.0
    star_score = (np.clip(mean_stars, 1.0, 5.0) / 5.0) * 100.0
    comfort_score = (rating_score * 0.7) + (star_score * 0.3)

    total_weights = budget_weight + comfort_weight
    if total_weights == 0:
        total_weights = 1

    final_iaw = ((cost_score * budget_weight) + (comfort_score * comfort_weight)) / total_weights

    if total_cost > user_budget:
        final_iaw = final_iaw * 0.5

    final_iaw = float(np.clip(final_iaw, 5.0, 100.0))

    return {
        "iaw_score": float(round(final_iaw, 1)),
        "mean_hotel_price": float(round(mean_hotel_price, 2)),
        "min_flight_price": float(round(flight_price, 2)),
        "is_anomaly": bool(total_cost > user_budget),
        "coords": city_data["coords"]
    }