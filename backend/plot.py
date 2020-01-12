from matplotlib import pyplot as plt


class plotCPU:

    def __init__(self, cpu_data):
        self.cpu_data = cpu_data

    def plot_events_per_second(self):
        y_axis = self.cpu_data.get("CPU speed", {}).get("events per second")
        x_axis = range(1, len(y_axis) + 1)
        plt.figure("events_per_second")
        plt.xlabel("Test Number")
        plt.ylabel("Events Per Second")
        plt.title("Events Per Second")
        plt.plot(x_axis, y_axis)

    def total_time_and_events(self):
        total_events = self.cpu_data.get("General statistics", {}).get(
            "total number of events"
        )
        total_time = self.cpu_data.get("General statistics", {}).get(
            "total time"
        )
        total_time = [float(time.strip("s")) for time in total_time]
        x_axis = range(1, len(total_events) + 1)
        plt.figure("total_time_and_events")
        plt.xlabel("Test Number")
        plt.title("Total Number of Events vs Total Time")
        plt.plot(x_axis, total_time)
        plt.plot(x_axis, total_events)
        plt.legend(["time in sec", "total events"])

    def latency_in_ms(self):
        latency = self.cpu_data.get("Latency (ms)", {})
        min_lat = latency.get("min")
        max_lat = latency.get("max")
        avg_lat = latency.get("avg")
        per_95_lat = latency.get("95th percentile")
        x_axis = range(1, len(min_lat) + 1)
        plt.figure("latency_in_ms")
        plt.xlabel("Test Number")
        plt.title("Latency in milliseconds")
        plt.plot(x_axis, min_lat)
        plt.plot(x_axis, max_lat)
        plt.plot(x_axis, avg_lat)
        plt.plot(x_axis, per_95_lat)
        plt.legend(["min", "max", "avg", "95%le"])

    def plot_all(self):
        self.plot_events_per_second()
        self.total_time_and_events()
        self.latency_in_ms()
        plt.show()


