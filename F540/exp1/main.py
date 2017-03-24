#!/usr/bin/env python 

import os
import math
import glob
import re

import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf

saveEach = True


def main():
    c = 'pb'
    os.chdir('data/' + c)
    print('Running for ' + c)
    run(c)


def process(pdf, c, file):
    with open(file['file_name']) as f:
        matrix = lines_to_matrix(f)
        plot_chart(c, file, matrix, pdf)
        return extract_delta_ts(file, matrix)


def extract_delta_ts(file, matrix):
    result = []
    for k in range(1, 3):
        i = 0
        if file['idx'] == 10:
            i = 200
        while True:
            if matrix[i][k] > 0:
                break
            else:
                i += 1

        while matrix[i][k] > -0.01:
            i += 1
        result.append(matrix[i - 1][0])
    return result


def plot_chart(c, file, matrix, pdf):
    c_name = 'c_' + c + '_' + str(file['idx'])
    fig = plt.figure(c_name)
    transposed = transpose(matrix)
    times = transposed[0]
    for k in range(1, 3):
        voltages = transposed[k]
        plt.plot(times, voltages, label='V' + str(k))
    plt.xlabel('time (s)')
    plt.ylabel('voltage (V)')
    plt.legend(loc='upper center', shadow=True)
    plt.title(c_name)
    plt.grid(True)
    if saveEach:
        plt.savefig('out/charts/' + c_name + '.png')
    pdf.savefig(fig)
    fig.clf()


def transpose(s):
    transposed = []
    for _ in s[0]:
        transposed.append([])
    for el in s:
        for i, v in enumerate(el):
            transposed[i].append(v)
    return transposed


def lines_to_matrix(f):
    lines = f.readlines()
    lines.pop(0)
    s = []
    for line in lines:
        r = []
        for value in line.split('\t'):
            r.append(float(value))
        r.pop(0)
        s.append(r)
    return s


def filter_files():
    files = []
    for file in glob.glob("2017_03_15/*.dat"):
        groups = re.match('2017_03_15/exp1_(\d*)_(\d*\.\d*)_curvas_.*\.dat', file)
        files.append({
            'file_name': file,
            'idx': int(groups.group(1)),
            'freq': float(groups.group(2))
        })
    files.sort(key=lambda el: el['idx'])
    files.pop(19)  # this is not good
    return files


def extract_data(pdf, c):
    files = filter_files()
    results = []
    for file in files:
        t1, t2 = process(pdf, c, file)
        diff = abs(t1 - t2)
        error_t = lambda t: .01 / 100 * t + .4 / 100 * 100 / (10 ** 6) + .4 / (10 ** 6)
        error_diff = math.sqrt(error_t(t1) ** 2 + error_t(t2) ** 2)
        phi = 2 * math.pi * file['freq'] * diff
        error_phi = 2 * math.pi * file['freq'] * error_diff
        results.append([file['idx'], file['freq'], phi, error_phi])
    return results


def plot_mary(l, result):
    phi = []
    freq = []
    for r in result:
        phi.append(math.degrees(r[2]))
        freq.append(math.log10(r[1]))

    fig = plt.figure('p' + l + '_mary')
    plt.plot(freq, phi, label='Phi')
    plt.xlabel('freq (Hz)')
    plt.ylabel('Phi (dg)')
    plt.legend(loc='upper center', shadow=True)
    plt.title('Phi por freq')
    plt.grid(True)
    plt.savefig('out/mary.png')
    fig.clf()


def run(c):
    pdf = matplotlib.backends.backend_pdf.PdfPages('out/all-charts.pdf')
    result = extract_data(pdf, c)
    pdf.close()
    plt.close('all')
    for el in result:
        print(el)
    plot_mary(c, result)


main()
