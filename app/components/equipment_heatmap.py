import reflex as rx
from app.components.tracker_heatmap_plotly import tracker_heatmap_plotly
from app.components.combiner_box_heatmap import combiner_box_heatmap_plotly
from app.components.inverter_heatmap import inverter_heatmap_plotly


def equipment_heatmap_view() -> rx.Component:
    return rx.el.div(
        tracker_heatmap_plotly(),
        rx.el.div(class_name="mb-6"),
        combiner_box_heatmap_plotly(),
        rx.el.div(class_name="mb-6"),
        inverter_heatmap_plotly(),
        class_name="flex flex-col animate-in fade-in duration-500",
    )