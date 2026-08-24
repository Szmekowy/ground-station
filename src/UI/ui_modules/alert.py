import dearpygui.dearpygui as dpg
from enum import Enum, auto
# from collections.abc import Callable


class AlertType(Enum):
    LOW_BATTERY = auto()


class AlertManager:
    _width, _height = 300, 150
    _pos_x, _pos_y = 300, 150

    _alert_tags: dict = {
        AlertType.LOW_BATTERY: "low_battery_alert"
    }

    _silenced_alerts: set[AlertType] = set([])

    @classmethod
    def initialize(cls):
        cls.initialize_low_battery_alert()

    @classmethod
    def show_alert(cls, alert_type: AlertType):
        if alert_type in cls._silenced_alerts:
            return

        tag = cls.get_alert_tag(alert_type)
        dpg.configure_item(tag, show=True)

    @classmethod
    def hide_alert(cls, alert_type: AlertType):
        tag = cls.get_alert_tag(alert_type)
        dpg.configure_item(tag, show=False)

    @classmethod
    def get_alert_tag(cls, alert_type: AlertType) -> str:
        return cls._alert_tags.get(alert_type)

    @classmethod
    def initialize_low_battery_alert(cls) -> None:
        with dpg.window(
            label="Low Battery",
            tag=cls.get_alert_tag(AlertType.LOW_BATTERY),
            modal=True,
            pos=[cls._pos_x, cls._pos_y],
            width=cls._width,
            height=cls._height,
            show=False
        ):
            dpg.add_text("Connect power supply")
            with dpg.group():
                # tag = cls._alert_tags.get(AlertType.LOW_BATTERY)

                def _on_low_battery_alert_ok():
                    cls.hide_alert(AlertType.LOW_BATTERY)

                def _on_low_battery_alert_dont_show():
                    cls._silenced_alerts.add(AlertType.LOW_BATTERY)
                    cls.hide_alert(AlertType.LOW_BATTERY)

                dpg.add_button(label="Ok", callback=_on_low_battery_alert_ok)
                dpg.add_button(label="Don't show again", callback=_on_low_battery_alert_dont_show)

