import reflex as rx
from app.states.dashboard_state import DashboardState


def issue_card(label: str, count: int, icon: str = "alert-circle") -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                label.upper(),
                class_name="text-[10px] text-gray-500 font-bold tracking-widest uppercase mb-1",
            ),
            rx.el.h3(count, class_name="text-2xl font-bold text-red-500"),
            class_name="flex flex-col",
        ),
        rx.el.div(
            rx.icon(icon, class_name="h-5 w-5 text-red-900/50"),
            class_name="p-2 bg-red-500/10 rounded-lg border border-red-500/20",
        ),
        class_name="bg-[#111827]/50 border border-white/5 p-4 rounded-xl flex justify-between items-center",
    )


def priority_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "OUTSTANDING ISSUES",
                class_name="text-xs font-bold text-white tracking-widest mb-4",
            ),
            rx.el.div(
                issue_card("Inverter", DashboardState.outstanding_inverters),
                issue_card("Transformer", DashboardState.outstanding_transformers),
                issue_card("Breaker", DashboardState.outstanding_breakers),
                issue_card("Tracker Controller", DashboardState.outstanding_trackers),
                class_name="grid grid-cols-4 gap-4",
            ),
            class_name="mb-8",
        ),
        class_name="flex flex-col animate-in fade-in duration-500",
    )