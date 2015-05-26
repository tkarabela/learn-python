PYTHON = python

UI_FILES = $(shell find -type f -name '*.ui')

run:
	$(PYTHON) snake.py

ui: $(UI_FILES)
	$(PYTHON) -c 'import PyQt4.uic; PyQt4.uic.compileUiDir(".", recurse=True)'
