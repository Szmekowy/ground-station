import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import sys

# expected parameters
# - temperature
# - location (latiture, longitude)
# - altitude
# - atm. pressure


class UI:
    figure: plt.Figure
    temperature_plt: plt.Axes
    location_plt: plt.Axes
    altitude_plt: plt.Axes
    pressure_plt: plt.Axes

    def __init__(self):
        pass

    def initialize_ui(self):
        plt.ion()
        f, ax = plt.subplots(2, 2)

        self.figure = f
        self.figure.set_layout_engine('tight')

        self.temperature_plt = ax[0, 0]
        self.location_plt = ax[1, 0]
        self.altitude_plt = ax[0, 1]
        self.pressure_plt = ax[1, 1]

        (self.temp_line,) = self.temperature_plt.plot([], [])
        (self.alt_line,) = self.altitude_plt.plot([], [])
        (self.location_line,) = self.location_plt.plot([], [])
        (self.pressure_line,) = self.pressure_plt.plot([], [])

        self.temperature_plt.set_title("Temperature [°C]")
        self.altitude_plt.set_title("Altitude [m]")
        self.pressure_plt.set_title("Pressure [hPa]")
        self.location_plt.set_title("Location")
        self.location_plt.set_xlabel("Longitude")
        self.location_plt.set_ylabel("Latitude")

        self._set_time_formatting(self.temperature_plt)
        self._set_time_formatting(self.altitude_plt)
        self._set_time_formatting(self.pressure_plt)
        self._set_location_formatting()

        self.figure.canvas.mpl_connect('close_event', _on_plot_closed)

        plt.show()
        plt.pause(1)

    def _set_time_formatting(self, ax: plt.Axes):
        # properly format timestamps on x axis and rotate them 30 degrees
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.tick_params(axis='x', labelrotation=30, labelbottom=True)

    def _set_location_formatting(self):
        self.location_plt.set_aspect('equal', adjustable='datalim')

    def redraw_plots(self):
        plt.draw()
        plt.pause(0.1)

    def update_temperature(self, readings: list):
        xs = [reading['time'] for reading in readings]
        ys = [reading['temp'] for reading in readings]
        self.temp_line.set_xdata(xs)
        self.temp_line.set_ydata(ys)

        self.temperature_plt.relim()
        self.temperature_plt.autoscale_view()

        self.redraw_plots()

    def update_altitude(self, readings: list):
        xs = [reading['time'] for reading in readings]
        ys = [reading['alt'] for reading in readings]
        self.alt_line.set_xdata(xs)
        self.alt_line.set_ydata(ys)

        self.altitude_plt.relim()
        self.altitude_plt.autoscale_view()

        self.redraw_plots()

    def update_pressure(self, readings: list):
        xs = [reading['time'] for reading in readings]
        ys = [reading['pressure'] for reading in readings]
        self.pressure_line.set_xdata(xs)
        self.pressure_line.set_ydata(ys)

        self.pressure_plt.relim()
        self.pressure_plt.autoscale_view()

        self.redraw_plots()

    def update_location(self, readings: list):
        xs = [reading['longitude'] for reading in readings]
        ys = [reading['latitude'] for reading in readings]

        self.location_line.set_xdata(xs)
        self.location_line.set_ydata(ys)

        self.location_plt.relim()
        self.location_plt.autoscale_view()

        self.redraw_plots()

def _on_plot_closed(event):
    print("Closed the plot")
    sys.exit(0)
