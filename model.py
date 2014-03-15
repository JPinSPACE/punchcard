import sqlite3 as lite
import sys

db_conn = None

def get_conn():
    global db_conn
    if db_conn is not None:
        return db_conn
    else:
        try:
            db_conn = lite.connect('punchcard.db')
            return db_conn
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

### ALL DATA ##################################################################

# get all data from all sequences
def get_all_data():
    pass

### SEQUENCE ##################################################################

# add sequence with optional data
def add_sequence(name, color, type, data=None):
    pass

# update sequence attributes
def update_sequence(name, new_data):
    pass

# get all data for one sequence
def get_sequence(seq):
    pass

# add one datum to one sequence
def add_to_sequence(seq, date):
    pass

# delete an entire sequence
def delete_sequence(seq):
    pass

### DATUM #####################################################################

# add one datum
def add_datum(seq, date, datum):
    pass

# get one datum, i.e., data for one sequence at a specific date
def get_datum(seq, date):
    pass

# update one specific datum
def update_datum(seq, date, datum):
    pass

# delete one specific datum
def delete_datum(seq, date):
    pass

### DATE ######################################################################

# add date with optional data
# if no data is passed, it will be entered as zeroes
def add_date(date, date=None):
    pass

# update all data for one date, i.e. the datum for each sequence on this date
def update_date_data(date, date):
    pass

# delete all data for a date and remove the date entirely
def delete_date(date):
    pass
