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

    def normalize_liftname(self, name):
        # Remove uppercase and spaces from lift name
        return name.replace(' ', '').lower()

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
        return results

    def logs(self, limit):
        # Return most recent n logs by date
        # TODO: return by date not by exercise
        contents = self.db.readlines()
        return contents[:limit]
