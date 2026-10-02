import dearpygui.dearpygui as dpg
from ui_modules.alert import AlertManager, AlertType
from ui_modules.topbar import Topbar

from ui_modules.panels.panel import PanelType
from ui_modules.panels.main_panel import MainPanel
from ui_modules.panels.settings_panel import SettingsPanel

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400

LOW_BATTERY_THRESHOLD = 60.0



class UI:
    _altitude_readings = []
    _pressure_readings = []

    panels = [
        PanelType.MainPanel,
        PanelType.SettingsPanel
    ]

    def __init__(self):
        self._gui_ready = False

    def switch_panel(self, panel_type: PanelType):
        for panel in self.panels:
            dpg.configure_item(panel, show=(panel == panel_type))

    def initialize_ui(self):
        dpg.create_context()
        dpg.create_viewport(
            title='Pi Dashboard',
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            min_width=WINDOW_WIDTH,
            max_width=WINDOW_WIDTH,
            min_height=WINDOW_HEIGHT,
            max_height=WINDOW_HEIGHT,
            resizable=False
        )

        with dpg.window(tag="main_window"):
            Topbar.initialize()
            with dpg.group(horizontal=True):
                # Vertical navbar on the left side
                with dpg.group(width=50):
                    dpg.add_button(label="Main", callback = lambda: self.switch_panel(PanelType.MainPanel))
                    dpg.add_button(label="Settings", callback = lambda: self.switch_panel(PanelType.SettingsPanel))

                # Panels on the right
                with dpg.group():
                    MainPanel.initialize()
                    SettingsPanel.initialize()

        dpg.set_primary_window("main_window", True)
        dpg.setup_dearpygui()
        dpg.show_viewport()

        AlertManager.cut_line_confirmation_callback = send_cut_line_request

        AlertManager.initialize()
        self.switch_panel(PanelType.MainPanel)

        self._gui_ready = True

        while dpg.is_dearpygui_running():
            Topbar.update_time()
            dpg.render_dearpygui_frame()
        dpg.destroy_context()

    def update_altitude(self, reading):
        self._altitude_readings.append(reading)
        if not self._gui_ready:
            return

        xs = [r['time'] for r in self._altitude_readings]
        ys = [r['altitude'] for r in self._altitude_readings]

        dpg.set_value(MainPanel.altitude_series, [xs, ys])
        dpg.fit_axis_data("altitude_x")
        dpg.fit_axis_data("altitude_y")

    def update_pressure(self, reading):
        self._pressure_readings.append(reading)
        if not self._gui_ready:
            return

        xs = [r['time'] for r in self._pressure_readings]
        ys = [r['pressure'] for r in self._pressure_readings]

        dpg.set_value(MainPanel.pressure_series, [xs, ys])
        dpg.fit_axis_data("pressure_x")
        dpg.fit_axis_data("pressure_y")

    def update_battery(self, reading):
        if not self._gui_ready:
            return

        Topbar.update_battery(reading)

        if reading <= LOW_BATTERY_THRESHOLD:
            self._on_low_battery(reading)

    def _on_low_battery(self, battery_level: float):
        AlertManager.show_alert(AlertType.LOW_BATTERY)


if __name__ == "__main__":
    ui = UI()
    ui.initialize_ui()


def send_cut_line_request():
    print("Line was cut")
