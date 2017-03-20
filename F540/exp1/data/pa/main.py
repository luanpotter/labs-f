#!/usr/bin/env python 

saveEach = False

import glob
import re

import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
plt.rcParams.update({'figure.max_open_warning': 0})

import numpy as np

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

def main():
  t = []
  for f in glob.glob("2017_03_15/*.dat"):
    groups = re.match('2017_03_15\/exp1_(\d*)_(\d*\.\d*)_curvas_.*\.dat', f)
    s = []
    s.append(int(groups.group(1)))
    s.append(float(groups.group(2)))
    s.append(f)
    t.append(s)
  return t

def doit():
  a = main()
  a.sort(key=lambda el: el[0])
  for s in a:
    r = process(s[2], s[0])
    diff = abs(r[0] - r[1])
    # s[2] = str(r[0]) + '|' + str(r[1])
    s[2] = diff
  return a


result = doit()
for el in result:
  print(el)

pdf = matplotlib.backends.backend_pdf.PdfPages('out/allcharts.pdf')
for fig in range(1, plt.figure().number): ## will open an empty extra figure :(
    pdf.savefig( fig )
pdf.close()
