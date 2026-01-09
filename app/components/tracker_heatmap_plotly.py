import reflex as rx
from app.states.dashboard_state import DashboardState


def tracker_issue_row(issue: dict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            issue["motor"], class_name="px-4 py-2 text-xs text-cyan-400 font-mono"
        ),
        rx.el.td(
            issue["controller"],
            class_name="px-4 py-2 text-xs text-gray-500 font-medium",
        ),
        rx.el.td(
            f"{issue['dc_capacity']} kW",
            class_name="px-4 py-2 text-xs text-gray-400 font-bold",
        ),
        rx.el.td(
            f"{issue['lost_energy']} kWh",
            class_name="px-4 py-2 text-xs text-orange-400 font-bold",
        ),
        class_name="border-b border-white/5 hover:bg-white/5 transition-colors",
    )


def tracker_issues_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/80 backdrop-blur-sm z-40"
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.el.div(
                        rx.radix.primitives.dialog.title(
                            "TRACKER MOTORS WITH ISSUES",
                            class_name="text-sm font-black text-white tracking-widest",
                        ),
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                rx.icon(
                                    "x",
                                    class_name="h-4 w-4 text-gray-400 hover:text-white",
                                ),
                                class_name="p-1 hover:bg-white/10 rounded-md transition-colors",
                            )
                        ),
                        class_name="flex justify-between items-center mb-6",
                    ),
                    rx.el.div(
                        rx.icon("search", class_name="h-4 w-4 text-gray-500 mr-2"),
                        rx.el.input(
                            placeholder="Search motors or controllers...",
                            on_change=DashboardState.set_tracker_modal_search,
                            class_name="bg-transparent border-none text-sm text-white focus:ring-0 p-0 w-full",
                        ),
                        class_name="flex items-center bg-[#0a0f1a] border border-white/10 rounded-lg px-3 py-2 mb-4",
                    ),
                    rx.el.div(
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    rx.el.th(
                                        "Motor ID",
                                        class_name="px-4 py-2 text-left text-[10px] font-bold text-gray-500 uppercase tracking-widest",
                                    ),
                                    rx.el.th(
                                        "Controller ID",
                                        class_name="px-4 py-2 text-left text-[10px] font-bold text-gray-500 uppercase tracking-widest",
                                    ),
                                    rx.el.th(
                                        "Impacted DC Capacity",
                                        class_name="px-4 py-2 text-left text-[10px] font-bold text-gray-500 uppercase tracking-widest",
                                    ),
                                    rx.el.th(
                                        "Total Lost Energy",
                                        class_name="px-4 py-2 text-left text-[10px] font-bold text-gray-500 uppercase tracking-widest",
                                    ),
                                )
                            ),
                            rx.el.tbody(
                                rx.foreach(
                                    DashboardState.motors_with_issues_list,
                                    tracker_issue_row,
                                )
                            ),
                            class_name="w-full table-auto",
                        ),
                        class_name="max-h-[60vh] overflow-y-auto border border-white/5 rounded-lg bg-black/20",
                    ),
                    class_name="bg-[#111827] border border-white/10 rounded-2xl p-6 w-full max-w-3xl",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-[100] w-full max-w-3xl",
            ),
        ),
        open=DashboardState.show_tracker_modal,
        on_open_change=DashboardState.toggle_tracker_modal,
    )


def tracker_kpi_card(
    label: str,
    value: rx.Var,
    icon: str,
    color: str,
    on_click: rx.event.EventType = rx.noop(),
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                label,
                class_name="text-[10px] text-gray-500 font-bold uppercase tracking-widest mb-1",
            ),
            rx.el.h4(value, class_name=f"text-lg font-black {color}"),
            class_name="flex flex-col",
        ),
        rx.el.div(
            rx.icon(icon, class_name=f"h-5 w-5 {color} opacity-70"),
            class_name="p-2 bg-white/5 rounded-lg",
        ),
        on_click=on_click,
        class_name=rx.cond(
            on_click != rx.noop(),
            "flex flex-1 justify-between items-center p-4 bg-[#111827]/50 border border-white/5 rounded-xl cursor-pointer hover:bg-white/10 transition-colors",
            "flex flex-1 justify-between items-center p-4 bg-[#111827]/50 border border-white/5 rounded-xl",
        ),
    )


def tracker_heatmap_plotly() -> rx.Component:
    return rx.el.div(
        tracker_issues_modal(),
        rx.el.div(
            rx.el.h3(
                "TRACKER MOTOR HEATMAP",
                class_name="text-lg font-bold text-white tracking-widest uppercase",
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            tracker_kpi_card(
                "Motors with Issues",
                DashboardState.tracker_motors_with_issues.to_string(),
                "circle_alert",
                "text-red-500",
                on_click=DashboardState.toggle_tracker_modal,
            ),
            tracker_kpi_card(
                "Total Lost Energy",
                f"{DashboardState.tracker_total_lost_energy:.1f} MWh",
                "zap-off",
                "text-orange-500",
            ),
            tracker_kpi_card(
                "Total Lost Revenue",
                f"${DashboardState.tracker_total_lost_revenue:,.0f}",
                "dollar-sign",
                "text-green-500",
            ),
            tracker_kpi_card(
                "Most Problematic Controller",
                DashboardState.tracker_most_problematic_controller,
                "triangle_alert",
                "text-yellow-500",
            ),
            class_name="grid grid-cols-4 gap-4 mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.plotly(data=DashboardState.tracker_heatmap_fig, class_name="w-full"),
                class_name="bg-black/20 rounded-xl border border-white/5 p-4",
            ),
            class_name="flex flex-col relative",
        ),
        class_name="flex flex-col animate-in fade-in duration-700",
    )