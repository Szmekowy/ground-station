import dearpygui.dearpygui as dpg
from ui_modules.alert import AlertManager, AlertType

from ui_modules.panels.panel import PanelType

class MainPanel:
    battery_series = None
    pressure_series = None
    altitude_series = None

    @classmethod
    def initialize(cls):
        with dpg.group(tag=PanelType.MainPanel):
            with dpg.subplots(rows=2, columns=2, width=-1, height=-30):
                with dpg.plot(label="Pressure (hPa)", height=-1, width=-1):
                    dpg.add_plot_legend()
                    dpg.add_plot_axis(dpg.mvXAxis, tag="pressure_x")
                    dpg.add_plot_axis(dpg.mvYAxis, tag="pressure_y")
                    cls.pressure_series = dpg.add_line_series([], [], parent="pressure_y")

                with dpg.plot(label="Altitude (m)", height=-1, width=-1):
                    dpg.add_plot_legend()
                    dpg.add_plot_axis(dpg.mvXAxis, tag="altitude_x")
                    dpg.add_plot_axis(dpg.mvYAxis, tag="altitude_y")
                    cls.altitude_series = dpg.add_line_series([], [], parent="altitude_y")

                with dpg.plot(label="GPS Coordinates", height=-1, width=-1):
                    dpg.add_plot_legend()
                    dpg.add_plot_axis(dpg.mvXAxis)
                    dpg.add_plot_axis(dpg.mvYAxis)

            with dpg.group(horizontal=True, height=30):
                dpg.add_button(label="Cut the Line", callback=cls._cut_line_btn_pressed)
                dpg.add_button(label="Reset Telemetry", callback=cls._reset_graphs_btn_pressed)

    @classmethod
    def _cut_line_btn_pressed(cls):
        AlertManager.show_alert(AlertType.CUT_LINE_CONFIRMATION)

    @classmethod
    def _reset_graphs_btn_pressed(cls):
        return
