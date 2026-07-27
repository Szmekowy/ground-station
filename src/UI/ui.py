import dearpygui.dearpygui as dpg

# expected parameters
# - temperature
# - location (latiture, longitude)
# - altitude
# - atm. pressure

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400

class UI:
    _altitude_readings = []
    _pressure_readings = []
    _battery_readings = []

    def __init__(self):
        self.battery_series = None
        self.pressure_series = None
        self.altitude_series = None

        self._gui_ready = False

    def _cut_line_btn_pressed(self):
        return

    def _reset_graphs_btn_pressed(self):
        return

    def _create_main_view(self):
        dpg.add_text("Telemetry Data", color=[0, 200, 255])
        with dpg.subplots(rows=2, columns=2, width=-1, height=-30): 
            with dpg.plot(label="Battery (%)", height=-1, width=-1):
                dpg.add_plot_legend()
                dpg.add_plot_axis(dpg.mvXAxis, tag="battery_x")
                dpg.add_plot_axis(dpg.mvYAxis, tag="battery_y")
                self.battery_series = dpg.add_line_series([], [], parent="battery_y")

            with dpg.plot(label="Pressure (hPa)", height=-1, width=-1):
                dpg.add_plot_legend()
                dpg.add_plot_axis(dpg.mvXAxis, tag="pressure_x")
                dpg.add_plot_axis(dpg.mvYAxis, tag="pressure_y")
                self.pressure_series = dpg.add_line_series([], [], parent="pressure_y")

            with dpg.plot(label="Altitude (m)", height=-1, width=-1):
                dpg.add_plot_legend()
                dpg.add_plot_axis(dpg.mvXAxis, tag="altitude_x")
                dpg.add_plot_axis(dpg.mvYAxis, tag="altitude_y")
                self.altitude_series = dpg.add_line_series([], [], parent="altitude_y")

            with dpg.plot(label="GPS Coordinates", height=-1, width=-1):
                dpg.add_plot_legend()
                dpg.add_plot_axis(dpg.mvXAxis)
                dpg.add_plot_axis(dpg.mvYAxis)

        with dpg.group(horizontal=True, height=30):
            dpg.add_button(label="Cut the Line", callback=self._cut_line_btn_pressed)
            dpg.add_button(label="Reset Telemetry", callback=self._reset_graphs_btn_pressed)

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
            self._create_main_view()

        dpg.set_primary_window("main_window", True)
        dpg.setup_dearpygui()
        dpg.show_viewport()

        self._gui_ready = True

        dpg.start_dearpygui()
        dpg.destroy_context()

    def update_altitude(self, reading):
        self._altitude_readings.append(reading)
        if not self._gui_ready:
            return

        xs = [r['time'] for r in self._altitude_readings]
        ys = [r['altitude'] for r in self._altitude_readings]

        dpg.set_value(self.altitude_series, [xs, ys])
        dpg.fit_axis_data("altitude_x")
        dpg.fit_axis_data("altitude_y")

    def update_pressure(self, reading):
        self._pressure_readings.append(reading)
        if not self._gui_ready:
            return

        xs = [r['time'] for r in self._pressure_readings]
        ys = [r['pressure'] for r in self._pressure_readings]

        dpg.set_value(self.pressure_series, [xs, ys])
        dpg.fit_axis_data("pressure_x")
        dpg.fit_axis_data("pressure_y")

    def update_battery(self, reading):
        self._battery_readings.append(reading)
        if not self._gui_ready:
            return

        xs = [r['time'] for r in self._battery_readings]
        ys = [r['battery'] for r in self._battery_readings]

        dpg.set_value(self.battery_series, [xs, ys])
        dpg.fit_axis_data("battery_x")
        dpg.fit_axis_data("battery_y")

if __name__ == "__main__":
    ui = UI()
    ui.initialize_ui()
