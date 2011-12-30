#!/usr/bin/env python
# coding: utf-8

import datetime
from collections import Counter
import numpy
from matplotlib.pyplot import figure
import matplotlib.cm
from outputty import Table


class Plotter(object):
    'Stores information about a plot and plot it'

    def __init__(self, data=None, legends=None):
        self.fig = figure()
        self._load_data(data)

    def _load_data(self, data):
        self.data = Table()
        self.data.read('csv', data)
        self.columns = zip(*self.data.rows)

    def _get_new_subplot(self):
        return self.fig.add_subplot(111)

    def save(self, filename):
        #self.fig.savefig(filename, bbox_inches='tight', pad_inches=0.1)
        self.fig.savefig(filename)

    def linear(self, title='', grid=True, style='o-', x_labels=None,
               legends=True, ignore='', colors=None,
               colormap=matplotlib.cm.PRGn):
        if legends is None or legends is True:
            legends = {header: header for header in self.data.headers}
        subplot = self._get_new_subplot()
        subplot.set_title(title)
        subplot.grid(grid)
        columns_to_plot = []
        for header in set(self.data.headers) - set(ignore):
            if header != x_labels and self.data.types[header] in (int, float):
                columns_to_plot.append(header)
        if colors is None:
            color_range = numpy.linspace(0, 0.9, len(columns_to_plot))
            colors = [colormap(i) for i in color_range]
        for header in columns_to_plot:
                subplot.plot(self.data[header], style, label=legends[header],
                             color=colors.pop(0))
        if x_labels is not None:
            subplot.set_xticklabels(self.data[x_labels])
        subplot.legend()

    def scatter(self, x_column, title='', grid=True, labels=True, legends=True,
                style='o-', ignore='', colors=None,
                colormap=matplotlib.cm.PRGn):
        subplot = self._get_new_subplot()
        subplot.set_title(title)
        subplot.grid(grid)
        if legends is None or legends is True:
            legends = {header: header for header in self.data.headers}
        if self.data.types[x_column] in (datetime.date, datetime.datetime):
            self.fig.autofmt_xdate()
        if labels:
            subplot.set_xlabel(x_column)
        x_values = self.data[x_column]
        columns_to_plot = []
        for header in set(self.data.headers) - set(ignore):
            if header != x_column and self.data.types[header] in (int, float):
                columns_to_plot.append(header)
        if colors is None:
            color_range = numpy.linspace(0, 0.9, len(columns_to_plot))
            colors = [colormap(i) for i in color_range]
        for header in columns_to_plot:
            subplot.plot(x_values, self.data[header], style,
                         label=legends[header], color=colors.pop(0))
        subplot.legend()

    def bar(self, title='', grid=True, count=None, bar_width=0.8,
            bar_start=0.5, bar_increment=1.0, legends=True,
            x_rotation=0, colors=None, colormap=matplotlib.cm.PRGn):
        if legends is None or legends is True:
            legends = {header: header for header in self.data.headers}
        subplot = self._get_new_subplot()
        subplot.set_title(title)
        subplot.grid(grid)
        bar_offset = (bar_increment - bar_width) / 2.0
        bars_titles = []
        if count is not None:
            counter = Counter(self.data[count])
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
        if colors is None:
            color_range = numpy.linspace(0, 0.9, len(columns_to_plot))
            colors = [colormap(i) for i in color_range]
        for index, column in enumerate(columns_to_plot):
            left = bar_start + index * bar_width
            lefts = [bar_offset + left + i * bar_increment \
                     for i in range(len(column))]
            bars.append(subplot.bar(lefts, column, bar_width,
                                    color=colors.pop(0))[0])
        xticks = [bar_start + bar_increment * (i + 0.5) \
                  for i in range(len(lefts))]
        subplot.set_xticks(xticks)
        if legends:
            if not count:
                bars_titles = [legends[header] \
                               for header in self.data.headers]
                xticklabels = ['' for t in range(len(xticks))]
            else:
                bars_titles = [legends[count]]
            subplot.legend(bars, bars_titles)
        subplot.set_xticklabels(xticklabels, rotation=x_rotation)

    def stacked_bar(self, x_column, y_column, y_labels=None, title='',
                    grid=True, bar_width=0.5, x_rotation=0, legends=True,
                    legend_location='upper left', legend_box=(-0.4, 1),
                    colors=None, colormap=matplotlib.cm.gist_heat):
        subplot = self._get_new_subplot()
        subplot.set_title(title)
        subplot.grid(grid)
        if y_labels is None:
            y_labels = y_column
        x_offset = (1.0 - bar_width) / 2
        x_values = list(set(self.data[x_column]))
        x_values.sort()
        x_values = numpy.array(x_values)
        subplot.set_xticks(x_values + x_offset)
        subplot.set_xticklabels(x_values, rotation=x_rotation)
        y_labels_values = list(set(self.data[y_labels]))
        y_labels_values.sort()
        data = {y: Counter() for y in y_labels_values}
        if colors is None:
            color_range = numpy.linspace(0, 0.9, len(data.keys()))
            colors = [colormap(i) for i in color_range]
        for row in self.data.to_list_of_dicts():
            data[row[y_labels]][row[x_column]] += row[y_column]
        bottom = numpy.zeros(len(x_values))
        for y in y_labels_values:
            values = [data[y][x] for x in x_values]
            subplot.bar(x_values, values, width=bar_width, label=y,
                        color=colors.pop(0), bottom=bottom)
            bottom = [bottom[index] + value \
                      for index, value in enumerate(values)]
        if legends:
            subplot.legend(loc=legend_location, bbox_to_anchor=legend_box)
        self.fig.subplots_adjust(bottom=0.1, left=0.25)
