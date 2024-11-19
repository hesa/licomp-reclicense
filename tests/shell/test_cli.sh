#!/bin/bash

# SPDX-FileCopyrightText: 2024 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

lr()
{
    PYTHONPATH=. ./licomp_reclicense/__main__.py $*
    if [ $? -ne 0 ]
    then
        echo "failed: $*"
        exit 1
    fi
}

lr --help
lr --name
lr --version
lr supported-provisionings
lr supported-usecases
lr supported-licenses
lr verify -il MIT -ol BSD-3-Clause
