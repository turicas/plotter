#!/usr/bin/env python
# coding: utf-8

import datetime
from collections import Counter
from matplotlib.pyplot import figure
from outputty import Table


class Plotter(object):
    'Stores information about a plot and plot it'

    def __init__(self, data='', legends=None):
        self.load_data(data)
        self.PLOT = {'linear': self._plot_linear,
                     'scatter': self._plot_scatter,
                     'bar': self._plot_bar}

    def load_data(self, data):
        info = data.split(':')
        if len(info) and info[0] == 'csv':
            self.data = Table(from_csv=':'.join(info[1:]))
            self.columns = zip(*self.data.rows)

    def plot(self, kind='linear', to='', title='', labels=True, grid=True,
             legends=True, style='o-', ignore=None, xlabels=None,
             x_column=None, aggregate=None):
        '''Does the plot with passed configurations and save the result in a
        file.

        Keyword arguments:
        kind -- linear|scatter|bar
        to -- filename to save the plot file
        title -- the title of the graph
        labels -- should put x and y labels? Default: True
        xlabels -- header name of the column to put values in x axe
        grid -- should put a grid in the graph? Default: True)
        legends -- should use legends in the curves? Default: True
        style -- the style used for the curve (see matplotlib). Default: 'o-'

        `legends` can be a dictionary with each key being the column header
        name and value what will be showed in the legend for this header.
        '''
        self.kind = kind
        self.title = title
        self.grid = grid
        self.labels = labels
        self.xlabels = xlabels
        self.x_column = x_column
        self.legends = legends
        self.style = style
        self.ignore = ignore
        self.aggregate = aggregate
        if ignore is not None:
            self.filtered_columns = []
            for index, column in enumerate(self.columns):
                if self.data.headers[index] not in ignore:
                    self.filtered_columns.append(column)
                else:
                    self.filtered_columns.append(None)
        else:
            self.filtered_columns = self.columns
        if not self.legends or self.legends is True:
            self.legends = dict([(header, header) \
                                 for header in self.data.headers])

        self.fig = figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title(title)
        self.ax.grid(grid)
        self.PLOT[kind]()
        if self.legends and kind != 'bar':
            self.ax.legend()
        self.fig.savefig(to, bbox_inches='tight', pad_inches=0.1)

    def _plot_linear(self):
        for index, column in enumerate(self.filtered_columns):
            header = self.data.headers[index]
            if self.xlabels is not None and header == self.xlabels or \
               column is None:
                continue
            if self.data.types[header] in (int, float):
                self.ax.plot(column, self.style, label=self.legends[header])
        if self.xlabels is not None:
            x_labels = self.columns[self.data.headers.index(self.xlabels)]
            self.ax.set_xticklabels(x_labels)

    def _plot_scatter(self):
        x_column_name = self.x_column
        if not x_column_name:
            for name, type_ in self.data.types.iteritems():
                if type_ in (datetime.date, datetime.datetime):
                    x_column_name = name
                    break
        if x_column_name is None:
            x_column_name = self.data.headers[0]
        if self.labels:
            self.ax.set_xlabel(x_column_name)
        x_column_index = self.data.headers.index(x_column_name)
        x_column = self.columns[x_column_index]
        for index, column in enumerate(self.columns):
            header = self.data.headers[index]
            if index == x_column_index or \
               self.data.types[header] not in (int, float):
                continue
            self.ax.plot(x_column, column, self.style,
                         label=self.legends[header])
        if self.data.types[x_column_name] in (datetime.date, datetime.datetime):
            self.fig.autofmt_xdate()

    def _plot_bar(self):
        colors = list('wkymcrgb')
        bar_width = 0.8
        bar_start = 0.5
        bar_increment = 1.0
        bar_offset = (bar_increment - bar_width) / 2.0
        bars_titles = []
        if self.aggregate:
            aggregate_index = self.data.headers.index(self.aggregate)
            counter = Counter(self.columns[aggregate_index])
            xticklabels = counter.keys()
            columns_to_plot = [[counter[k] for k in xticklabels]]
        else:
            columns_to_plot = []
            for index in range(len(self.columns)):
                if self.data.types[self.data.headers[index]] in (int, float):
                    columns_to_plot.append(self.columns[index])
                    bars_titles.append(self.data.headers[index])
        bar_width /= float(len(columns_to_plot))
        bars = []
        for index, column in enumerate(columns_to_plot):
            left = bar_start + index * bar_width
            lefts = [bar_offset + left + i * bar_increment \
                     for i in range(len(column))]
            bars.append(self.ax.bar(lefts, column, bar_width,
                                    color=colors.pop())[0])
        xticks = [bar_start + bar_increment * (i + 0.5) \
                  for i in range(len(lefts))]
        self.ax.set_xticks(xticks)
        if self.legends:
            if not self.aggregate:
                bars_titles = [self.legends[header] \
                               for header in self.data.headers]
                xticklabels = ['' for t in range(len(xticks))]
            else:
                bars_titles = [self.legends[self.aggregate]]
            self.ax.legend(bars, bars_titles)
        self.ax.set_xticklabels(xticklabels)
