#!/bin/bash

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
lr supported-triggers
lr supported-licenses
lr verify -il MIT -ol BSD-3-Clause
