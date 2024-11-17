#!/bin/env python3

import json
import os

from licomp_reclicense.config import module_name
from licomp_reclicense.config import version

from licomp.interface import Licomp
from licomp.interface import ObligationTrigger
from licomp.interface import ModifiedTrigger
from licomp.interface import CompatibilityStatus

SCRIPT_DIR = os.path.dirname(__file__)
VAR_DIR = os.path.join(SCRIPT_DIR,'var')
MATRIX_FILE_NAME = 'reclicense-matrix.json'
MATRIX_FILE = os.path.join(VAR_DIR,MATRIX_FILE_NAME)

class LicompReclicense(Licomp):

    def __init__(self):
        Licomp.__init__(self)
        self.obligation_triggers = [ ObligationTrigger.BIN_DIST, ObligationTrigger.SOURCE_DIST]
        with open (MATRIX_FILE) as fp:
            self.matrix = json.load(fp)
            self.licenses = self.matrix['licenses']

        self.ret_statuses = {
            "1": CompatibilityStatus.COMPATIBLE,
            "2": CompatibilityStatus.COMPATIBLE,
            "1,2": CompatibilityStatus.COMPATIBLE,
            "0": CompatibilityStatus.INCOMPATIBLE,
        }
    
    def _outbound_inbound_compatibility(self,
                                       outbound,
                                       inbound,
                                       trigger,
                                       modified):
        
        values = self.licenses[outbound][inbound]

        return self.outbound_inbound_reply(self.ret_statuses[values],
                                           f'values from matrix: {values}')

    def name(self):
        return module_name

    def version(self):
        return version

    def supported_licenses(self):
        return list(self.licenses.keys())
        
    def supported_triggers(self):
        return self.obligation_triggers

    def _status_to_licomp_status(self, status):
        return self.ret_statuses[status]

