#!/usr/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt
import pylab

def frange(x, y, jump):
  while x < y:
    yield x
    x += jump

def plot_hist(fname):
  data = np.genfromtxt(fname)
  lst = []
  for row in data:
    lst.extend(row)
  lst = filter(lambda x: x > 0, lst)
  hist, bins = np.histogram(lst, bins=100)
  width = 0.7*(bins[1]-bins[0])
  center = (bins[:-1]+bins[1:])/2
  plt.bar(center, hist, align = 'center', width = width)
  
  title = fname.split('/')[-1]
  plt.title(title)
  plt.xlabel('Jaccard Index')
  plt.ylabel('Histogram Count')
  loc = np.array([float("{:.2f}".format(i+0.01)) for i in frange(0.0, 1, 0.01)])
  labels = ["{:.2f}".format(i+0.01) for i in frange(0.0, 1, 0.01)]
  
  plt.xticks(loc, labels)
  
#   loc, labels = 
#   for l in labels:
#       print l
  fig = pylab.gcf()
  fig.canvas.set_window_title(title)
  plt.savefig(title+'.png')
  plt.show()
  plt.clf()
  

# def main():
#   if len(sys.argv) < 2:
#     print 'Usage: python progname filename'
#     return
#   fname = sys.argv[1]
#   plot_hist(fname)


if __name__ == '__main__':
  files = [
#         "/Users/shauvik/S/Dropbox/Research/D2M/SubjectTraces/twitter/twitter.csv",
#         "/Users/shauvik/S/Dropbox/Research/D2M/SubjectTraces/twitter_mobile/twitter_mobile.csv",
#         "/Users/shauvik/S/Dropbox/Research/D2M/SubjectTraces/wikipedia/wikipedia.csv",
#         "/Users/shauvik/S/Dropbox/Research/D2M/SubjectTraces/wikipedia_mobile/wikipedia_mobile.csv",
#         "/Users/shauvik/S/Dropbox/Research/D2M/SubjectTraces/wordpress/wordpress.csv",
        "/Users/shauvik/S/Dropbox/Research/D2M/SubjectTraces/wordpress_mobile/wordpress_mobile.csv"
        ]
    
  for f in files:
      print f
      plot_hist(f)
      #exit()