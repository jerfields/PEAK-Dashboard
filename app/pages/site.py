import reflex as rx
from app.states.dashboard_state import DashboardState
from app.components.executive_summary import executive_summary_view
from app.components.priority_view import priority_view
from app.components.equipment_heatmap import equipment_heatmap_view
from app.components.key_metrics import key_metrics_view
from app.components.settings_modal import settings_modal


def site_info_card(
    label: str, value: str, icon: str, color: str = "text-cyan-400"
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name=f"h-4 w-4 {color}"),
            class_name="p-2 bg-white/5 rounded-lg",
        ),
        rx.el.div(
            rx.el.p(
                label,
                class_name="text-[10px] text-gray-500 font-bold uppercase tracking-wider",
            ),
            rx.el.p(value, class_name="text-sm text-white font-bold"),
            class_name="flex flex-col",
        ),
        class_name="flex items-center gap-3 px-4 py-2 bg-[#111827] border border-white/5 rounded-lg min-w-[140px]",
    )


def forecast_day(item: dict) -> rx.Component:
    return rx.el.div(
        rx.el.p(item["day"], class_name="text-[9px] text-gray-500 font-bold mb-1"),
        rx.icon(item["icon"].to(str), class_name="h-3 w-3 text-white mb-1"),
        rx.el.div(
            rx.el.span(
                f"{item['high']}°", class_name="text-[9px] text-white font-bold"
            ),
            rx.el.span(f"{item['low']}°", class_name="text-[9px] text-gray-500 ml-1"),
            class_name="flex",
        ),
        class_name="flex flex-col items-center",
    )


def site_header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "SITE OVERVIEW",
                    class_name="text-[10px] text-cyan-400 font-bold tracking-widest mb-1",
                ),
                rx.el.h1(
                    DashboardState.site_name,
                    class_name="text-2xl font-black text-white tracking-tight",
                ),
                class_name="flex flex-col mr-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "FROM", class_name="text-[10px] text-cyan-400 font-bold mb-1"
                    ),
                    rx.el.div(
                        rx.el.input(
                            type="date",
                            default_value=DashboardState.start_date,
                            on_change=DashboardState.set_start_date,
                            class_name="bg-transparent text-white text-xs border-none focus:ring-0 p-0 cursor-pointer w-24",
                        ),
                        rx.icon(
                            "calendar",
                            class_name="h-3 w-3 text-gray-400 absolute right-2 pointer-events-none",
                        ),
                        class_name="flex items-center relative bg-[#111827] border border-white/10 rounded px-2 py-1",
                    ),
                    class_name="flex flex-col",
                ),
                rx.el.div(
                    rx.el.p(
                        "TO", class_name="text-[10px] text-cyan-400 font-bold mb-1"
                    ),
                    rx.el.div(
                        rx.el.input(
                            type="date",
                            default_value=DashboardState.end_date,
                            on_change=DashboardState.set_end_date,
                            class_name="bg-transparent text-white text-xs border-none focus:ring-0 p-0 cursor-pointer w-24",
                        ),
                        rx.icon(
                            "calendar",
                            class_name="h-3 w-3 text-gray-400 absolute right-2 pointer-events-none",
                        ),
                        class_name="flex items-center relative bg-[#111827] border border-white/10 rounded px-2 py-1",
                    ),
                    class_name="flex flex-col",
                ),
                class_name="flex gap-2 items-center mr-8",
            ),
            rx.el.div(
                rx.el.p(
                    "SELECT SITE", class_name="text-[10px] text-cyan-400 font-bold mb-1"
                ),
                rx.el.div(
                    rx.el.select(
                        rx.foreach(
                            DashboardState.available_sites,
                            lambda s: rx.el.option(s, value=s),
                        ),
                        value=DashboardState.site_name,
                        on_change=lambda val: rx.redirect(f"/site/{val}"),
                        class_name="bg-[#111827] text-white text-xs border border-white/10 rounded px-3 py-1.5 w-48 appearance-none",
                    ),
                    rx.icon(
                        "chevron-down",
                        class_name="h-3 w-3 text-gray-400 absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none",
                    ),
                    class_name="relative",
                ),
                class_name="flex flex-col mr-auto",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            DashboardState.weather_location,
                            class_name="text-[10px] text-cyan-400 font-bold uppercase",
                        ),
                        rx.el.div(
                            rx.icon(
                                DashboardState.current_icon,
                                class_name="h-5 w-5 text-white mr-2",
                            ),
                            rx.el.span(
                                f"{DashboardState.current_temp}°C",
                                class_name="text-xl font-bold text-white",
                            ),
                            rx.el.span(
                                f"Feels {DashboardState.current_feels_like}°",
                                class_name="text-[10px] text-gray-500 ml-2",
                            ),
                            class_name="flex items-center",
                        ),
                        rx.el.p(
                            DashboardState.current_condition,
                            class_name="text-[10px] text-gray-400 font-bold uppercase",
                        ),
                        class_name="flex flex-col border-r border-white/10 pr-4 mr-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "droplets", class_name="h-3 w-3 text-cyan-400 mr-1"
                            ),
                            rx.el.span(
                                DashboardState.current_humidity,
                                class_name="text-[10px] text-gray-300",
                            ),
                            class_name="flex items-center mb-1",
                        ),
                        rx.el.div(
                            rx.icon("wind", class_name="h-3 w-3 text-cyan-400 mr-1"),
                            rx.el.span(
                                DashboardState.current_wind,
                                class_name="text-[10px] text-gray-300",
                            ),
                            class_name="flex items-center",
                        ),
                        class_name="flex flex-col mr-6 justify-center",
                    ),
                    class_name="flex items-center",
                ),
                rx.el.div(
                    rx.foreach(DashboardState.weather_forecast, forecast_day),
                    class_name="flex gap-3",
                ),
                class_name="flex items-center bg-[#0f141e] border border-white/10 p-2 rounded-lg",
            ),
            class_name="flex items-start mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    DashboardState.location,
                    class_name="text-xs text-gray-400 font-bold tracking-[0.2em] mr-8",
                ),
                rx.el.span(
                    f"POI: {DashboardState.poi_limit}",
                    class_name="text-xs text-gray-500 font-bold tracking-wider mr-6",
                ),
                rx.el.span(
                    f"AC: {DashboardState.ac_capacity}",
                    class_name="text-xs text-gray-500 font-bold tracking-wider mr-6",
                ),
                rx.el.span(
                    f"DC: {DashboardState.dc_capacity}",
                    class_name="text-xs text-gray-500 font-bold tracking-wider mr-6",
                ),
                rx.el.span(
                    f"LAT: {DashboardState.lat}",
                    class_name="text-xs text-gray-500 font-bold tracking-wider mr-6",
                ),
                rx.el.span(
                    f"LON: {DashboardState.lon}",
                    class_name="text-xs text-gray-500 font-bold tracking-wider",
                ),
                class_name="flex items-center uppercase",
            ),
            rx.el.div(
                site_info_card(
                    "STATUS", DashboardState.status, "circle_check", "text-cyan-400"
                ),
                site_info_card(
                    "CLIENT", DashboardState.client, "user", "text-gray-400"
                ),
                site_info_card(
                    "INCEPTION",
                    DashboardState.inception_date,
                    "calendar",
                    "text-gray-400",
                ),
                site_info_card(
                    "INVERTER", DashboardState.inverter_type, "cpu", "text-gray-400"
                ),
                class_name="flex gap-4",
            ),
            class_name="flex justify-between items-center pb-6 border-b border-white/10",
        ),
        class_name="px-8 pt-8",
    )


