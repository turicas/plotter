#!/usr/bin/env python
# coding: utf-8

from plotter import Plotter
my_plot = Plotter('data.csv')
my_plot.scatter(x_column='Z Values', title='Hello, plotter!',
                colors=['blue', 'red'])
my_plot.save('data.png')
