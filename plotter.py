#!/usr/bin/env python
# coding: utf-8

import datetime
from collections import Counter
from numpy import linspace, array, zeros, pi, concatenate
from matplotlib.pyplot import figure
import matplotlib.cm
from outputty import Table


class Plotter(object):
    'Stores information about a plot and plot it'

    def __init__(self, data=None, rows=1, cols=1, width=1024, height=768):
        self.rows = rows
        self.cols = cols
        self._subplot_number = 0
        self.fig = figure(figsize=(width / 80, height / 80), dpi=80)
        self._load_data(data)

    def _load_data(self, data):
        self.data = Table()
        self.data.read('csv', data)

    def _get_new_subplot(self, projection=None):
        self._subplot_number += 1
        if self._subplot_number > self.rows * self.cols:
            raise OverflowError('This figure can handle only %d subplots' % \
                                self.rows * self.cols)
        if projection is not None:
            return self.fig.add_subplot(self.rows, self.cols,
                                        self._subplot_number,
                                        projection=projection)
        else:
            return self.fig.add_subplot(self.rows, self.cols,
                                        self._subplot_number)

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
            color_range = linspace(0, 0.9, len(columns_to_plot))
            colors = [colormap(i) for i in color_range]
        for header in columns_to_plot:
                subplot.plot(self.data[header], style, label=legends[header],
                             color=colors.pop(0))
        if x_labels is not None:
            subplot.set_xticklabels(self.data[x_labels])
        subplot.legend()

    def scatter(self, x_column, title='', grid=True, labels=True, legends=True,
                style='o-', ignore='', colors=None,
                colormap=matplotlib.cm.PRGn, order_by=None, ordering='asc',
                x_label=None, y_lim=None, legend_location='upper center',
                legend_box=(0.5, 2.2)):
        subplot = self._get_new_subplot()
        subplot.set_title(title)
        subplot.grid(grid)
        if order_by is None:
            order_by = x_column
        self.data.order_by(order_by, ordering)
        if legends is True:
            legends = {header: header for header in self.data.headers}
        if self.data.types[x_column] in (datetime.date, datetime.datetime):
            self.fig.autofmt_xdate()
        if labels:
            if x_label is None:
                x_label = x_column
            subplot.set_xlabel(x_label)
        x_values = range(len(self.data[x_column]))
        columns_to_plot = []
        for header in set(self.data.headers) - set(ignore):
            if header != x_column and self.data.types[header] in (int, float):
                columns_to_plot.append(header)
        if colors is None:
            color_range = linspace(0, 0.9, len(columns_to_plot))
            colors = [colormap(i) for i in color_range]
        for header in columns_to_plot:
            if legends is None:
                subplot.plot(x_values, self.data[header], style,
                             color=colors.pop(0))
            else:
                subplot.plot(x_values, self.data[header], style,
                             label=legends[header], color=colors.pop(0))
        subplot.set_xticks(x_values)
        subplot.set_xticklabels(self.data[x_column])
        if y_lim is not None:
            subplot.set_ylim(y_lim)
        if legends is not None:
            subplot.legend(loc=legend_location, bbox_to_anchor=legend_box)
            self.fig.subplots_adjust(top=0.5, right=0.9)

    def bar(self, title='', grid=True, count=None, bar_width=0.8, x_column='',
            bar_start=0.5, bar_increment=1.0, legends=True,
            x_rotation=0, colors=None, colormap=matplotlib.cm.PRGn,
            y_label=None, y_lim=None):
        if legends is True:
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
            for header in self.data.headers:
                if self.data.types[header] in (int, float):
                    columns_to_plot.append(self.data[header])
                    bars_titles.append(header)
        bar_width /= float(len(columns_to_plot))
        bars = []
        if colors is None:
            color_range = linspace(0, 0.9, len(columns_to_plot))
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
            if count is None:
                bars_titles = [legends[header] \
                               for header in self.data.headers]
                xticklabels = xticks
            else:
                bars_titles = [legends[count]]
            subplot.legend(bars, bars_titles)
        else:
            xticklabels = self.data[x_column]
        subplot.set_xticklabels(xticklabels, rotation=x_rotation)
        if y_label is not None:
            subplot.set_ylabel(y_label)
        if y_lim is not None:
            subplot.set_ylim(y_lim)

    def stacked_bar(self, x_column, y_column, y_labels=None, title='',
                    grid=True, bar_width=0.5, x_rotation=0, legends=True,
                    legend_location='upper left', legend_box=(-0.4, 1),
                    colors=None, colormap=matplotlib.cm.gist_heat):
        subplot = self._get_new_subplot()
        subplot.set_title(title)
        subplot.grid(grid)
        x_offset = (1.0 - bar_width) / 2
        x_values_unique = list(set(self.data[x_column]))
        x_values = array(range(len(set(self.data[x_column]))))
        subplot.set_xticks(x_values + x_offset)
        subplot.set_xticklabels(x_values_unique, rotation=x_rotation)
        y_labels_values = list(set(self.data[y_labels]))
        y_labels_values.sort()
        data = {y: Counter() for y in y_labels_values}
        if colors is None:
            color_range = linspace(0, 0.9, len(data.keys()))
            colors = [colormap(i) for i in color_range]
        for row in self.data.to_list_of_dicts(encoding=None):
            data[row[y_labels]][row[x_column]] += row[y_column]
        bottom = zeros(len(x_values))
        for y in y_labels_values:
            values = [data[y][x] for x in x_values_unique]
            subplot.bar(x_values, values, width=bar_width, label=unicode(y),
                        color=colors.pop(0), bottom=bottom)
            bottom = [bottom[index] + value \
                      for index, value in enumerate(values)]
        if legends:
            subplot.legend(loc=legend_location, bbox_to_anchor=legend_box)
        self.fig.subplots_adjust(bottom=0.1, left=0.25)

    def radar(self, axis_labels, values, legends, title='', grid=True,
              fill_alpha=0.25, colors=None, colormap=matplotlib.cm.gist_heat):
        subplot = self._get_new_subplot(projection='polar')
        subplot.set_title(title)
        subplot.grid(grid)
        axis_labels_values = list(set(self.data[axis_labels]))
        axis_labels_values.sort()
        number_of_axis = len(axis_labels_values)
        axis_angles = 2 * pi * linspace(0, 1 - 1.0 / number_of_axis,
                                        number_of_axis)
        subplot.set_thetagrids(axis_angles * 180 / pi, axis_labels_values)
        legends_values = list(set(self.data[legends]))
        legends_values.sort()
        if colors is None:
            len_legends = len(legends_values)
            color_range = linspace(0, 1 - 1.0 / len_legends, len_legends)
            colors = [colormap(i) for i in color_range]
        curves = {x: Counter() for x in legends_values}
        self.data.order_by(axis_labels)
        for row in self.data.to_list_of_dicts(encoding=None):
            curves[row[legends]][row[axis_labels]] += row[values]
        for key in legends_values:
            values = [curves[key][x] for x in axis_labels_values]
            color = colors.pop(0)
            lines = subplot.plot(axis_angles, values, color=color)
            subplot.fill(axis_angles, values, facecolor=color,
                         alpha=fill_alpha)
            x, y = lines[0].get_data()
            new_x = concatenate((x, [x[0]]))
            new_y = concatenate((y, [y[0]]))
            lines[0].set_data(new_x, new_y)
        subplot.legend(legends_values)