def tab_button(tab_name: str) -> rx.Component:
    is_active = DashboardState.active_tab == tab_name
    return rx.el.button(
        tab_name.upper(),
        on_click=lambda: DashboardState.set_tab(tab_name),
        class_name=rx.cond(
            is_active,
            "text-[11px] font-black text-cyan-400 border-b-2 border-cyan-400 pb-2 px-1 transition-all",
            "text-[11px] font-bold text-gray-500 hover:text-gray-300 pb-2 px-1 transition-all",
        ),
    )


def site_dashboard() -> rx.Component:
    from app.components.sidebar import sidebar

    return rx.el.main(
        sidebar(),
        settings_modal(),
        rx.el.div(
            site_header(),
            rx.el.div(
                rx.el.div(
                    rx.foreach(DashboardState.tabs, tab_button),
                    class_name="flex gap-8 px-8 mt-4 border-b border-white/5",
                ),
                rx.el.div(
                    rx.match(
                        DashboardState.active_tab,
                        ("Executive Summary", executive_summary_view()),
                        ("Priority View", priority_view()),
                        ("Equipment Heatmap", equipment_heatmap_view()),
                        ("Key Metrics Overview", key_metrics_view()),
                        rx.el.h3(
                            f"{DashboardState.active_tab} Content Placeholder",
                            class_name="text-gray-500 mt-12 text-center text-sm font-medium",
                        ),
                    ),
                    class_name="p-8",
                ),
                class_name="flex-1 overflow-auto",
            ),
            class_name="flex-1 flex flex-col min-w-0 w-full",
        ),
        class_name="flex min-h-screen bg-[#0a0f1a] font-['Inter'] w-full",
    )