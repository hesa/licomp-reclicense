#!/bin/env python3

# SPDX-FileCopyrightText: 2024 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

import csv
import datetime
import json
import os
import sys

from licomp_reclicense.config import version
from licomp_reclicense.config import module_name
from licomp_reclicense.config import repo
from licomp_reclicense.config import disclaimer


RECLICENSE_DATA_DIR = os.path.join('..','RecLicense/knowledge_base/files for program input')
RECLICENSE_LICENSES_CSV = os.path.join(RECLICENSE_DATA_DIR, 'compatibility_63.csv')

# the licenses in the CSV sometimes do not have SPDX identifiers. Here is a map to normzlize
license_map = {
    "LGPL-2.1+": "LGPL-2.1-or-later",
    "LGPL-2.1": "LGPL-2.1-only",
    "LGPL-3.0+": "LGPL-3.0-or-later",
    "LGPL-3.0": "LGPL-3.0-only",
    "GPL-2.0+": "GPL-2.0-or-later",
    "GPL-2.0": "GPL-2.0-only",
    "GPL-3.0+": "GPL-3.0-or-later",
    "GPL-3.0": "GPL-3.0-only",
    "AGPL-3.0+": "AGPL-3.0-or-later",
    "AGPL-3.0": "AGPL-3.0-only"
}

def normalize_license(lic):
    return license_map.get(lic, lic)
    #return fl.expression_license(lic, update_dual=False)['identified_license']

def create_matrix():
    with open(RECLICENSE_LICENSES_CSV) as csvfile:

        reader = csv.reader(csvfile, delimiter=',')
        first_row = True
        compat_dict = {}
        compat_dict = {}

        for row in reader:
            if first_row:
                headers = row
                first_row = False
                for header in headers:
                    if header == 'license':
                        print("Ignoring \"license\"", file=sys.stderr)
                    compat_dict[normalize_license(header)] = {}

            else:
                #print(str(row))
                row_index = 0
                for col in row:
                    if row_index == 0:
                        current_lic = col
                        #print("current_lic: " + current_lic)
                    else:
                        #print("    " + str(row_index) + "  " + headers[row_index] + ": " + str(col))
                        compat_dict[normalize_license(headers[row_index])][normalize_license(current_lic)] = col
                        pass
                    row_index += 1
    return compat_dict

matrix = {
    "meta": {
        'description': f'This is a JSON version (with additional meta data and some license normalizations) of the CSV provided by Open Source Software Data Analytics Lab@PKU-SEI. It is mainly intended for use by {module_name} ({repo}).',
        'disclaimer': disclaimer,
        'created': {
            'date': f'{datetime.datetime.now()}',
            'tool_url': repo,
            'tool_name': module_name,
            'tool_version': version,
        },
        'origin': {
            'matrix_url': 'https://raw.githubusercontent.com/osslab-pku/RecLicense/refs/heads/master/knowledge_base/files%20for%20program%20input/compatibility_63.csv',
            'homepage': 'https://licenserec.com/',
            'repository': 'https://github.com/osslab-pku/RecLicense',
            'license': {
                'license_repo_url': 'https://github.com/osslab-pku/RecLicense/?tab=License-1-ov-file#readme',
                'license_url': 'http://license.coscl.org.cn/MulanPubL-2.0',
                'license_osi_url': 'https://opensource.org/license/mulanpsl-2-0',
                'license_spdx_url': 'https://spdx.org/licenses/MulanPSL-2.0.html',
                'license_scancode_url': 'https://scancode-licensedb.aboutcode.org/mulanpsl-2.0.html',
                'license_scancode_en_url': 'https://scancode-licensedb.aboutcode.org/mulanpsl-2.0-en.html',
                'spdxid': 'MulanPubL-2.0'
            }
        }
    },
    "licenses": create_matrix()
}

#print(json.dumps(matrix, indent=4))

VAR_DIR = os.path.join(os.path.dirname(__file__), '..')
VAR_DIR = os.path.join(VAR_DIR, 'licomp_reclicense')
VAR_DIR = os.path.join(VAR_DIR, 'var')
MATRIX_FILE=os.path.join(VAR_DIR, 'reclicense-matrix.json')

#print(json.dumps(matrix, indent=4))
#sys.exit(0)

with open(MATRIX_FILE, 'w') as fp:
    json.dump(matrix, fp, indent=4)

