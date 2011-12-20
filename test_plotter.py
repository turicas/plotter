#!/usr/bin/env python
# coding: utf-8

import unittest
import os
import shutil
import tempfile
import inspect
from textwrap import dedent
from plotter import Plotter


TEST_RESULTS_PATH = 'test_results'
try:
    shutil.rmtree(TEST_RESULTS_PATH)
except OSError:
    pass
os.mkdir(TEST_RESULTS_PATH)

def create_temp_csv(contents):
    temp_fp = tempfile.NamedTemporaryFile(delete=False)
    temp_fp.write(contents)
    temp_fp.close()
    return temp_fp.name

def get_filename_from_frame(frame):
    test_name = frame.f_code.co_name
    return os.path.join(TEST_RESULTS_PATH, test_name + '.png')

class TestCsvPlot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = {}
        file_contents = dedent('''
        "X Values"
        1
        2
        3
        4
        5
        6
        7
        8
        9
        ''')
        cls.data['int'] = create_temp_csv(file_contents)
        file_contents = dedent('''
        "X Values","Y Values"
        1,1
        2,4
        3,9
        4,16
        5,25
        6,36
        7,49
        8,64
        9,81
        ''')
        cls.data['int-int'] = create_temp_csv(file_contents)
        file_contents = dedent('''
        "X Values","Y Values"
        2011-01-01,1
        2011-01-02,4
        2011-01-03,9
        2011-01-04,16
        2011-01-05,25
        2011-01-06,36
        2011-01-07,49
        2011-01-08,64
        2011-01-09,81
        ''')
        cls.data['date-int'] = create_temp_csv(file_contents)
        file_contents = dedent('''
        "X Values","Y Values","Z Values"
        1,1,2011-01-01
        4,8,2011-01-02
        9,27,2011-01-03
        16,64,2011-01-04
        25,125,2011-01-05
        36,216,2011-01-06
        49,343,2011-01-07
        64,512,2011-01-08
        81,729,2011-01-09
        ''')
        cls.data['int-int-date'] = create_temp_csv(file_contents)
        file_contents = dedent('''
        "X Values","Y Values","Z Values"
        1,1,1
        4,8,12
        9,27,36
        16,64,80
        25,125,150
        36,216,252
        49,343,392
        64,512,576
        81,729,810
        ''')
        cls.data['int-int-int'] = create_temp_csv(file_contents)
        file_contents = dedent('''
        animal
        dog
        cat
        dog
        dog
        dog
        cat
        cat
        human
        dog
        tiger
        tiger
        coati
        ''')
        cls.data['animals'] = create_temp_csv(file_contents)

    @classmethod
    def tearDownClass(cls):
        for filename in cls.data.values():
            os.remove(filename)

    def test_01_2_columns_with_only_data_no_scatter(self):
        image_filename = get_filename_from_frame(inspect.currentframe())
        my_plot = Plotter(self.data['int-int'])
        my_plot.plot('linear', image_filename, title='Hello, world')

    def test_02_2_columns_with_only_data_scatter(self):
        image_filename = get_filename_from_frame(inspect.currentframe())
        my_plot = Plotter(self.data['int-int'])
        my_plot.plot('scatter', image_filename)

    def test_03_2_columns_with_one_as_date_no_scatter(self):
        image_filename = get_filename_from_frame(inspect.currentframe())
        my_plot = Plotter(self.data['date-int'])
        my_plot.plot('linear', image_filename)

    def test_04_2_columns_with_one_as_date_scatter(self):
        image_filename = get_filename_from_frame(inspect.currentframe())
        my_plot = Plotter(self.data['date-int'])
        my_plot.plot('scatter', image_filename)

    def test_05_3_columns_with_one_as_date_scatter_no_labels(self):
        image_filename = get_filename_from_frame(inspect.currentframe())
        my_plot = Plotter(self.data['date-int'])
        my_plot.plot('scatter', image_filename, labels=False)

    def test_06_3_columns_with_one_as_date_and_x_as_int_scatter(self):
        image_filename = get_filename_from_frame(inspect.currentframe())
        my_plot = Plotter(self.data['int-int-date'])
        my_plot.plot('scatter', image_filename, x_column='Y Values')

    def test_07_1_column_barplot(self):
        image_filename = get_filename_from_frame(inspect.currentframe())
        my_plot = Plotter(self.data['int'])
        my_plot.plot('bar', image_filename)

    def test_08_2_columns_barplot(self):
        image_filename = get_filename_from_frame(inspect.currentframe())
        my_plot = Plotter(self.data['int-int'])
        my_plot.plot('bar', image_filename)

    def test_09_1_column_with_aggregate(self):
        image_filename = get_filename_from_frame(inspect.currentframe())
        my_plot = Plotter(self.data['animals'])
        my_plot.plot('bar', image_filename, aggregate='animal',
                legends={'animal': 'Animals'})

    def test_10_2_columns_plot_with_one_as_label(self):
        image_filename = get_filename_from_frame(inspect.currentframe())
        my_plot = Plotter(self.data['int-int'])
        my_plot.plot('linear', image_filename, x_labels='Y Values')

    def test_11_ignore_columns(self):
        image_filename = get_filename_from_frame(inspect.currentframe())
        my_plot = Plotter(self.data['int-int-int'])
        my_plot.plot('linear', image_filename, x_labels='Y Values',
                     ignore=['X Values', 'Y Values'])
