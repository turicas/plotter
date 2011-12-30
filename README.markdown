plotter
=======

This is a little project on top of
[outputty](https://github.com/turicas/outputty) and
[matplotlib](http://matplotlib.sourceforge.net/) that aims in easily create
plots (without all pain of using matplotlib). By now you can do linear, scatter
and bar plots with data from CSV files.


Requirements/Installation
-------------------------

- Execute `pip install numpy matplotlib`
- [Download outputty](https://github.com/turicas/outputty/tarball/master)
- [Download plotter](https://github.com/turicas/plotter/tarball/master)
- Unpack `outputty` and `plotter` in the same directory (sorry for that - it'll
  be available on PyPI soon)


Examples
--------

If you have a CSV file called `data.csv` with this content:

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

and execute this little piece of code:

    from plotter import Plotter
    my_plot = Plotter('data.csv')
    my_plot.scatter(x_column='Z Values', title='Hello, plotter!',
                    colors=['blue', 'red'])
    my_plot.save('data.png')

then `data.png` will be created:

<img src="http://www.justen.eng.br/projects/plotter/img/data.png">

> For more example please see file `test_plotter.py`. If you run it, a
> directory called `test_results` will be created with the plots.


License
-------

This software is licensed under
[GPL 2](http://www.gnu.org/licenses/gpl-2.0.html).


Copyright
---------

Copyright Álvaro Justen 2011
