"""

---
database.py
~~~~~~~~~~~

Lifts flatfile database accessing / querying functions.

"""

# For with clause, create new db_manager that connects
def dbm(db_file):
    return DB_Manager(db_file)

class DB_Manager():
    def __init__(self, db_file):
        self.db_file = db_file
        pass
    
    # __enter__ and __exit set to allow for with clause
    # returns an enabled DB_Manager
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def connect(self):
        self.db = open(self.db_file, 'r+')
    
    def close(self):
        self.db.close()

    def get_notes(self, entry):
        # Extract the note portion of an entry (assumes well formed)
        notes = None
        if '"' in entry:
            notes = '"' + entry.split('"')[1] + '"\n'

        return notes

    def get_date(self, entry):
        # Extract date from (assumes well formed)
        return entry.split(' ')[0]
    
    def get_liftname(self, entry):
        # Extract liftname from entry (assumes well formed)
        return entry.split(' ')[1]
    
    def get_unit(self, entry):
        # Returns 'kg' if set to kg, 'lbs' if not (assumes well formed)
        if entry.split(' ')[2] == 'kg':
            return 'kg'
        return 'lbs'

    def get_sets(self, entry):
        # Extract sets (as list) from entry (assumes well formed)
        cleaned = entry
        print entry.replace('\n', '')
        
        # Remove notes
        notes = self.get_notes(entry)
        if notes != None:
            cleaned = cleaned[:-len(notes)]

        # Remove date, liftname, kg/lbs (if set)
        elems = [x.replace('\n', '') for x in cleaned.split(' ')]
        elems = [x for x in elems if x != '']
        if elems[2] in ['kg', 'lbs']:
            return elems[3:]
        else:
            return elems[2:]

    def convert_entry_to_lbs(self, entry):
        kg_sets = self.get_sets(entry)
        lbs_sets = []
        for s in kg_sets:
            # Extract kg, reps (optional), remove failed if present
            kg = s.split('x')[0]
            reps = ''
            if 'x' in s:
                reps = 'x' + s.split('x')[1]
            failed = ''
            if '-' in s:
                failed = '-'
                kg = kg.split('-')[0]
                reps = reps.split('-')[0]

            lbs = int(round(float(kg) * 2.20462))
            lbs_sets.append('%s%s%s' % (str(lbs), reps, failed))

        return_entry = '%s %s %s' % (self.get_date(entry), self.get_liftname(entry), ' '.join(lbs_sets))
        if self.get_notes(entry) is not None:
            return return_entry + ' ' + self.get_notes(entry)
        else:
            return return_entry + '\n'

    def normalize_liftname(self, name):
        # Remove uppercase and spaces from lift name
        return name.replace(' ', '').lower()

    def process_results(self, result_list):
        # Processing entires:
        # - allow comments (starts with #)
        # - convert to kg if needed
        new_results = []
        for result in result_list:
            if result[0] == '#':
                new_results.append(result)
                continue
            elif ' kg ' in result:
                # Convert to lbs
                new_results.append(self.convert_entry_to_lbs(result))
            else:
                new_results.append(result)
                
        return new_results

    def add_entry(self, entry):
        # Insert entry to database at start of file, ensure newline at
        # end of entry
        contents = self.db.readlines()
        contents.insert(0, entry.replace('\n', '') + '\n')
        self.db.seek(0)
        self.db.write(''.join(contents))

    def search(self, name):
        # Search for entries with lift name
        contents = self.db.readlines()
        normal_name = self.normalize_liftname(name)
        results = [x for x in contents if normal_name in x]
        return self.process_results(results)

    def logs(self, limit):
        # Return most recent n logs by date
        # TODO: return by date not by exercise
        contents = self.db.readlines()
        return self.process_results(contents[:limit])
