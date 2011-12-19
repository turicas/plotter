#!/usr/bin/env python
# coding: utf-8

import datetime
from collections import Counter
from matplotlib.pyplot import figure
from outputty import Table


def linear(csv_filename, image_filename, title='', labels=True, grid=True,
           legends=True, style='o-', xlabel=None, ignore=None):
    data = Table(from_csv=csv_filename)
    columns = zip(*data.rows)
    if ignore is not None:
        filtered_columns = []
        for index, column in enumerate(columns):
            if data.headers[index] not in ignore:
                filtered_columns.append(column)
            else:
                filtered_columns.append(None)
    else:
        filtered_columns = columns
    fig = figure()
    ax = fig.add_subplot(111)
    ax.grid(grid)
    ax.set_title(title)
    if legends is True or not legends:
        legends = dict([(header, header) for header in data.headers])
    for index, column in enumerate(filtered_columns):
        header = data.headers[index]
        if xlabel is not None and header == xlabel or column is None:
            continue
        if data.types[header] in (int, float):
            ax.plot(column, style, label=legends[header])
    if legends:
        ax.legend()
    if xlabel is not None:
        x_column_label = columns[data.headers.index(xlabel)]
        ax.set_xticklabels(x_column_label)
    fig.savefig(image_filename, bbox_inches='tight', pad_inches=0.1)

def bar(csv_filename, image_filename, title='', labels=True, grid=True,
        width=0.8, start=0.5, increment=1, colors='bgrcmykw', aggregate=None,
        legends=None):
    data = Table(from_csv=csv_filename)
    columns = zip(*data.rows)
    offset = (increment - width) / 2.0
    fig = figure()
    ax = fig.add_subplot(111)
    ax.grid(grid)
    ax.set_title(title)
    if legends is True or not legends:
        legends = dict([(header, header) for header in data.headers])
    bars_titles = []
    if aggregate:
        counter = Counter(columns[data.headers.index(aggregate)])
        xticklabels = counter.keys()
        columns_to_plot = [[counter[k] for k in xticklabels]]
    else:
        columns_to_plot = []
        for index in range(len(columns)):
            if data.types[data.headers[index]] in (int, float):
                columns_to_plot.append(columns[index])
                bars_titles.append(data.headers[index])
    width /= float(len(columns_to_plot))
    colors = list(colors)
    colors.reverse()
    bars = []
    for index, column in enumerate(columns_to_plot):
        lefts = []
        left = start + index * width
        for i in range(len(column)):
            lefts.append(offset + left + i * increment)
        bars.append(ax.bar(lefts, column, width, color=colors.pop())[0])
    xticks = [start + increment * (i + 0.5) for i in range(len(lefts))]
    if legends:
        if not aggregate:
            if isinstance(legends, dict):
                bars_titles = [legends[header] for header in data.headers]
            ax.legend(bars, bars_titles)
            xticklabels = ['' for t in range(len(xticks))]
        else:
            ax.legend(bars, [legends[aggregate]])
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels)
    fig.savefig(image_filename, bbox_inches='tight', pad_inches=0.1)

def scatter(csv_filename, image_filename, title='', labels=True, grid=True,
            legends=True, x_column=None, style='o-'):
    data = Table(from_csv=csv_filename)
    columns = zip(*data.rows)
    data_types = data.types.values()
    fig = figure()
    ax = fig.add_subplot(111)
    ax.grid(grid)
    ax.set_title(title)
    x_column_name = x_column
    if legends is True or not legends:
        legends = dict([(header, header) for header in data.headers])
    if not x_column_name:
        for name, type_ in data.types.iteritems():
            if type_ in (datetime.date, datetime.datetime):
                x_column_name = name
                break
    if x_column_name is None:
        x_column_name = data.headers[0]
    if labels:
        ax.set_xlabel(x_column_name)
    x_column_index = data.headers.index(x_column_name)
    x_column = columns[x_column_index]
    for index, column in enumerate(columns):
        header = data.headers[index]
        if index == x_column_index or data.types[header] not in (int, float):
            continue
        ax.plot(x_column, column, style, label=legends[header])
    if data.types[x_column_name] in (datetime.date, datetime.datetime):
        fig.autofmt_xdate()
    if legends:
        ax.legend()
    fig.savefig(image_filename, bbox_inches='tight', pad_inches=0.1)
