import sys

DATAFILE = 'data/lifts.db'

def usage():
    print 'Usage:'
    print '  add: python lift-cli.py add date liftname weightxrep1 weightxrep2 \n       weightxrep3.. "notes notes notes"'
    print ''
    print '  date defaults to today if not included'
    print '  kg/lb defaults to lb if not included'
    print '  Units: --weight=kg --weight=lbs'

def add_entry(entry):
    """Insert to data file at start, ensure newline at end of entry"""
    
    with open(DATAFILE, 'r+') as f:
        contents = f.readlines()
        contents.insert(0, entry.replace('\n', '') + '\n')
        f.seek(0)
        f.write(''.join(contents))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
        sys.exit()
    
    add_entry(' '.join(sys.argv[1:]))
    
