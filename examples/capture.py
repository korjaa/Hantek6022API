import matplotlib.pyplot as plt

from Hantek6022B import Hantek6022B


def main():
    scope = Hantek6022B()
    scope.setup()
    scope.open_handle()

    vrange = 10
    scope.set_voltage_range(ch=0, range_index=vrange)
    scope.set_voltage_range(ch=1, range_index=vrange)
    scope.set_num_channels(2)
    scope.set_sample_rate(110)  # 20 kS/s

    scope.read(100)
    ch1, ch2 = scope.read(1000)

    plt.plot(ch1, label="ch1")
    plt.plot(ch2, label="ch2")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
