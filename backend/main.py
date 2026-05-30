from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn

from analytics import fetch_city_data, calculate_iaw_index, CITIES_CONFIG

app = FastAPI(title="Travel Intelligence Engine API", version="1.2.0")


class AnalizaRequest(BaseModel):
    cities: List[str]
    arrival_date: str
    departure_date: str
    budget_weight: float
    comfort_weight: float
    user_budget: float


@app.post("/api/analiza")
def uruchom_analize_rynku(request: AnalizaRequest):
    if not request.cities:
        raise HTTPException(status_code=400, detail="Lista stolic nie może być pusta.")

    compiled_results = {}

    for city in request.cities:
        if city not in CITIES_CONFIG:
            continue

        raw_city_data = fetch_city_data(city, request.arrival_date, request.departure_date)
        if raw_city_data is None:
            continue

        optimized_metrics = calculate_iaw_index(
            raw_city_data,
            budget_weight=request.budget_weight,
            comfort_weight=request.comfort_weight,
            user_budget=request.user_budget
        )

        if optimized_metrics is not None:
            compiled_results[city] = optimized_metrics

    return {
        "status": "success",
        "total_analyzed": len(compiled_results),
        "data": compiled_results
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)