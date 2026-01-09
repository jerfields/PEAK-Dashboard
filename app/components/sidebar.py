import reflex as rx
from app.states.dashboard_state import DashboardState


def nav_item(item: dict[str, str]) -> rx.Component:
    is_settings = item["label"] == "SETTINGS"
    return rx.el.a(
        rx.icon(item["icon"].to(str), class_name="h-4 w-4"),
        rx.el.span(item["label"], class_name="text-xs font-semibold"),
        href=rx.cond(is_settings, "#", item["href"]),
        on_click=rx.cond(is_settings, DashboardState.toggle_settings_modal, rx.noop()),
        class_name="flex items-center gap-3 px-4 py-3 text-gray-400 hover:text-cyan-400 hover:bg-white/5 transition-colors border-l-2 border-transparent hover:border-cyan-400 cursor-pointer",
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "PEAK Δ",
                    class_name="text-cyan-400 font-bold text-2xl tracking-wider",
                ),
                rx.el.p(
                    "SOLV ENERGY",
                    class_name="text-gray-500 text-[15px] font-bold tracking-[0.2em]",
                ),
                rx.el.button(
                    rx.icon("chevron-left", class_name="h-4 w-4"),
                    class_name="absolute right-4 top-6 text-gray-500 hover:text-white p-1 rounded-md border border-white/10",
                ),
                class_name="p-6 border-b border-white/10 mb-4 relative",
            ),
            rx.el.nav(
                rx.el.div(
                    "MONITORING & ANALYTICS",
                    class_name="px-6 py-2 text-[10px] text-cyan-500 font-bold tracking-widest mb-2",
                ),
                rx.foreach(
                    DashboardState.nav_sections["MONITORING & ANALYTICS"], nav_item
                ),
                rx.el.div(
                    "SYSTEM",
                    class_name="px-6 py-2 text-[10px] text-cyan-500 font-bold tracking-widest mt-6 mb-2",
                ),
                rx.foreach(DashboardState.nav_sections["SYSTEM"], nav_item),
                class_name="flex flex-col flex-1 overflow-y-auto",
            ),
            class_name="flex flex-col h-full",
        ),
        class_name="w-64 bg-[#0a0f1a] border-r border-white/10 h-screen sticky top-0 shrink-0",
    )