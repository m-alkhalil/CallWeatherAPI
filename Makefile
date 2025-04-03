VENV_DIR=.wenv
PYTHON = $(VENV_DIR)/bin/python 
PIP = $(VENV_DIR)/bin/pip
TESTS = test
PYTEST = $(VENV_DIR)/bin/pytest
APP = src/main.py

#Default target when running make without arguments
.PHONY: help
help:
	@echo "********** Makefile commands: **********"
	@echo " - make install		 install dependencies"
	@echo " - make lint 		 Run py linter"
	@echo " - make run 		 Run the app"
	@echo " - make test 		 Run py tests"
	@echo " - make clean 		 Clean up the environment created "
	@echo " - dockerImg		 build the docker image"

#Install dependencies and create virtual environment if not created 
.PHONY: install
install:
	@python3 -m venv $(VENV_DIR)
	@$(PIP) install requiremnts.txt

.PHONY: lint	
lint:
	@pylint $(APP) 

.PHONY: run
run:
	@$(PYTHON) $(APP)

#clean the virtual env.
.PHONY: clean
clean:
	@rm -rf $(VENV_DIR)

.PHONY: dockerImg
dockerImg:
	@docker build -t callWeather .
