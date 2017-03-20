#!/usr/bin/env python 

saveEach = False
import os

def main():
  main_l('b')
  main_l('a')

def main_l(l):
  os.chdir('data/p' + l)
  print('Running for p' + l)
  run()
  os.chdir('../..')

import math
import glob
import re
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
plt.rcParams.update({'figure.max_open_warning': 0})

def process(fname, aaa):
  with open(fname) as f:
    lines = f.readlines()
    lines.pop(0)
    s = []
    for line in lines:
      r = []
      for value in line.split('\t'):
        r.append(float(value))
      r.pop(0)
      s.append(r)

    result = [-1, -1]
    cname = "charts/c_" + str(aaa) + ".png"
    plt.figure(cname)
    for k in range(1, 3):

      transpor = [[], []]
      for el in s:
        transpor[0].append(el[0])
        transpor[1].append(el[k])
      plt.plot(transpor[0], transpor[1], label='V' + str(k))
      plt.xlabel('time (s)')
      plt.ylabel('voltage (V)')
      plt.legend(loc='upper center', shadow=True)
      plt.title(cname)
      plt.grid(True)

      i = 0
      if aaa == 10:
        i = 200
      while True:
        if s[i][k] > 0:
          break
        else:
          i += 1
  
      while s[i][k] > -0.01:
        i += 1
      result[k - 1] = s[i - 1][0]
    if saveEach:
      plt.savefig('out/' + cname)
    return result

def filter_files():
  t = []
  for f in glob.glob("2017_03_15/*.dat"):
    groups = re.match('2017_03_15\/exp1_(\d*)_(\d*\.\d*)_curvas_.*\.dat', f)
    s = []
    s.append(int(groups.group(1)))
    s.append(float(groups.group(2)))
    s.append(f)
    t.append(s)
  return t

def extract_data():
  a = filter_files()
  a.sort(key=lambda el: el[0])
  a.pop(19)
  for s in a:
    r = process(s[2], s[0])
    diff = abs(r[0] - r[1])
    # s[2] = str(r[0]) + '|' + str(r[1])
    s[2] = diff
    s.append(diff * 2 * math.pi * s[1])
  return a


def print_pdf():
  pdf = matplotlib.backends.backend_pdf.PdfPages('out/all-charts.pdf')
  for fig in range(1, plt.figure().number): ## will open an empty extra figure :(
    pdf.savefig( fig )
  pdf.close()

def plot_mary(result):
  phi = []
  freq = []
  for r in result:
    phi.append(math.degrees(r[3]))
    freq.append(math.log10(r[1]))
  
  
  plt.figure('mary')
  plt.plot(freq, phi, label='Phi')
  plt.xlabel('freq (Hz)')
  plt.ylabel('Phi (dg)')
  plt.legend(loc='upper center', shadow=True)
  plt.title('Phi por freq')
  plt.grid(True)
  plt.savefig('out/mary.png')

def run():
  result = extract_data()
  for el in result:
    print(el)
  print_pdf()
  plot_mary(result)

main()

