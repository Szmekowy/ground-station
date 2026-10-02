import dearpygui.dearpygui as dpg
from datetime import datetime
from zoneinfo import ZoneInfo


class Topbar:
    _timezone = ZoneInfo("Europe/Warsaw")
    _start_time = datetime.now(_timezone)

    @classmethod
    def initialize(cls):
        with dpg.group(horizontal=True, horizontal_spacing=220):
            dpg.add_text("Telemetry Data", color=[0, 200, 255])
            with dpg.group(horizontal=True):
                dpg.add_text("", tag="clock_label")
                dpg.add_text("", tag="uptime_label", color=[0, 200, 255])
            dpg.add_text("Battery: ", tag="battery_label")

    @classmethod
    def update_battery(cls, new_value: float):
        dpg.set_value("battery_label", f"Battery: {new_value:.1f}%")

    @classmethod
    def update_time(cls):
        current_time = datetime.now(cls._timezone).strftime("%H:%M:%S")
        uptime = datetime.now(cls._timezone) - cls._start_time

        # strip microseconds at the end
        uptime_str = str(uptime).split(".")[0]
        dpg.set_value("clock_label", current_time)
        dpg.set_value("uptime_label", uptime_str)
