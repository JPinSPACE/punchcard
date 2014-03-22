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
def add_sequence(seq, view, data=None):
    pass

# update sequence attributes
def update_sequence(seq, view=None, data=None):
    pass

# get all data for one sequence
def get_sequence(seq):
    pass

# add one datum to one sequence
def add_to_sequence(seq, date, value):
    conn = get_conn()
    c = conn.cursor()

    c.execute("INSERT INTO data (sequence, date, value)" +
        "VALUES (?, ?, ?)", seq, date, value)

    c.commit()
    c.close()

# delete an entire sequence
def delete_sequence(seq):
    pass

### VIEWS #####################################################################

# create new view
def add_view (view, type, color_info):
    pass

# delete existing view. will fail if view is in use
def delete_view (view):
    pass

# update view's type and/or color_info
def update_view (view, type=None, color_info=None):
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
