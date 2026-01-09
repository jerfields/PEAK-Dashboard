import reflex as rx
from app.states.dashboard_state import DashboardState
from app.states.fleet_state import FleetState
from app.components.fleet_charts import site_distribution_chart, loss_breakdown_chart
from app.components.sidebar import sidebar
from app.pages.site import site_dashboard
from app.components.settings_modal import settings_modal


def fleet_kpi_card(
    label: str, value: str, icon: str, color: str = "text-cyan-400"
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                label.upper(),
                class_name="text-[10px] text-gray-500 font-bold tracking-widest mb-1",
            ),
            rx.el.div(
                rx.el.span(value, class_name="text-xl font-black text-white"),
                class_name="flex items-baseline gap-1",
            ),
            class_name="flex flex-col",
        ),
        rx.el.div(
            rx.icon(icon, class_name=f"h-4 w-4 {color}"),
            class_name="p-2 bg-white/5 rounded-lg",
        ),
        class_name="flex justify-between items-center p-6 bg-[#111827]/50 border border-white/5 rounded-2xl flex-1",
    )


def fleet_site_row(site: dict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.a(
                rx.el.div(
                    rx.icon("zap", class_name="h-4 w-4 text-cyan-500 mr-3"),
                    rx.el.div(
                        rx.el.span(
                            site["name"],
                            class_name="text-sm font-bold text-white block",
                        ),
                        rx.el.span(
                            site["location"],
                            class_name="text-[10px] text-gray-500 font-bold tracking-wider",
                        ),
                    ),
                    class_name="flex items-center",
                ),
                href=f"/site/{site['id']}",
                class_name="hover:opacity-80 transition-opacity",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                site["status"],
                class_name=f"px-2 py-1 rounded border border-white/10 text-[10px] font-bold tracking-wider {site['status_color']} bg-white/5",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            site["ac_capacity"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-400",
        ),
        rx.el.td(
            f"{site['availability']}%",
            class_name="px-6 py-4 whitespace-nowrap text-sm text-cyan-400 font-bold",
        ),
        rx.el.td(
            f"{site['performance']}%",
            class_name="px-6 py-4 whitespace-nowrap text-sm text-purple-400 font-bold",
        ),
        rx.el.td(
            f"{site['measured_energy']:,.1f} MWh",
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-300 font-mono",
        ),
        rx.el.td(
            f"{site['modeled_energy']:,.1f} MWh",
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-300 font-mono",
        ),
        class_name="border-b border-white/5 hover:bg-white/5 transition-colors",
    )


def fleet_header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "FLEET OVERVIEW",
                    class_name="text-2xl font-black text-white tracking-tight",
                ),
                rx.el.p(
                    "ASSET PERFORMANCE MONITORING",
                    class_name="text-[10px] text-cyan-400 font-bold tracking-widest",
                ),
                class_name="flex flex-col",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        FleetState.weather_location,
                        class_name="text-[10px] text-cyan-400 font-bold mb-1",
                    ),
                    rx.el.div(
                        rx.icon(
                            FleetState.weather_icon,
                            class_name="h-5 w-5 text-white mr-3",
                        ),
                        rx.el.div(
                            rx.el.span(
                                FleetState.current_temp,
                                class_name="text-xl font-bold text-white leading-none",
                            ),
                            rx.el.span(
                                FleetState.current_condition,
                                class_name="text-[9px] text-gray-400 font-bold tracking-wider",
                            ),
                            class_name="flex flex-col",
                        ),
                        class_name="flex items-center border-r border-white/10 pr-4 mr-4",
                    ),
                    class_name="flex",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon("droplets", class_name="h-3 w-3 text-cyan-400 mr-1"),
                        rx.el.span(
                            FleetState.current_humidity,
                            class_name="text-[10px] text-gray-300",
                        ),
                        class_name="flex items-center mb-1",
                    ),
                    rx.el.div(
                        rx.icon("wind", class_name="h-3 w-3 text-cyan-400 mr-1"),
                        rx.el.span(
                            FleetState.current_wind,
                            class_name="text-[10px] text-gray-300",
                        ),
                        class_name="flex items-center",
                    ),
                    class_name="flex flex-col justify-center",
                ),
                class_name="flex bg-[#0f141e] border border-white/10 p-2 rounded-lg items-center",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "FROM", class_name="text-[10px] text-cyan-400 font-bold mb-1"
                    ),
                    rx.el.div(
                        rx.el.input(
                            type="date",
                            default_value=FleetState.start_date,
                            on_change=FleetState.set_start_date,
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
                            default_value=FleetState.end_date,
                            on_change=FleetState.set_end_date,
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
                rx.el.button(
                    rx.icon("filter", class_name="h-4 w-4 mr-2"),
                    "FILTERS",
                    class_name="flex items-center bg-[#111827] text-cyan-400 text-xs font-bold px-4 py-3 rounded border border-white/10 hover:bg-white/5 transition-colors h-full mt-auto",
                ),
                class_name="flex gap-2 items-end",
            ),
            class_name="flex justify-between items-center mb-8 px-8 pt-8",
        )
    )


