# SPDX-FileCopyrightText: 2024 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

RECLIC_CSV=compatibility_63.csv
RECLIC_MATRIX=licomp_reclicense/var/reclicense-matrix.json
SCRIPT_DIR=scripts

RAW_GITHUB=https://raw.githubusercontent.com
CSV_URL="$(RAW_GITHUB)/osslab-pku/RecLicense/refs/heads/master/knowledge_base/files%20for%20program%20input/compatibility_63.csv"

$(RECLIC_MATRIX): $(RECLIC_CSV)
	@echo Creating matrix 
	PYTHONPATH=. $(SCRIPT_DIR)/create_matrix.py

$(RECLIC_CSV):
	@echo Downloading CSV file
	curl -LJO "$(CSV_URL)"

matrix: $(RECLIC_MATRIX)

force-matrix:
	rm $(RECLIC_MATRIX)
	make $(RECLIC_MATRIX)

clean:
	find . -name "*~" | xargs rm -f
	rm -fr licomp_reclicense.egg-info
	rm -fr build
	rm -fr licomp_reclicense/__pycache__
	rm -fr tests/__pycache__
	rm -f *.csv
	rm -fr dist

lint:
	PYTHONPATH=. flake8 licomp_reclicense

.PHONY: build
build:
	rm -fr build && python3 setup.py sdist

test:
	PYTHONPATH=. python3 -m pytest --log-cli-level=10 tests/
	PYTHONPATH=. ./licomp_reclicense/__main__.py -h
	PYTHONPATH=. ./licomp_reclicense/__main__.py --name
	PYTHONPATH=. ./licomp_reclicense/__main__.py --version
	PYTHONPATH=. ./licomp_reclicense/__main__.py supported-triggers
	PYTHONPATH=. ./licomp_reclicense/__main__.py supported-licenses
	PYTHONPATH=. ./licomp_reclicense/__main__.py verify -il MIT -ol BSD-3-Clause

install:
	pip install .

reuse:
	reuse lint
