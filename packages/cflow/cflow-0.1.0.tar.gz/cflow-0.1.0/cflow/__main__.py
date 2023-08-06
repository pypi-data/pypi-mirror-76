from __future__ import print_function

import sys
import cflow

try:
    exit_code = cflow.Runner.invoke(sys.argv)
except RuntimeError as err:
    print('\033[1;31m' + str(err) + '\033[0m')
    exit_code = 1

sys.exit(exit_code or 0)
