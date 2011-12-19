test:	clean clear_screen
	nosetests --with-coverage --cover-package csv_plotter -s

clean:
	@rm -rf *.pyc *.png

clear_screen:
	clear

.PHONY:	test clean clear_screen
