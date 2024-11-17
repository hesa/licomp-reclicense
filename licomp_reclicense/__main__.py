#!/bin/env python3                                                                                                    

from licomp.interface import ObligationTrigger
from licomp.main_base import LicompParser

from licomp_reclicense.config import cli_name
from licomp_reclicense.config import description
from licomp_reclicense.config import epilog
from licomp_reclicense.reclicense import LicompReclicense

def main():
    lr = LicompReclicense()
    o_parser = LicompParser(lr,
                            name = cli_name,
                            description = description,
                            epilog = epilog,
                            default_trigger = ObligationTrigger.BIN_DIST)
    o_parser.run()

if __name__ == '__main__':
    main()




