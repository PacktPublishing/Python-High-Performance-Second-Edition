from rx import Observable
import psutil
import numpy as np
import pylab as plt

cpu_data = (Observable
            .interval(100) # Each 100 milliseconds
            .map(lambda x: psutil.cpu_percent())
            .publish())
cpu_data.connect()


def monitor_cpu(npoints):
    lines, = plt.plot([], [])
    plt.xlim(0, npoints)
    plt.ylim(0, 100)

    cpu_data_window = cpu_data.buffer_with_count(npoints, 1)

    def update_plot(cpu_readings):
        lines.set_xdata(np.arange(len(cpu_readings)))
        lines.set_ydata(np.array(cpu_readings))
        plt.draw()

    alertpoints = 4
    high_cpu = (cpu_data
                .buffer_with_count(alertpoints, 1)
                .map(lambda readings: all(r > 20 for r in readings)))

    label = plt.text(1, 1, "normal")

    def update_warning(is_high):
        if is_high:
            label.set_text("high")
        else:
            label.set_text("normal")

    high_cpu.subscribe(update_warning)
    cpu_data_window.subscribe(update_plot)

    plt.show()

if __name__ == '__main__':
    monitor_cpu(10)
