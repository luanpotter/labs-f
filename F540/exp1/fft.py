import numpy as np
import matplotlib.pyplot as plt


def lines_to_matrix(file_name):
    with open(file_name) as f:
        lines = f.readlines()
        lines.pop(0)
        s = []
        for line in lines:
            r = []
            for value in line.split('\t'):
                r.append(float(value))
            r.pop(0)
            s.append(r)
        return [list(i) for i in zip(*s)]


def write(file, y, t):
    arq = open(file, 'w')
    arq.write('y \t time (s) \n')
    for i in range(len(y)):
        arq.write(str(t[i]) + '\t')
        arq.write(str(y[i]) + '\n')
    arq.close()


def plot_chart(time, y1, y2):
    fig, ax = plt.subplots(2, 1)
    ax[0].plot(time, y1)
    ax[0].set_xlabel('Time')
    ax[0].set_ylabel('Amplitude')
    ax[1].plot(time, y2)
    ax[1].set_xlabel('Freq (Hz)')
    ax[1].set_ylabel('|Y(freq)|')
    ax[1].set_xlim(xmin=1)
    # plt.show()
    plt.savefig('result.png')


def main():
    # freq = .1
    # time = np.arange(1, 100, .001)
    # voltage = [np.sin(2 * np.pi * freq * t) for t in time]
    time, _, voltage = lines_to_matrix('in.dat')

    fft = np.fft.fft(voltage) / len(time)
    fft_real = np.real(fft)

    plot_chart(time, voltage, fft_real)
    write('fft.dat', fft_real, time)


main()
