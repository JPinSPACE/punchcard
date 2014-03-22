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

def fail(msg):
    print msg
    sys.exit(1)

### ALL DATA ##################################################################

# get all data from all sequences
def get_all_data():
    pass


### SEQUENCE ##################################################################

# add sequence with optional data
def add_sequence(seq, view, data=None):
    conn = get_conn()
    c = conn.cursor()

    if 'name' is not in seq:
        fail('add_sequence - sequence is missing attribute "name"')
    if 'label' is not in seq:
        fail('add_sequence - sequence is missing attribute "label"')

    if 'type' is not in view:
        fail('add_sequence - view is missing attribute "type"')
    if 'color_info' is not in view:
        fail('add_sequence - view is missing attribute "color_info"')

    c.execute("INSERT INTO sequences (name, label)" +
        "VALUES (?, ?)", [seq.name, seq.label])

    c.execute("INSERT INTO views (name, type, color_info)" +
        "VALUES (?, ?, ?)", [seq.name, view.type, view.color_info])

    if data is not None:
        for datum in data:
            c.execute("INSERT INTO data (sequence, date, value)" +
                "VALUES (?, ?, ?)", [seq.name, datum.date, datum.value])

    c.commit()
    c.close()

# update sequence attributes
def update_sequence(seq, view=None, data=None):
    pass

# get all data for one sequence
#
# param seq - string - sequence name
# returns dict - dates and values
def get_sequence_data(seq):
    conn = get_conn()
    c = conn.cursor()

    c.execute("SELECT date, value FROM data" +
        "WHERE sequence = ? ORDER BY date DESC")

    data = c.fetchall()

    c.close()

    return data

# add one datum to one sequence
def add_to_sequence(seq, date, value):
    conn = get_conn()
    c = conn.cursor()

    c.execute("INSERT INTO data (sequence, date, value)" +
        "VALUES (?, ?, ?)", [seq, date, value])

    c.commit()
    c.close()

# delete an entire sequence
def delete_sequence(seq, remove_view=True):
    conn = get_conn()
    c = conn.cursor()

    c.execute("DELETE FROM sequences WHERE name = ? LIMIT 1", [seq])
    c.execute("DELETE FROM data WHERE sequence = ?", [seq])
    c.execute("DELETE FORM views WHERE name = ?", [seq])
    c.commit()
    c.close()

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
