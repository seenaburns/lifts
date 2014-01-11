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
    print '  add: python lifts-cli.py add date liftname weightxrep1 weightxrep2 \n'+\
          '       weightxrep3.. "notes notes notes"'
    print '  search: python lifts-cli.py search liftname'
    print ''
    print '  Alternatively, the data file can be editted directly'
    print ''
    print '  date defaults to today if not included'
    print '  kg/lb defaults to lb if not included'
    print '  Units: --weight=kg --weight=lbs'

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
        sys.exit()
    
    with database.dbm(DATAFILE) as dbm:
        if sys.argv[1] == 'add':
            dbm.add_entry(' '.join(sys.argv[1:]))
        elif sys.argv[1] == 'search':
            print dbm.search(sys.argv[2])
        else:
            print 'Unrecognized command: %s' % (sys.argv[2])
            print ''
            usage()
