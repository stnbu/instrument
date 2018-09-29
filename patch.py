#!/usr/bin/env python
"""A quick-and-dirty utility to patch python source files so that they are instrumented
"""

import os
import re


magic = """
import instrument
instrument.instrument_this_module()
"""

def patch_files(paths):
    # not perfect, but perfect enough
    name_main_re = re.compile('.*if.* .*__name__.*==.*__main__')
    for path in paths:
        orig = open(path, 'r')
        with open(path+'.new', 'w') as new:
            for line in orig:
                if name_main_re.match(line):
                    new.write(magic)
                new.write(line)
            else:
                new.write(magic)
        orig.close()

        os.rename(path+'.new', path)


if __name__ == '__main__':

    import sys
    patch_files(sys.argv[1:])

    
