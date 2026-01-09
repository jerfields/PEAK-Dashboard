import reflex as rx
import pandas as pd
from datetime import datetime
import logging
import random
import plotly.graph_objects as go
import httpx
from app.weather_utils import get_weather_info


class DashboardState(rx.State):
    current_site_id: str = "Airport Solar"
    active_tab: str = "Executive Summary"
    start_date: str = "2025-01-01"
    end_date: str = "2025-12-10"
    site_name: str = "AIRPORT SOLAR"
    location: str = "OREGON"
    ac_capacity: str = "48.60 MW"
    dc_capacity: str = "60.70 MW"
    lat: str = "42.16"
    lon: str = "-120.4"
    status: str = "HEALTHY"
    client: str = "DESRI"
    inception_date: str = "7/3/2023"
    inverter_type: str = "Power Electronics"
    poi_limit: str = "48.60 MW"
    available_sites: list[str] = ["AIRPORT SOLAR"]
    show_settings_modal: bool = False
    soiling_loss_pct: float = 0.5
    vegetation_loss_pct: float = 0.0
    nav_sections: dict[str, list[dict[str, str]]] = {
        "MONITORING & ANALYTICS": [
            {"label": "FLEET DASHBOARD", "icon": "layout-dashboard", "href": "/"},
            {"label": "MAP VIEW", "icon": "map", "href": "#"},
            {"label": "SITE PRIORITY VIEW", "icon": "alert-triangle", "href": "#"},
            {"label": "SITE OVERVIEW", "icon": "layout", "href": "#"},
        ],
        "SYSTEM": [
            {"label": "SETTINGS", "icon": "settings", "href": "#"},
            {"label": "GLOSSARY", "icon": "book-open", "href": "#"},
            {"label": "USER GUIDE", "icon": "help-circle", "href": "#"},
        ],
    }
    tabs: list[str] = ["Executive Summary", "Priority View", "Equipment Heatmap"]

    @rx.event
    def set_tab(self, tab: str):
        self.active_tab = tab

    @rx.event
    def toggle_settings_modal(self):
        self.show_settings_modal = not self.show_settings_modal

    @rx.event
    def set_soiling_loss(self, val: str):
        try:
            self.soiling_loss_pct = float(val)
        except ValueError as e:
            logging.exception(f"Error: {e}")

    @rx.event
    def set_vegetation_loss(self, val: str):
        try:
            self.vegetation_loss_pct = float(val)
        except ValueError as e:
            logging.exception(f"Error: {e}")

    performance: float = 78.3
    availability: float = 87.8
    contractual_availability: float = 98.2
    potential_lds: float = -42097.0
    measured_energy: float = 993.4
    modeled_energy: float = 1268.9
    modeled_insolation: float = 2736.7
    measured_insolation: float = 2890.1
    expected_energy: float = 1268.9
    curtailed_energy: float = 0.0
    total_lost_energy: float = 275.5
    excused_energy: float = 1739.8
    inverters_offline_loss: float = 11779.4
    plant_offline_loss: float = 2539.4
    derated_loss: float = 0.0
    underperformance_loss: float = 0.0
    loss_driver_unit: str = "MWh"
    primary_loss_data: list[dict[str, str | float]] = [
        {
            "name": "Plant Outage",
            "loss_pct": 2.6,
            "mwh": 33.0,
            "revenue": 1649.03,
            "color": "bg-red-500",
        },
        {
            "name": "Inverters",
            "loss_pct": 0.1,
            "mwh": 2.0,
            "revenue": 81.74,
            "color": "bg-orange-400",
        },
        {
            "name": "Inverter Modules",
            "loss_pct": 0.4,
            "mwh": 5.0,
            "revenue": 273.71,
            "color": "bg-yellow-500",
        },
        {
            "name": "Derate",
            "loss_pct": 0.0,
            "mwh": 0.0,
            "revenue": 0.0,
            "color": "bg-gray-500",
        },
        {
            "name": "DC",
            "loss_pct": 4.2,
            "mwh": 53.0,
            "revenue": 2634.24,
            "color": "bg-cyan-500",
        },
        {
            "name": "Trackers",
            "loss_pct": 3.6,
            "mwh": 45.0,
            "revenue": 2264.35,
            "color": "bg-blue-500",
        },
        {
            "name": "Soiling",
            "loss_pct": 0.5,
            "mwh": 6.0,
            "revenue": 317.23,
            "color": "bg-emerald-500",
        },
        {
            "name": "Vegetation",
            "loss_pct": 0.0,
            "mwh": 0.0,
            "revenue": 0.0,
            "color": "bg-green-700",
        },
        {
            "name": "Misc",
            "loss_pct": 10.3,
            "mwh": 131.0,
            "revenue": 6554.7,
            "color": "bg-purple-500",
        },
    ]
    weather_forecast: list[dict] = [
        {"day": "TUE", "icon": "cloud-rain", "high": 8, "low": -4},
        {"day": "WED", "icon": "snowflake", "high": 12, "low": -2},
        {"day": "THU", "icon": "snowflake", "high": 4, "low": -1},
        {"day": "FRI", "icon": "snowflake", "high": -1, "low": -6},
        {"day": "SAT", "icon": "sun", "high": -1, "low": -7},
        {"day": "SUN", "icon": "cloud-sun", "high": 6, "low": -4},
        {"day": "MON", "icon": "cloud", "high": 3, "low": -2},
    ]
    current_temp: str = "2"
    current_feels_like: str = "-2"
    current_condition: str = "CLEAR SKY"
    current_humidity: str = "56%"
    current_wind: str = "6.6 km/h"
    weather_location: str = "CROWNPOINT"
    current_icon: str = "moon"

    @rx.event
    def set_loss_driver_unit(self, unit: str):
        self.loss_driver_unit = unit

    @rx.var
    def loss_drivers(self) -> list[dict[str, str | float]]:
        """Prepare sorted data for the Loss Drivers panel based on selected unit."""
        raw_data = self.primary_loss_data
        key_map = {"MWh": "mwh", "%": "loss_pct", "$": "revenue"}
        unit_key = key_map.get(self.loss_driver_unit, "mwh")
        sorted_data = sorted(
            raw_data, key=lambda x: float(x.get(unit_key, 0.0)), reverse=True
        )
        max_val = (
            max([float(x.get(unit_key, 0.0)) for x in sorted_data])
            if sorted_data
            else 1.0
        )
        if max_val == 0:
            max_val = 1.0
        drivers = []
        for item in sorted_data:
            val = float(item.get(unit_key, 0.0))
            display = ""
            if self.loss_driver_unit == "MWh":
                display = f"{val:,.1f} MWh"
            elif self.loss_driver_unit == "%":
                display = f"{val:,.1f}%"
            else:
                display = f"${val:,.2f}"
            drivers.append(
                {
                    "name": item["name"],
                    "display_value": display,
                    "color": item["color"],
                    "width_pct": val / max_val * 100,
                }
            )
        return drivers

    @rx.var
    def waterfall_plotly_fig(self) -> go.Figure:
        """Generate a Plotly Waterfall chart for energy loss profile with units."""
        x_data = ["Expected Energy"]
        y_data = [float(self.expected_energy)]
        measure = ["absolute"]
        text_data = [f"{self.expected_energy:,.1f} MWh"]
        for driver in self.primary_loss_data:
            x_data.append(driver["name"])
            loss_val = -abs(float(driver.get("mwh", 0.0)))
            y_data.append(loss_val)
            measure.append("relative")
            text_data.append(f"{loss_val:,.1f} MWh" if abs(loss_val) > 0.01 else "")
        x_data.append("Measured Energy")
        y_data.append(0)
        measure.append("total")
        text_data.append(f"{self.measured_energy:,.1f} MWh")
        fig = go.Figure(
            go.Waterfall(
                name="Energy Profile",
                orientation="v",
                measure=measure,
                x=x_data,
                textposition="outside",
                text=text_data,
                y=y_data,
                connector={"line": {"color": "rgba(255,255,255,0.2)"}},
                increasing={"marker": {"color": "#10b981"}},
                decreasing={"marker": {"color": "#ef4444"}},
                totals={"marker": {"color": "#06b6d4"}},
                textfont=dict(color="white", size=11, family="Inter"),
                hovertemplate="%{x}: %{y:,.1f} MWh<extra></extra>",
            )
        )
        max_val = max(self.expected_energy, self.measured_energy) * 1.15
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#9ca3af", size=10, family="Inter"),
            margin=dict(l=10, r=10, t=5, b=10),
            xaxis=dict(
                showgrid=False, zeroline=False, tickfont=dict(color="#9ca3af", size=10)
            ),
            yaxis=dict(
                title=dict(text="ENERGY (MWh)", font=dict(size=10)),
                showgrid=True,
                gridcolor="rgba(255,255,255,0.05)",
                zeroline=False,
                tickfont=dict(color="#9ca3af", size=10),
                range=[0, max_val],
            ),
            height=310,
            showlegend=False,
            hoverlabel=dict(
                bgcolor="#111827",
                bordercolor="rgba(255,255,255,0.1)",
                font=dict(color="white", size=12, family="Inter"),
                align="left",
            ),
        )
        return fig

    @rx.var
    def dynamic_summary(self) -> list[str]:
        """Generate a list of strings representing the 5-point analysis narrative."""
        return [
            "1. DC system issues are the largest driver of under-performance (~4.2%, ~53MWh lost); prioritize corrective actions on DC string outages and the recorded DC feeder down event.",
            '2. Tracker system faults are a significant contributor (~3.6%, ~45 MWh lost); address high-frequency "stuck tracker" events to recover aggregate production losses. Most of these events were flagged on a single that correlates to the Plant Offline date. Further verification may be necessary.',
            "3. Plant outage losses (~2.6%, ~33 MWh) materially impacted site performance but were isolated to a single day of 12/10/2025.",
            "4. Inverter offline events had minor but recurring impact (~0.1%, ~2 MWh); restore affected inverters and monitor for repeat offline occurrences.",
            "5. Inverter Modules (~0.4%, ~5 MWh) are comparatively small; further investigation and corrective action may be needed on identified inverter module issues where calculated, but treat as lower priority relative to DC and tracker losses.",
        ]

    @rx.event(background=True)
    async def load_weather_data(self):
        """Fetch weather data for the site location from Open-Meteo."""
        try:
            lat = float(self.lat) if self.lat else 42.16
            lon = float(self.lon) if self.lon else -120.4
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.open-meteo.com/v1/forecast",
                    params={
                        "latitude": lat,
                        "longitude": lon,
                        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,is_day",
                        "daily": "weather_code,temperature_2m_max,temperature_2m_min",
                        "timezone": "auto",
                        "forecast_days": 7,
                        "temperature_unit": "celsius",
                        "wind_speed_unit": "kmh",
                    },
                    timeout=10.0,
                )
                if response.status_code == 200:
                    data = response.json()
                    current = data.get("current", {})
                    daily = data.get("daily", {})
                    temp = round(current.get("temperature_2m", 0))
                    feels_like = round(current.get("apparent_temperature", 0))
                    humidity = current.get("relative_humidity_2m", 0)
                    wind = current.get("wind_speed_10m", 0)
                    code = current.get("weather_code", 0)
                    is_day = current.get("is_day", 1)
                    icon, condition = get_weather_info(code, is_day)
                    forecast_items = []
                    times = daily.get("time", [])
                    highs = daily.get("temperature_2m_max", [])
                    lows = daily.get("temperature_2m_min", [])
                    codes = daily.get("weather_code", [])
                    for i in range(min(7, len(times))):
                        date_str = times[i]
                        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                        day_name = date_obj.strftime("%a").upper()
                        icon, _ = get_weather_info(codes[i], 1)
                        forecast_items.append(
                            {
                                "day": day_name,
                                "icon": icon,
                                "high": round(highs[i]),
                                "low": round(lows[i]),
                            }
                        )
                    async with self:
                        self.current_temp = str(temp)
                        self.current_feels_like = str(feels_like)
                        self.current_humidity = f"{humidity}%"
                        self.current_wind = f"{wind} km/h"
                        self.current_condition = condition
                        self.current_icon = icon
                        self.weather_forecast = forecast_items
        except Exception as e:
            logging.exception(f"Error fetching site weather data: {e}")

    @rx.event
    async def load_site_data(self):
        """Load data from the provided Excel files with proper metadata extraction."""
        route_site_id = self.router.url.query_parameters.get("site_id")
        self.active_tab = "Executive Summary"
        self.site_name = "AIRPORT SOLAR"
        self.current_site_id = "Airport Solar"
        self.available_sites = ["AIRPORT SOLAR"]
        try:
            epc_file = "assets/EPC Input File - Airport Solar.xlsx"
            site_details = pd.read_excel(epc_file, sheet_name="Site Details")

            def _get_val(desc_name, default):
                row = site_details[site_details["Description"] == desc_name]
                return row["Value"].iloc[0] if not row.empty else default

            self.client = str(_get_val("Client Name", "DESRI"))
            plant_ac = _get_val("Plant AC Capacity (kW)", 48600)
            plant_dc = _get_val("Plant DC Capacity (kW)", 60697.91)
            self.ac_capacity = f"{float(plant_ac) / 1000:.2f} MW"
            self.dc_capacity = f"{float(plant_dc) / 1000:.2f} MW"
            lat_val = _get_val("Latitude", 42.16)
            lon_val = _get_val("Longitude", -120.4)
            self.lat = str(lat_val)
            self.lon = str(lon_val)
            self.location = "OREGON"
            self.inception_date = str(
                _get_val("Plant Substantial Completion Date", "7/3/2023")
            )
            self.inverter_type = str(_get_val("Inverter Model", "Power Electronics"))
            poi_val = _get_val("POI Curtail Limit (kW)", None)
            if poi_val is None or (isinstance(poi_val, float) and pd.isna(poi_val)):
                poi_val = _get_val("poi_curtail_sp", 48600)
            self.poi_limit = f"{float(poi_val) / 1000:.2f} MW"
            self.weather_location = "LAKEVIEW"
            master_file = "assets/master_report.xlsx"
            site_metrics = pd.read_excel(master_file, sheet_name="Site Metrics")
            if not site_metrics.empty:
                if "DateTime" in site_metrics.columns:
                    dates = pd.to_datetime(site_metrics["DateTime"])
                    self.start_date = dates.min().strftime("%Y-%m-%d")
                    self.end_date = dates.max().strftime("%Y-%m-%d")
                self.measured_energy = float(site_metrics["Measured Energy"].sum())
                self.expected_energy = float(site_metrics["Expected Energy"].sum())
                self.curtailed_energy = float(site_metrics["Curtailed Energy"].sum())
                self.performance = round(float(site_metrics["Performance"].mean()), 1)
                self.availability = 98.5
                self.modeled_energy = (
                    self.expected_energy / 0.98 if self.expected_energy else 0.0
                )

                def _get_sheet_sum(sheet_name, is_kwh=True):
                    try:
                        df = pd.read_excel(master_file, sheet_name=sheet_name)
                        numeric_cols = df.select_dtypes(include=["number"])
                        total = numeric_cols.sum().sum()
                        return total / 1000.0 if is_kwh else total
                    except Exception as e:
                        logging.exception(f"Error reading sheet {sheet_name}: {e}")
                        return 0.0

                self.inverters_offline_loss = _get_sheet_sum("inv_kW_offline_lost")
                self.derated_loss = _get_sheet_sum("inv_kW_derate_lost")
                try:
                    plant_offline_df = pd.read_excel(
                        master_file, sheet_name="site_kW_plant_offline_loss (pi)"
                    )
                    self.plant_offline_loss = (
                        plant_offline_df.select_dtypes(include=["number"]).sum().sum()
                        / 1000.0
                    )
                except Exception as e:
                    logging.exception(f"Error reading plant offline sheet: {e}")
                    self.plant_offline_loss = 2.5
                self.underperformance_loss = 0.0
                self.total_lost_energy = (
                    self.inverters_offline_loss
                    + self.plant_offline_loss
                    + self.derated_loss
                    + self.underperformance_loss
                    + self.curtailed_energy
                )
                self.potential_lds = -42097.0
                self.contractual_availability = 98.2
                self.excused_energy = 1739.8
                try:
                    t_dc_df = pd.read_excel(
                        master_file, sheet_name="Tracker - Affected DC Capacity"
                    )
                    t_lost_df = pd.read_excel(
                        master_file, sheet_name="Tracker - Lost Energy"
                    )
                    t_cols = [c for c in t_dc_df.columns if c != "DateTime"]
                    controllers = sorted(list(set((c.split("/")[0] for c in t_cols))))
                    motors = sorted(
                        list(set((c.split("/")[1] for c in t_cols if "/" in c)))
                    )
                    t_dc_sum = t_dc_df[t_cols].sum()
                    t_lost_sum = t_lost_df[t_cols].sum()
                    z_dc = []
                    z_lost = []
                    for ctrl in controllers:
                        row_dc = []
                        row_lost = []
                        for motor in motors:
                            col_name = f"{ctrl}/{motor}"
                            row_dc.append(float(t_dc_sum.get(col_name, 0.0)))
                            row_lost.append(float(t_lost_sum.get(col_name, 0.0)))
                        z_dc.append(row_dc)
                        z_lost.append(row_lost)
                    self.tracker_z_dc = z_dc
                    self.tracker_z_lost = z_lost
                    self.tracker_x_motors = motors
                    self.tracker_y_controllers = controllers
                except Exception as e:
                    logging.exception(f"Tracker data error: {e}")
                try:
                    dc_lost_df = pd.read_excel(
                        master_file, sheet_name="DC - Lost Energy"
                    )
                    dc_cap_df = pd.read_excel(
                        master_file, sheet_name="DC - Affected Capacity"
                    )
                    dc_class_df = pd.read_excel(
                        master_file, sheet_name="DC - Classification"
                    )
                    cols = [c for c in dc_lost_df.columns if c != "timestamp"]
                    raw_inverters = set()
                    raw_cbs = set()
                    for c in cols:
                        if " - " in c:
                            parts = c.split(" - ")
                            raw_inverters.add(parts[0])
                            raw_cbs.add(parts[1])
                    self.cb_y_inverters = sorted(list(raw_inverters))
                    self.cb_x_combiner_boxes = sorted(list(raw_cbs))
                    lost_sums = dc_lost_df[cols].sum()
                    cap_sums = dc_cap_df[cols].sum()

                    @rx.event
                    def get_mode_class(col):
                        if col not in dc_class_df.columns:
                            return "Healthy"
                        mode_series = dc_class_df[col].dropna().mode()
                        return (
                            str(mode_series.iloc[0])
                            if not mode_series.empty
                            else "Healthy"
                        )

                    class_map = {c: get_mode_class(c) for c in cols}
                    z_lost, z_cap, z_class = ([], [], [])
                    for inv in self.cb_y_inverters:
                        row_lost, row_cap, row_class = ([], [], [])
                        for cb in self.cb_x_combiner_boxes:
                            col_name = f"{inv} - {cb}"
                            row_lost.append(float(lost_sums.get(col_name, 0.0)))
                            row_cap.append(float(cap_sums.get(col_name, 0.0)))
                            row_class.append(class_map.get(col_name, "Healthy"))
                        z_lost.append(row_lost)
                        z_cap.append(row_cap)
                        z_class.append(row_class)
                    self.cb_z_lost = z_lost
                    self.cb_z_capacity = z_cap
                    self.cb_z_classifications = z_class
                except Exception as e:
                    logging.exception(f"CB data error: {e}")
                try:
                    import re
                    import math

                    inv_lost_df = pd.read_excel(
                        master_file, sheet_name="Inverter - Lost Energy"
                    )
                    inv_dc_df = pd.read_excel(
                        master_file, sheet_name="Inverter - DC Capacity"
                    )
                    inv_mod_lost_df = pd.read_excel(
                        master_file, sheet_name="Inverter Mod - Lost Energy"
                    )
                    cols = sorted([c for c in inv_lost_df.columns if c != "Unnamed: 0"])
                    rows, cols_grid = (3, 6)
                    z_lost, z_cap, z_offline, z_module, z_names = ([], [], [], [], [])
                    for r in range(rows):
                        row_lost, row_cap, row_offline, row_module, row_names = (
                            [],
                            [],
                            [],
                            [],
                            [],
                        )
                        for c in range(cols_grid):
                            idx = r * cols_grid + c
                            if idx < len(cols):
                                col_name = cols[idx]
                                off_val = float(inv_lost_df[col_name].sum())
                                mod_val = float(inv_mod_lost_df[col_name].sum())
                                row_offline.append(off_val)
                                row_module.append(mod_val)
                                row_lost.append(off_val + mod_val)
                                row_cap.append(float(inv_dc_df[col_name].iloc[0]))
                                row_names.append(col_name)
                            else:
                                row_offline.append(0.0)
                                row_module.append(0.0)
                                row_lost.append(0.0)
                                row_cap.append(0.0)
                                row_names.append("Empty")
                        z_lost.append(row_lost)
                        z_cap.append(row_cap)
                        z_offline.append(row_offline)
                        z_module.append(row_module)
                        z_names.append(row_names)
                    self.inv_z_lost_energy = z_lost
                    self.inv_z_dc_capacity = z_cap
                    self.inv_z_offline_lost = z_offline
                    self.inv_z_module_lost = z_module
                    self.inv_inverter_names = z_names
                    self.inv_x_positions = [str(i + 1) for i in range(cols_grid)]
                    self.inv_y_blocks = [str(i + 1) for i in range(rows)]
                except Exception as e:
                    logging.exception(f"Inverter data error: {e}")
        except Exception as e:
            logging.exception(f"Error loading real data for Airport Solar: {e}")
            self.location = "OREGON (FALLBACK)"

    @rx.event
    async def finalize_site_load(self):
        """Finalize site data loading after async operations if needed."""
        self.sites_data = [
            {
                "name": self.site_name,
                "status": "HEALTHY",
                "ac_capacity": self.ac_capacity,
                "availability": f"{self.availability}%",
                "performance": f"{self.performance}%",
                "measured_energy": f"{self.measured_energy:,.1f} MWh",
                "modeled_energy": f"{self.modeled_energy:,.1f} MWh",
                "status_color": "text-green-400",
            }
        ]
        yield DashboardState.load_weather_data

    @rx.var
    def current_year(self) -> str:
        return str(datetime.now().year)

    outstanding_inverters: int = 5
    outstanding_transformers: int = 3
    outstanding_breakers: int = 1
    outstanding_trackers: int = 5
    show_tracker_modal: bool = False
    tracker_modal_search: str = ""
    tracker_z_dc: list[list[float]] = []
    tracker_z_lost: list[list[float]] = []
    tracker_x_motors: list[str] = []
    tracker_y_controllers: list[str] = []
    cb_z_lost: list[list[float]] = []
    cb_z_capacity: list[list[float]] = []
    cb_z_classifications: list[list[str]] = []
    cb_x_combiner_boxes: list[str] = []
    cb_y_inverters: list[str] = []
    cb_heatmap_mode: str = "CAPACITY"
    show_cb_modal: bool = False
    cb_modal_search: str = ""
    inv_z_dc_capacity: list[list[float]] = []
    inv_z_lost_energy: list[list[float]] = []
    inv_z_offline_lost: list[list[float]] = []
    inv_z_module_lost: list[list[float]] = []
    inv_inverter_names: list[list[str]] = []
    inv_x_positions: list[str] = []
    inv_y_blocks: list[str] = []
    show_inv_modal: bool = False
    inv_modal_search: str = ""
    site_search: str = ""
    sites_data: list[dict[str, str | float]] = []

    @rx.event
    def set_site_search(self, query: str):
        self.site_search = query

    @rx.event
    def toggle_tracker_modal(self):
        self.show_tracker_modal = not self.show_tracker_modal

    @rx.event
    def set_tracker_modal_search(self, val: str):
        self.tracker_modal_search = val

    @rx.event
    def set_cb_heatmap_mode(self, mode: str):
        self.cb_heatmap_mode = mode

    @rx.event
    def toggle_cb_modal(self):
        self.show_cb_modal = not self.show_cb_modal

    @rx.event
    def set_cb_modal_search(self, val: str):
        self.cb_modal_search = val

    @rx.event
    def toggle_inv_modal(self):
        self.show_inv_modal = not self.show_inv_modal

    @rx.event
    def set_inv_modal_search(self, val: str):
        self.inv_modal_search = val

    @rx.var
    def filtered_sites(self) -> list[dict[str, str | float]]:
        if not self.site_search:
            return self.sites_data
        query = self.site_search.lower()
        return [site for site in self.sites_data if query in site["name"].lower()]

    @rx.var
    def tracker_motors_with_issues(self) -> int:
        """Count total motor-controller combinations with lost energy > 0."""
        if not self.tracker_z_lost:
            return 0
        total_issues = 0
        for row in self.tracker_z_lost:
            for val in row:
                if val > 0:
                    total_issues += 1
        return total_issues

    @rx.var
    def tracker_total_lost_energy(self) -> float:
        """Sum of all lost energy values in tracker_z_lost (already in MWh)."""
        total = 0.0
        for row in self.tracker_z_lost:
            for val in row:
                total += val
        return total

    @rx.var
    def tracker_total_lost_revenue(self) -> float:
        """Total Lost Revenue for trackers: Lost Energy MWh * $40/MWh."""
        return self.tracker_total_lost_energy * 40.0

    @rx.var
    def motors_with_issues_list(self) -> list[dict[str, str | float]]:
        """Extract unique list of tracker motors with issues > 0.1kWh lost energy."""
        if (
            not self.tracker_z_lost
            or not self.tracker_x_motors
            or (not self.tracker_y_controllers)
        ):
            return []
        issues = []
        for i, controller in enumerate(self.tracker_y_controllers):
            for j, motor in enumerate(self.tracker_x_motors):
                lost_val = self.tracker_z_lost[i][j]
                if lost_val > 0.1:
                    dc_val = self.tracker_z_dc[i][j]
                    issues.append(
                        {
                            "motor": motor,
                            "controller": controller,
                            "dc_capacity": round(float(dc_val), 1),
                            "lost_energy": round(float(lost_val), 1),
                        }
                    )
        if self.tracker_modal_search:
            q = self.tracker_modal_search.lower()
            issues = [
                i
                for i in issues
                if q in str(i["motor"]).lower() or q in str(i["controller"]).lower()
            ]
        return sorted(issues, key=lambda x: x["lost_energy"], reverse=True)

    @rx.var
    def tracker_most_problematic_controller(self) -> str:
        """Find the controller name with the highest total lost energy."""
        if not self.tracker_z_lost or not self.tracker_y_controllers:
            return "N/A"
        max_loss = -1.0
        best_idx = 0
        for i, row in enumerate(self.tracker_z_lost):
            row_sum = sum(row)
            if row_sum > max_loss:
                max_loss = row_sum
                best_idx = i
        if best_idx < len(self.tracker_y_controllers):
            return self.tracker_y_controllers[best_idx]
        return "N/A"

    @rx.var
    def tracker_heatmap_fig(self) -> go.Figure:
        custom_data = []
        for i in range(len(self.tracker_z_lost)):
            row = []
            for j in range(len(self.tracker_z_lost[i])):
                lost_val = self.tracker_z_lost[i][j]
                cost_val = lost_val * 40.0
                cap_val = self.tracker_z_dc[i][j]
                row.append([lost_val, cost_val, cap_val])
            custom_data.append(row)
        fig = go.Figure(
            data=go.Heatmap(
                z=self.tracker_z_lost,
                x=self.tracker_x_motors,
                y=self.tracker_y_controllers,
                customdata=custom_data,
                colorscale="RdYlGn_r",
                colorbar=dict(
                    title=dict(text="Lost Energy (MWh)", font=dict(color="#9ca3af")),
                    tickfont=dict(color="#9ca3af"),
                ),
                hovertemplate="<b>Controller:</b> %{y}<br>"
                + "<b>Motor:</b> %{x}<br>"
                + "<b>Lost Energy:</b> %{z:,.1f} MWh<br>"
                + "<b>DC Capacity:</b> %{customdata[2]:,.1f} kW<br>"
                + "<b>Cost Impact:</b> $%{customdata[1]:,.1f}<extra></extra>",
            )
        )
        fig.update_layout(
            title=None,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#9ca3af", size=10, family="Inter"),
            margin=dict(l=10, r=40, t=20, b=10),
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False,
                title=dict(text="MOTORS", font=dict(size=10)),
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                autorange="reversed",
                title=dict(text="CONTROLLERS", font=dict(size=10)),
            ),
            height=600,
        )
        return fig

    @rx.var
    def cb_combiner_boxes_with_issues(self) -> int:
        """Count total instances of CB-Inverter combinations with issues (lost energy > 0)."""
        if not self.cb_z_lost:
            return 0
        total_issues = 0
        for row in self.cb_z_lost:
            for val in row:
                if val > 0:
                    total_issues += 1
        return total_issues

    @rx.var
    def cb_total_lost_energy(self) -> float:
        """Sum of all lost energy values in cb_z_lost (already in MWh)."""
        total = 0.0
        for row in self.cb_z_lost:
            total += sum(row)
        return total

    @rx.var
    def cb_total_lost_revenue(self) -> float:
        """Total Lost Revenue for Combiner Boxes: Lost Energy MWh * $40/MWh."""
        return self.cb_total_lost_energy * 40.0

    @rx.var
    def cb_most_problematic_box(self) -> str:
        """Find the CB name with the highest total lost energy."""
        if not self.cb_z_lost or not self.cb_x_combiner_boxes:
            return "N/A"
        num_rows = len(self.cb_z_lost)
        if num_rows == 0:
            return "N/A"
        num_cols = len(self.cb_z_lost[0])
        max_loss = -1.0
        best_col_idx = 0
        for j in range(num_cols):
            col_sum = 0.0
            for i in range(num_rows):
                if j < len(self.cb_z_lost[i]):
                    col_sum += self.cb_z_lost[i][j]
            if col_sum > max_loss:
                max_loss = col_sum
                best_col_idx = j
        if best_col_idx < len(self.cb_x_combiner_boxes):
            return self.cb_x_combiner_boxes[best_col_idx]
        return "N/A"

    @rx.var
    def cb_issues_list(self) -> list[dict[str, str | float]]:
        """Extract list of inverters with issues > 0 kWh lost energy."""
        if (
            not self.cb_z_lost
            or not self.cb_x_combiner_boxes
            or (not self.cb_y_inverters)
        ):
            return []
        issues = []
        for i, inv in enumerate(self.cb_y_inverters):
            for j, cb in enumerate(self.cb_x_combiner_boxes):
                lost_val = self.cb_z_lost[i][j]
                if lost_val > 0:
                    cap_val = self.cb_z_capacity[i][j]
                    issues.append(
                        {
                            "inverter": inv,
                            "cb": cb,
                            "capacity": round(float(cap_val), 1),
                            "lost_energy": round(float(lost_val), 1),
                        }
                    )
        if self.cb_modal_search:
            q = self.cb_modal_search.lower()
            issues = [
                i
                for i in issues
                if q in str(i["inverter"]).lower() or q in str(i["cb"]).lower()
            ]
        return sorted(issues, key=lambda x: x["lost_energy"], reverse=True)

    @rx.var
    def inv_inverters_with_issues(self) -> int:
        if not self.inv_z_lost_energy:
            return 0
        return sum((1 for row in self.inv_z_lost_energy for val in row if val > 0))

    @rx.var
    def inv_total_lost_energy(self) -> float:
        if not self.inv_z_lost_energy:
            return 0.0
        return sum((sum(row) for row in self.inv_z_lost_energy))

    @rx.var
    def inv_total_lost_revenue(self) -> float:
        return self.inv_total_lost_energy * 40.0

    @rx.var
    def inv_most_problematic_block(self) -> str:
        """Returns the name of the inverter with the highest loss."""
        if not self.inv_z_lost_energy or not self.inv_inverter_names:
            return "N/A"
        max_loss = -1.0
        best_inv = "N/A"
        for i, row in enumerate(self.inv_z_lost_energy):
            for j, val in enumerate(row):
                if val > max_loss:
                    max_loss = val
                    best_inv = self.inv_inverter_names[i][j]
        return best_inv

    @rx.var
    def inv_issues_list(self) -> list[dict[str, str | float]]:
        if not self.inv_z_lost_energy:
            return []
        issues = []
        for i, block in enumerate(self.inv_y_blocks):
            for j, pos in enumerate(self.inv_x_positions):
                lost_val = self.inv_z_lost_energy[i][j]
                if lost_val > 0:
                    issues.append(
                        {
                            "inverter": f"{block} P{pos}",
                            "block": block,
                            "capacity": round(float(self.inv_z_dc_capacity[i][j]), 1),
                            "lost_energy": round(float(lost_val), 1),
                        }
                    )
        if self.inv_modal_search:
            q = self.inv_modal_search.lower()
            issues = [i for i in issues if q in i["inverter"].lower()]
        return sorted(issues, key=lambda x: x["lost_energy"], reverse=True)

    @rx.var
    def inv_heatmap_fig(self) -> go.Figure:
        if not self.inv_z_lost_energy:
            return go.Figure()
        custom_data = []
        for i in range(len(self.inv_z_lost_energy)):
            row = []
            for j in range(len(self.inv_z_lost_energy[i])):
                name = self.inv_inverter_names[i][j]
                lost = self.inv_z_lost_energy[i][j]
                off = self.inv_z_offline_lost[i][j]
                mod = self.inv_z_module_lost[i][j]
                cap = self.inv_z_dc_capacity[i][j]
                row.append([name, lost, off, mod, cap, lost * 40.0])
            custom_data.append(row)
        fig = go.Figure(
            data=go.Heatmap(
                z=self.inv_z_lost_energy,
                x=self.inv_x_positions,
                y=self.inv_y_blocks,
                customdata=custom_data,
                colorscale="RdYlGn_r",
                colorbar=dict(
                    title=dict(text="Lost Energy (MWh)", font=dict(color="#9ca3af")),
                    tickfont=dict(color="#9ca3af"),
                    thickness=15,
                ),
                hovertemplate="<b>Inverter ID:</b> %{customdata[0]}<br>"
                + "<b>Combined Lost Energy:</b> %{customdata[1]:,.1f} MWh<br>"
                + "<b>Offline Lost Energy:</b> %{customdata[2]:,.1f} MWh<br>"
                + "<b>Module Lost Energy:</b> %{customdata[3]:,.1f} MWh<br>"
                + "<b>DC Capacity:</b> %{customdata[4]:,.1f} kW<br>"
                + "<b>Revenue Impact:</b> $%{customdata[5]:,.1f}<extra></extra>",
                showscale=True,
            )
        )
        fig.update_layout(
            title=None,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#9ca3af", size=10, family="Inter"),
            margin=dict(l=5, r=5, t=5, b=5),
            xaxis=dict(
                showgrid=False, zeroline=False, showticklabels=False, title=None
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                autorange="reversed",
                showticklabels=False,
                title=None,
            ),
            height=250,
            dragmode=False,
        )
        return fig

    @rx.var
    def cb_heatmap_fig(self) -> go.Figure:
        custom_data = []
        for i in range(len(self.cb_z_lost)):
            row = []
            for j in range(len(self.cb_z_lost[i])):
                desc = (
                    self.cb_z_classifications[i][j]
                    if i < len(self.cb_z_classifications)
                    and j < len(self.cb_z_classifications[i])
                    else "N/A"
                )
                lost_val = self.cb_z_lost[i][j]
                cost_val = lost_val * 40.0
                cap_val = self.cb_z_capacity[i][j]
                row.append([desc, cost_val, cap_val])
            custom_data.append(row)
        fig = go.Figure(
            data=go.Heatmap(
                z=self.cb_z_lost,
                x=self.cb_x_combiner_boxes,
                y=self.cb_y_inverters,
                customdata=custom_data,
                colorscale="RdYlGn_r",
                colorbar=dict(
                    title=dict(text="Lost Energy (MWh)", font=dict(color="#9ca3af")),
                    tickfont=dict(color="#9ca3af"),
                ),
                hovertemplate="<b>Inverter:</b> %{y}<br>"
                + "<b>Combiner Box:</b> %{x}<br>"
                + "<b>Lost Energy:</b> %{z:,.1f} MWh<br>"
                + "<b>DC Capacity:</b> %{customdata[2]:,.1f} kW<br>"
                + "<b>Cost Impact:</b> $%{customdata[1]:,.1f}<br>"
                + "<b>Description:</b> %{customdata[0]}<extra></extra>",
            )
        )
        fig.update_layout(
            title=None,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#9ca3af", size=10, family="Inter"),
            margin=dict(l=10, r=40, t=20, b=10),
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=True,
                title=dict(text="COMBINER BOXES", font=dict(size=10)),
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                autorange="reversed",
                title=dict(text="INVERTERS", font=dict(size=10)),
            ),
            height=600,
        )
        return fig