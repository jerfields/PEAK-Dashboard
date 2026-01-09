import reflex as rx
from app.states.fleet_state import FleetState

TOOLTIP_PROPS = {
    "content_style": {
        "background": "#111827",
        "borderColor": "rgba(255,255,255,0.1)",
        "borderRadius": "8px",
        "color": "white",
        "fontSize": "12px",
    },
    "item_style": {"color": "#9ca3af"},
    "label_style": {"fontWeight": "bold", "marginBottom": "4px"},
    "separator": ": ",
}


def donut_legend_item(item: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            class_name=f"size-2 rounded-full", style={"backgroundColor": item["fill"]}
        ),
        rx.el.span(item["name"], class_name="text-[10px] text-gray-500 font-bold"),
        class_name="flex items-center gap-2",
    )


def site_distribution_chart() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "SITE DISTRIBUTION",
            class_name="text-center text-[10px] font-bold text-white tracking-widest mb-4",
        ),
        rx.el.div(
            rx.recharts.pie_chart(
                rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
                rx.recharts.pie(
                    rx.recharts.label_list(
                        data_key="value",
                        position="outside",
                        fill="#f59e0b",
                        font_size=12,
                        font_weight="bold",
                    ),
                    data=FleetState.site_distribution,
                    data_key="value",
                    name_key="name",
                    inner_radius="60%",
                    outer_radius="85%",
                    padding_angle=5,
                    stroke="transparent",
                    stroke_width=0,
                ),
                height=200,
            ),
            class_name="relative",
        ),
        rx.el.div(
            rx.foreach(FleetState.site_distribution, donut_legend_item),
            class_name="flex justify-center gap-4 mt-4",
        ),
        class_name="bg-[#111827]/50 p-6 rounded-2xl border border-white/5 h-full",
    )


def loss_breakdown_chart() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "FLEET LOSS BREAKDOWN (%)",
            class_name="text-center text-[10px] font-bold text-white tracking-widest mb-4",
        ),
        rx.el.div(
            rx.recharts.pie_chart(
                rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
                rx.recharts.pie(
                    rx.recharts.label_list(
                        data_key="value",
                        position="outside",
                        fill="#f59e0b",
                        font_size=12,
                        font_weight="bold",
                    ),
                    data=FleetState.loss_breakdown,
                    data_key="value",
                    name_key="name",
                    inner_radius="60%",
                    outer_radius="85%",
                    padding_angle=5,
                    stroke="transparent",
                    stroke_width=0,
                ),
                height=200,
            ),
            class_name="relative",
        ),
        rx.el.div(
            rx.foreach(FleetState.loss_breakdown, donut_legend_item),
            class_name="flex justify-center gap-4 mt-4 flex-wrap",
        ),
        class_name="bg-[#111827]/50 p-6 rounded-2xl border border-white/5 h-full",
    )