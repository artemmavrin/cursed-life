PYTHON := python3
SETUP := setup.py
SETUPOPTS := -q
RM := rm -rf

.PHONY: help install clean

help:
	@ echo "Usage:"
	@ echo "\tmake clean     \t remove auxiliary files."
	@ echo "\tmake help      \t view this help message."
	@ echo "\tmake install   \t install the package using setuptools."

install: clean
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) $(SETUP) $(SETUPOPTS) install

clean:
	@ $(RM) build dist *.egg-info .eggs .pytest_cache .coverage
	@ find . -name "__pycache__" -type d | xargs rm -rf
	@ find . -name ".ipynb_checkpoints" -type d | xargs rm -rf
	@ find . -name "*.pyc" -type f | xargs rm -f
	@ find . -name ".DS_Store" -type f | xargs rm -f
	@ find . -type d -empty -delete
