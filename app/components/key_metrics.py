import reflex as rx
from app.states.dashboard_state import DashboardState


def site_row(site: dict) -> rx.Component:
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
                            "OREGON",
                            class_name="text-[10px] text-gray-500 font-bold tracking-wider",
                        ),
                    ),
                    class_name="flex items-center",
                ),
                href=f"/site/{site['name']}",
                class_name="hover:opacity-80 transition-opacity",
            ),
            class_name="px-6 py-4 whitespace-nowrap flex items-center gap-2 group",
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
            site["availability"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-cyan-400 font-bold",
        ),
        rx.el.td(
            site["performance"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-purple-400 font-bold",
        ),
        rx.el.td(
            site["measured_energy"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-300 font-mono",
        ),
        rx.el.td(
            site["modeled_energy"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-300 font-mono",
        ),
        class_name="border-b border-white/5 hover:bg-white/5 transition-colors relative",
    )


def key_metrics_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "KEY METRICS OVERVIEW",
                class_name="text-xs font-bold text-white tracking-widest uppercase",
            ),
            rx.el.div(
                rx.icon("search", class_name="h-4 w-4 text-gray-500 mr-2"),
                rx.el.input(
                    placeholder="Search sites...",
                    on_change=DashboardState.set_site_search,
                    class_name="bg-transparent border-none text-sm text-white placeholder-gray-600 focus:ring-0 p-0 w-64",
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
                            class_name="px-6 py-3 text-left text-[10px] font-bold text-gray-500 uppercase tracking-wider",
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
                            class_name="px-6 py-3 text-left text-[10px] font-bold text-gray-500 uppercase tracking-wider",
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
                    rx.foreach(DashboardState.filtered_sites, site_row),
                    class_name="divide-y divide-white/5",
                ),
                class_name="w-full",
            ),
            class_name="bg-[#111827]/50 rounded-xl border border-white/5 overflow-hidden",
        ),
        class_name="flex flex-col animate-in fade-in duration-500",
    )