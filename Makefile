# Variables
PYTHON = python3
PIP = pip3
MAIN_FILE = src/main.py
CONFIG_FILE = src/config/config.ini

# Targets
.PHONY: install run clean

install:
	@echo "Installing requirements..."
	$(PIP) install -r requirements.txt
	@echo "Installing Graphviz..."
	bash install_graphviz.sh

run: $(MAIN_FILE) $(CONFIG_FILE)
	@echo "Starting application..."
	$(PYTHON) $(MAIN_FILE)

clean:
	@echo "Cleaning up..."
	rm -rf __pycache__ *.pyc
