import dearpygui.dearpygui as dpg

from ui_modules.panels.panel import PanelType


class SettingsPanel:
    @classmethod
    def initialize(cls):
        with dpg.group(tag=PanelType.SettingsPanel):
            dpg.add_text("Settings", pos=(350, 30))
