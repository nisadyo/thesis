#!d:\caca\thesis\env\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'Gammatone==1.0','console_scripts','gammatone'
__requires__ = 'Gammatone==1.0'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('Gammatone==1.0', 'console_scripts', 'gammatone')()
    )
