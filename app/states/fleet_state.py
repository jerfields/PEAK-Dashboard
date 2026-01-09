import reflex as rx
import urllib.parse
from typing import TypedDict
import httpx
from app.weather_utils import get_weather_info


class SiteData(TypedDict):
    id: str
    name: str
    location: str
    status: str
    status_color: str
    ac_capacity: str
    availability: float
    performance: float
    measured_energy: float
    modeled_energy: float


class DistributionData(TypedDict):
    name: str
    value: int
    fill: str


class LossData(TypedDict):
    name: str
    value: float
    fill: str


class FleetState(rx.State):
    """State for the Fleet Overview page."""

    sites: list[SiteData] = []
    search_query: str = ""
    sort_field: str = "name"
    sort_reverse: bool = False
    start_date: str = "2025-01-01"
    end_date: str = "2025-12-10"
    total_sites: int = 1
    avg_availability: float = 98.5
    avg_performance: float = 85.8
    total_measured_energy: float = 19127558.5
    total_lost_energy: float = 1268491.0
    weather_location: str = "SAN DIEGO, CA"
    current_temp: str = "--"
    current_condition: str = "LOADING..."
    current_humidity: str = "--%"
    current_wind: str = "-- km/h"
    weather_icon: str = "cloud"

    @rx.event(background=True)
    async def load_weather_data(self):
        """Fetch weather data for San Diego, CA from Open-Meteo."""
        try:
            lat = 32.7157
            lon = -117.1611
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.open-meteo.com/v1/forecast",
                    params={
                        "latitude": lat,
                        "longitude": lon,
                        "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,is_day",
                        "temperature_unit": "celsius",
                        "wind_speed_unit": "kmh",
                    },
                    timeout=10.0,
                )
                if response.status_code == 200:
                    data = response.json()
                    current = data.get("current", {})
                    temp = round(current.get("temperature_2m", 0))
                    humidity = current.get("relative_humidity_2m", 0)
                    wind = current.get("wind_speed_10m", 0)
                    code = current.get("weather_code", 0)
                    is_day = current.get("is_day", 1)
                    icon, desc = get_weather_info(code, is_day)
                    async with self:
                        self.current_temp = f"{temp}°C"
                        self.current_humidity = f"{humidity}%"
                        self.current_wind = f"{wind} km/h"
                        self.current_condition = desc
                        self.weather_icon = icon
        except Exception as e:
            import logging

            logging.exception(f"Error fetching weather data: {e}")

    @rx.var
    def site_distribution(self) -> list[DistributionData]:
        return [
            {"name": "CRITICAL", "value": 0, "fill": "#ef4444"},
            {"name": "WARNING", "value": 0, "fill": "#f59e0b"},
            {"name": "HEALTHY", "value": 1, "fill": "#10b981"},
        ]

    @rx.var
    def loss_breakdown(self) -> list[LossData]:
        return [
            {"name": "DERATED", "value": 3.2, "fill": "#f59e0b"},
            {"name": "PLANT OFFLINE", "value": 32.3, "fill": "#ef4444"},
            {"name": "INVERTERS OFFLINE", "value": 64.5, "fill": "#f97316"},
            {"name": "UNDERPERFORMING", "value": 0.0, "fill": "#8b5cf6"},
        ]

    @rx.event
    def set_search(self, val: str):
        self.search_query = val

    @rx.event
    def toggle_sort(self, field: str):
        if self.sort_field == field:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_field = field
            self.sort_reverse = False

    @rx.var
    def filtered_sites(self) -> list[SiteData]:
        data = self.sites
        if self.search_query:
            q = self.search_query.lower()
            data = [
                s for s in data if q in s["name"].lower() or q in s["location"].lower()
            ]
        return sorted(
            data, key=lambda x: x.get(self.sort_field, ""), reverse=self.sort_reverse
        )

    @rx.event
    def load_fleet_data(self):
        """Load fleet data focusing only on Airport Solar."""
        if len(self.sites) > 0:
            return
        import pandas as pd
        import logging

        airport_solar_data = {
            "name": "Airport Solar",
            "location": "OREGON",
            "ac_capacity": "48.60 MW AC",
            "availability": 98.5,
            "performance": 85.4,
            "measured_energy": 83.3,
            "modeled_energy": 97.5,
        }
        try:
            epc_df = pd.read_excel(
                "assets/EPC Input File - Airport Solar.xlsx", sheet_name="Site Details"
            )
            plant_ac = epc_df[epc_df["Description"] == "Plant AC Capacity (kW)"][
                "Value"
            ].iloc[0]
            airport_solar_data["ac_capacity"] = f"{float(plant_ac) / 1000:.2f} MW AC"
            master_file = "assets/master_report.xlsx"
            metrics_df = pd.read_excel(master_file, sheet_name="Site Metrics")
            if not metrics_df.empty:
                if "DateTime" in metrics_df.columns:
                    dates = pd.to_datetime(metrics_df["DateTime"])
                    self.start_date = dates.min().strftime("%Y-%m-%d")
                    self.end_date = dates.max().strftime("%Y-%m-%d")
                airport_solar_data["performance"] = round(
                    metrics_df["Performance"].mean(), 1
                )
                airport_solar_data["measured_energy"] = round(
                    metrics_df["Measured Energy"].sum(), 1
                )
                airport_solar_data["modeled_energy"] = round(
                    metrics_df["Expected Energy"].sum() / 0.98, 1
                )
        except Exception as e:
            logging.exception(f"Error loading real fleet data: {e}")
        self.sites = [
            {
                "id": urllib.parse.quote("Airport Solar"),
                "name": "Airport Solar",
                "location": airport_solar_data["location"],
                "status": "HEALTHY",
                "status_color": "text-green-400",
                "ac_capacity": airport_solar_data["ac_capacity"],
                "availability": airport_solar_data["availability"],
                "performance": airport_solar_data["performance"],
                "measured_energy": airport_solar_data["measured_energy"],
                "modeled_energy": airport_solar_data["modeled_energy"],
            }
        ]
        self.total_sites = 1
        self.avg_availability = 98.5
        self.avg_performance = airport_solar_data["performance"]
        self.total_measured_energy = airport_solar_data["measured_energy"]
        self.total_lost_energy = (
            airport_solar_data["modeled_energy"] - airport_solar_data["measured_energy"]
        )
        return FleetState.load_weather_data