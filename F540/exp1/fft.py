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


def plot_chart(name, time, y1, y2):
    fig, ax = plt.subplots(2, 1)
    ax[0].plot(time, y1)
    ax[0].set_xlabel('Time')
    ax[0].set_ylabel('Amplitude')
    ax[1].plot(time, y2)
    ax[1].set_xlabel('Freq (Hz)')
    ax[1].set_ylabel('|Y(freq)|')
    plt.savefig(name + '.png')


def run(input_file, output_file):
    time, _, voltage = lines_to_matrix(input_file)

    fft = np.real(np.fft.fft(voltage) / len(time))

    plot_chart(output_file, time, voltage, fft)
    write(output_file + '.dat', fft, time)


def main():
    run('data/pb/2017_03_15/exp1_12_12770.7359302_curvas_20_39_05.dat', 'data/pb/out/c12')
    run('data/pb/2017_03_15/exp1_19_116109.994846_curvas_20_40_20.dat', 'data/pb/out/c19')


main()
