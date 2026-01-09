import reflex as rx
from app.states.dashboard_state import DashboardState


def settings_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/80 backdrop-blur-sm z-[100]"
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.el.div(
                        rx.radix.primitives.dialog.title(
                            "SETTINGS",
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
                        class_name="flex justify-between items-center mb-8 pb-4 border-b border-white/10",
                    ),
                    rx.el.div(
                        rx.el.h4(
                            "ADJUSTMENT FACTORS",
                            class_name="text-[10px] font-black text-cyan-400 tracking-[0.2em] mb-4",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.label(
                                    "SOILING LOSS (%)",
                                    class_name="text-[10px] text-gray-500 font-bold mb-1.5",
                                ),
                                rx.el.input(
                                    type="number",
                                    default_value=DashboardState.soiling_loss_pct.to_string(),
                                    on_change=DashboardState.set_soiling_loss.debounce(
                                        300
                                    ),
                                    class_name="w-full bg-[#0a0f1a] border border-white/10 rounded-lg px-4 py-2.5 text-sm text-white focus:ring-1 focus:ring-cyan-500/50 outline-none transition-all",
                                ),
                                class_name="flex flex-col",
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "VEGETATION LOSS (%)",
                                    class_name="text-[10px] text-gray-500 font-bold mb-1.5",
                                ),
                                rx.el.input(
                                    type="number",
                                    default_value=DashboardState.vegetation_loss_pct.to_string(),
                                    on_change=DashboardState.set_vegetation_loss.debounce(
                                        300
                                    ),
                                    class_name="w-full bg-[#0a0f1a] border border-white/10 rounded-lg px-4 py-2.5 text-sm text-white focus:ring-1 focus:ring-cyan-500/50 outline-none transition-all",
                                ),
                                class_name="flex flex-col",
                            ),
                            class_name="grid grid-cols-2 gap-4",
                        ),
                        class_name="mb-8",
                    ),
                    rx.el.div(
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                "SAVE CHANGES",
                                class_name="w-full bg-cyan-500 hover:bg-cyan-600 text-[#0a0f1a] font-black text-xs py-3 rounded-lg transition-all tracking-widest",
                            )
                        ),
                        class_name="pt-4 border-t border-white/10",
                    ),
                    class_name="bg-[#111827] border border-white/10 rounded-2xl p-8 w-full max-w-md shadow-2xl",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-[101] w-full max-w-md",
            ),
        ),
        open=DashboardState.show_settings_modal,
        on_open_change=DashboardState.toggle_settings_modal,
    )