def fleet_overview() -> rx.Component:
    return rx.el.main(
        sidebar(),
        settings_modal(),
        rx.el.div(
            fleet_header(),
            rx.el.div(
                rx.el.div(
                    fleet_kpi_card(
                        "Total Sites", f"{FleetState.total_sites} Sites", "layout-grid"
                    ),
                    fleet_kpi_card(
                        "Availability",
                        f"{FleetState.avg_availability}%",
                        "zap",
                        "text-cyan-400",
                    ),
                    fleet_kpi_card(
                        "Performance",
                        f"{FleetState.avg_performance}%",
                        "activity",
                        "text-purple-400",
                    ),
                    fleet_kpi_card(
                        "Total Measured Energy",
                        f"{FleetState.total_measured_energy:,.0f} MWh",
                        "zap-off",
                        "text-cyan-400",
                    ),
                    fleet_kpi_card(
                        "Total Lost Energy",
                        f"{FleetState.total_lost_energy:,.0f} MWh",
                        "trending-down",
                        "text-red-400",
                    ),
                    class_name="grid grid-cols-5 gap-4 mb-6",
                ),
                rx.el.div(
                    rx.el.div(site_distribution_chart(), class_name="col-span-1"),
                    rx.el.div(loss_breakdown_chart(), class_name="col-span-1"),
                    class_name="grid grid-cols-2 gap-6 mb-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "KEY METRICS OVERVIEW",
                            class_name="text-xs font-bold text-white tracking-widest uppercase",
                        ),
                        rx.el.div(
                            rx.icon("search", class_name="h-4 w-4 text-gray-500 mr-2"),
                            rx.el.input(
                                placeholder="Search sites...",
                                on_change=FleetState.set_search,
                                class_name="bg-transparent border-none text-sm text-white focus:ring-0 p-0 w-64",
                            ),
                            class_name="flex items-center bg-[#111827] border border-white/10 rounded-lg px-3 py-1.5",
                        ),
                        class_name="flex justify-between items-center mb-6",
                    ),
                    rx.el.div(
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    rx.el.th(
                                        "Site Name",
                                        class_name="px-6 py-3 text-left text-[10px] font-bold text-gray-500 uppercase tracking-wider cursor-pointer",
                                        on_click=lambda: FleetState.toggle_sort("name"),
                                    ),
                                    rx.el.th(
                                        "Status",
                                        class_name="px-6 py-3 text-left text-[10px] font-bold text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "AC Capacity",
                                        class_name="px-6 py-3 text-left text-[10px] font-bold text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Availability",
                                        class_name="px-6 py-3 text-left text-[10px] font-bold text-gray-500 uppercase tracking-wider cursor-pointer",
                                        on_click=lambda: FleetState.toggle_sort(
                                            "availability"
                                        ),
                                    ),
                                    rx.el.th(
                                        "Performance",
                                        class_name="px-6 py-3 text-left text-[10px] font-bold text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Measured Energy",
                                        class_name="px-6 py-3 text-left text-[10px] font-bold text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Modeled Energy",
                                        class_name="px-6 py-3 text-left text-[10px] font-bold text-gray-500 uppercase tracking-wider",
                                    ),
                                ),
                                class_name="bg-black/20",
                            ),
                            rx.el.tbody(
                                rx.foreach(FleetState.filtered_sites, fleet_site_row),
                                class_name="divide-y divide-white/5",
                            ),
                            class_name="w-full table-auto",
                        ),
                        class_name="bg-[#111827]/50 rounded-xl border border-white/5 overflow-auto max-h-[600px]",
                    ),
                ),
                class_name="px-8",
            ),
            class_name="flex-1 overflow-auto",
        ),
        class_name="flex min-h-screen bg-[#0a0f1a] font-['Inter']",
        on_mount=FleetState.load_fleet_data,
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(fleet_overview, route="/", on_load=FleetState.load_fleet_data)
app.add_page(
    site_dashboard, route="/site/[site_id]", on_load=DashboardState.load_site_data
)