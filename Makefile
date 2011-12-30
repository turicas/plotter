test:	clean clear_screen
	nosetests --with-coverage --cover-package plotter -s

clean:
	@rm -rf *.pyc *.png reg_settings.py

clear_screen:
	clear

.PHONY:	test clean clear_screen
