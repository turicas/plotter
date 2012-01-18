#!/usr/bin/env python
# coding: utf-8

from plotter import Plotter


my_plot = Plotter('processes.csv')
my_plot.radar(axis_labels='state', values='processes', legends='year',
              title="Processes on Brazil's Supreme Court")
my_plot.save('processes.png')

