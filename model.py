import sqlite3 as lite
import sys
import json

db_conn = None

### UTIL ######################################################################

# Retrieve db connection
#
# return - db handle
def get_conn():
    global db_conn
    if db_conn is not None:
        return db_conn
    else:
        try:
            db_conn = lite.connect('punchcard.db')
            db_conn.row_factory = lite.Row
            return db_conn
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

def fail(msg):
    print msg
    sys.exit(1)

### ALL DATA ##################################################################

# Get all data from all sequences
#
# return dict - dict of arrays of sequence data
def get_all_data():
    conn = get_conn()
    c = conn.cursor()

    c.execute("SELECT sequence, date, value FROM data ORDER BY date DESC")

    data = c.fetchall()

    sequences = {}
    for datum in data:
        if not sequences.has_key(datum['sequence']):
            sequences[datum['sequence']] = []
        sequences[datum['sequence']].append({
            'date'  : datum['date'],
            'value' : datum['value'],
        })

    return sequences

### SEQUENCE ##################################################################

# Add sequence with optional data
#
# param seq - dict - sequence name and label
# param view - dict - information required for this view type
# param data - dict - OPTIONAL - data for the sequence
#
# return True - success
def add_sequence(seq, view, data=None):
    conn = get_conn()
    c = conn.cursor()

    if 'name' not in seq:
        fail('add_sequence - sequence is missing attribute "name"')
    if 'label' not in seq:
        fail('add_sequence - sequence is missing attribute "label"')

    if 'type' not in view:
        fail('add_sequence - view is missing attribute "type"')
    if 'color_info' not in view:
        fail('add_sequence - view is missing attribute "color_info"')

    c.execute("INSERT INTO sequences (name, label) "
        "VALUES (?, ?)", [seq.name, seq.label])

    c.execute("INSERT INTO views (name, type, color_info) "
        "VALUES (?, ?, ?)", [seq.name, view.type, view.color_info])

    if data is not None:
        for datum in data.keys():
            c.execute("INSERT INTO data (sequence, date, value) "
                "VALUES (?, ?, ?)", [seq.name, datum, data[datum]])

    conn.commit()

    return True

# update sequence attributes
#
# param seq - string - name of sequence to update
# param label - string - OPTIONAL - new label for sequence
# param data - dict - OPTIONAL - replace existing sequence data with this data
#
# return True - success
def update_sequence(seq, label=None, data=None):
    if label is None and data is None:
        return True

    conn = get_conn()
    c = conn.cursor()

    if label is not None:
        c.execute("UPDATE sequences SET label = ? "
            "WHERE name = ? LIMIT 1", [label])

    if data is not None:
        c.execute("DELETE FROM data WHERE sequence = ?", [seq])
        for datum in data.keys():
            c.execute("INSERT INTO data (sequence, date, value) "
                "VALUES (?, ?, ?)", [seq, datum, data[datum]])

    conn.commit()

# get all data for one sequence
#
# param seq - string - sequence name
#
# returns dict - dates and values
def get_sequence_data(seq):
    conn = get_conn()
    c = conn.cursor()

    c.execute("SELECT date, value FROM data "
        "WHERE sequence = ? ORDER BY date DESC", (seq,))

    raw_data = c.fetchall()
    data = {}

    for datum in raw_data:
        data[datum['date']] = datum['value']

    return data

def get_sequence_names():
    conn = get_conn()
    c = conn.cursor()

    c.execute("SELECT name FROM sequences ORDER BY name ASC")

    sequences = c.fetchall()

    return [ row['name'] for row in sequences ]

# add one datum to one sequence
#
# param seq - string - sequence name
# param date - string - date
# param value - float - value
#
# return True - success
def add_to_sequence(seq, date, value):
    conn = get_conn()
    c = conn.cursor()

    c.execute("INSERT INTO data (sequence, date, value) "
        "VALUES (?, ?, ?)", [seq, date, value])

    conn.commit()

    return True

# delete an entire sequence
#
# param seq - string - sequence name
# param remove_view  - boolean - defaults to True, removes associated view
#
# return True - success
def delete_sequence(seq, remove_view=True):
    conn = get_conn()
    c = conn.cursor()

    c.execute("DELETE FROM sequences WHERE name = ? LIMIT 1", [seq])
    c.execute("DELETE FROM data WHERE sequence = ?", [seq])
    c.execute("DELETE FORM views WHERE name = ?", [seq])

    conn.commit()

    return True

### VIEWS #####################################################################

# create new view
def add_view (name, type, color_info):
    color_info = json.dumps(color_info)

    conn = get_conn()
    c = conn.cursor()

    c.execute("INSERT INTO views (name, type, color_info) "
        "VALUES (?, ?, ?)", [name, type, color_info])

    conn.commit()

    return True


# delete existing view. will fail if view is in use (TODO)
def delete_view (name):
    conn = get_conn()
    c = conn.cursor()

    c.execute("DELETE FROM views WHERE name = ? LIMIT 1", [name])

    conn.commit()

    return True

# retrieve view
def get_view (name):
    conn = get_conn()
    c = conn.cursor()

    c.execute("SELECT type, color_info "
              "FROM views WHERE name = ? LIMIT 1", (name,))

    view = c.fetchone()

    return {
            'type' : view['type'],
            'color_info' : view['color_info'],
            }

# update view's type and/or color_info
def update_view (name, type=None, color_info=None):
    if type is None and color_info is None:
        return True

    conn = get_conn()
    c = conn.cursor()

    if type is not None:
        c.execute("UPDATE views SET type = ? WHERE name = ? LIMIT 1",
            [type, name])

    if color_info is not None:
        c.execute("UPDATE views SET color_info = ? WHERE name = ? LIMIT 1",
            [color_info, name])

    conn.commit()

    return True


### DATUM #####################################################################

# add one datum
def add_datum(seq, date, value):
    conn = get_conn()
    c = conn.cursor()

    c.execute("SELECT value FROM data WHERE seq = ? AND date = ?", [seq, date])
    existing = c.fetchone()

    if existing is not None:
        return False

    c.execute("INSERT INTO data (sequence, date, value) "
        "VALUES (?, ?, ?)", [seq, date, value])

    conn.commit()

    return True

# get one datum, i.e., data for one sequence at a specific date
def get_datum(seq, date):
    conn = get_conn()
    c = conn.cursor()

    c.execute("SELECT value FROM data WHERE sequence = ? AND date = ?",
        [seq, date])

    value = c.fetchone()

    return value

# update one specific datum
def update_datum(seq, date, value):
    conn = get_conn()
    c = conn.cursor()

    c.execute("UPDATE data SET value = ? WHERE sequence = ? AND date = ?",
        [value, sequence, date])
    
    conn.commit()

    return True

# delete one specific datum
def delete_datum(seq, date):
    conn = get_conn()
    c = conn.cursor()

    c.execute("DELETE FROM data WHERE sequence = ? and date = ? LIMIT 1",
        [seq, date])
    
    conn.commit()

    return True
