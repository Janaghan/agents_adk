from pydantic import BaseModel, Field
from typing import List, Optional

class WeatherResponse(BaseModel):
    location: str
    temperature: str
    weather_code: int
    status: str

class FlightResponse(BaseModel):
    flight: str
    gate: str
    state: str
    departure: str
    status: str

class ResearchResult(BaseModel):
    query: str
    findings: List[str]
    summary: str
