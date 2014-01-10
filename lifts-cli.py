"""

---
Lifts CLI
~~~~~~~~~

Main interface used to modify logs. Can also directly edit flat file
database.

"""

import sys
import database

DATAFILE = 'data/lifts.db'

def usage():
    print 'Usage:'
    print '  add: python lift-cli.py add date liftname weightxrep1 weightxrep2 \n       weightxrep3.. "notes notes notes"'
    print ''
    print '  date defaults to today if not included'
    print '  kg/lb defaults to lb if not included'
    print '  Units: --weight=kg --weight=lbs'

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
        sys.exit()
    
    with database.dbm(DATAFILE) as dbm:
        dbm.add_entry(' '.join(sys.argv[1:]))
    
