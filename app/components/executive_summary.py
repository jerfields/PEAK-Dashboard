import reflex as rx
from app.states.dashboard_state import DashboardState


def summary_card(
    label: str, value: rx.Var | str, icon: str, trend_color: str
) -> rx.Component:
    return rx.el.div(
        rx.el.p(
            label,
            class_name="text-[9px] text-gray-500 font-bold uppercase tracking-widest mb-1",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon(icon, class_name=f"h-3 w-3 {trend_color} mr-1.5"),
                class_name="flex items-center",
            ),
            rx.el.span(value, class_name=f"text-lg font-bold {trend_color}"),
            class_name="flex items-center",
        ),
        class_name="bg-[#111827] border border-white/5 p-3 rounded-xl flex flex-col justify-center",
    )


def loss_driver_row(driver: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(driver["name"], class_name="text-xs text-gray-400 font-medium"),
            rx.el.span(
                driver["display_value"],
                class_name="text-xs text-white font-bold tabular-nums",
            ),
            class_name="flex justify-between mb-2",
        ),
        rx.el.div(
            rx.el.div(
                class_name=f"h-full rounded-full {driver['color']}",
                style={"width": f"{driver['width_pct']}%"},
            ),
            class_name="h-1.5 w-full bg-gray-800 rounded-full overflow-hidden",
        ),
        class_name="flex flex-col mb-4",
    )


def operational_summary_section() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "OPERATIONAL SUMMARY",
            class_name="text-xs font-bold text-white mb-4 tracking-widest",
        ),
        rx.el.div(
            summary_card(
                "Measured Energy",
                f"{DashboardState.measured_energy:,.1f} MWh",
                icon="zap",
                trend_color="text-cyan-400",
            ),
            summary_card(
                "Expected Energy",
                f"{DashboardState.expected_energy:,.1f} MWh",
                icon="target",
                trend_color="text-gray-400",
            ),
            summary_card(
                "Curtailed Energy",
                f"{DashboardState.curtailed_energy:,.1f} MWh",
                icon="scissors",
                trend_color="text-yellow-400",
            ),
            summary_card(
                "Availability",
                f"{DashboardState.availability}%",
                icon="check-circle",
                trend_color="text-green-400",
            ),
            summary_card(
                "Performance",
                f"{DashboardState.performance}%",
                icon="activity",
                trend_color="text-purple-400",
            ),
            summary_card(
                "Total Lost Energy",
                f"{DashboardState.total_lost_energy:,.1f} MWh",
                icon="trending-down",
                trend_color="text-red-400",
            ),
            class_name="grid grid-cols-6 gap-3 mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h4(
                    "OBSERVATION AND RECOMMENDATION",
                    class_name="text-xs font-black text-cyan-400 tracking-[0.2em] mb-4",
                ),
                rx.el.div(
                    rx.foreach(
                        DashboardState.dynamic_summary,
                        lambda line: rx.el.p(
                            line, class_name="text-sm text-gray-300 leading-loose mb-3"
                        ),
                    ),
                    class_name="flex flex-col",
                ),
                class_name="w-full",
            ),
            class_name="flex flex-col bg-cyan-950/20 border border-cyan-500/20 p-8 rounded-xl flex-1",
        ),
        class_name="flex flex-col h-full bg-[#111827]/50 p-6 rounded-2xl border border-white/5",
    )


def loss_drivers_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "PRIMARY LOSS DRIVERS",
                class_name="text-xs font-bold text-white tracking-widest",
            ),
            rx.el.div(
                rx.el.button(
                    "LOSS %",
                    on_click=lambda: DashboardState.set_loss_driver_unit("%"),
                    class_name=rx.cond(
                        DashboardState.loss_driver_unit == "%",
                        "px-3 py-1 text-[9px] font-bold bg-cyan-500 text-white rounded-l",
                        "px-3 py-1 text-[9px] font-bold bg-[#1f2937] text-gray-400 rounded-l hover:bg-[#374151]",
                    ),
                ),
                rx.el.button(
                    "ENERGY (MWh)",
                    on_click=lambda: DashboardState.set_loss_driver_unit("MWh"),
                    class_name=rx.cond(
                        DashboardState.loss_driver_unit == "MWh",
                        "px-3 py-1 text-[9px] font-bold bg-cyan-500 text-white",
                        "px-3 py-1 text-[9px] font-bold bg-[#1f2937] text-gray-400 hover:bg-[#374151]",
                    ),
                ),
                rx.el.button(
                    "REVENUE ($)",
                    on_click=lambda: DashboardState.set_loss_driver_unit("$"),
                    class_name=rx.cond(
                        DashboardState.loss_driver_unit == "$",
                        "px-3 py-1 text-[9px] font-bold bg-cyan-500 text-white rounded-r",
                        "px-3 py-1 text-[9px] font-bold bg-[#1f2937] text-gray-400 rounded-r hover:bg-[#374151]",
                    ),
                ),
                class_name="flex",
            ),
            class_name="flex justify-between items-center mb-6",
        ),
        rx.el.div(
            rx.foreach(DashboardState.loss_drivers, loss_driver_row),
            class_name="flex flex-col",
        ),
        class_name="bg-[#111827]/50 p-6 rounded-2xl border border-white/5 h-full",
    )


def waterfall_chart_section() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "ENERGY WATERFALL & LOSS PROFILE",
                class_name="text-xs font-bold text-white tracking-widest mb-2",
            ),
            class_name="flex justify-between items-center",
        ),
        rx.el.div(
            rx.plotly(data=DashboardState.waterfall_plotly_fig, class_name="w-full"),
            class_name="w-full -mt-2",
        ),
        class_name="bg-[#111827]/50 p-6 rounded-2xl border border-white/5 mt-6",
    )


def executive_summary_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(operational_summary_section(), class_name="col-span-2"),
            rx.el.div(loss_drivers_panel(), class_name="col-span-1"),
            class_name="grid grid-cols-3 gap-6",
        ),
        waterfall_chart_section(),
        class_name="flex flex-col",
    )