# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
import sys
import traceback

from prettyprinter import pprint

from .. import get_setup_attrs

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        cwd = (argv + [os.getcwd()])[1]
        setup_attrs = get_setup_attrs(cwd)
        long_description = setup_attrs['long_description']
        if long_description and len(long_description) > 205:
            setup_attrs['long_description'] = long_description[:200] + '...'
        pprint(setup_attrs)
    except Exception: # pylint: disable=W0703
        traceback.print_exc()

if __name__ == '__main__':
    main()
