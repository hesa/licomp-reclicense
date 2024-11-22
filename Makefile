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

check_version:
	@echo -n "Checking api versions: "
	@MY_VERSION=`grep api_version licomp_reclicense/config.py | cut -d = -f 2 | sed -e "s,[ ']*,,g"` ; LICOMP_VERSION=`grep licomp requirements.txt | cut -d = -f 3 | sed -e "s,[ ']*,,g" -e "s,[ ']*,,g" -e "s,\(^[0-9].[0-9]\)[\.0-9\*]*,\1,g"` ; if [ "$$MY_VERSION" != "$$LICOMP_VERSION" ] ; then echo "FAIL" ; echo "API versions differ \"$$MY_VERSION\" \"$$LICOMP_VERSION\"" ; exit 1 ; else echo OK ; fi

lint:
	PYTHONPATH=. flake8 licomp_reclicense

.PHONY: build
build:
	rm -fr build && python3 setup.py sdist

test:
	PYTHONPATH=. python3 -m pytest --log-cli-level=10 tests/

test-local:
	PYTHONPATH=.:../licomp python3 -m pytest --log-cli-level=10 tests/

install:
	pip install .

reuse:
	reuse lint

check: clean reuse lint test check_version build
	@echo
	@echo
	@echo "All tests passed :)"
	@echo
	@echo

