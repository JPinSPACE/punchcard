#!/usr/bin/python

import sqlite3 as lite
import sys
import getopt
import random
import json
import datetime

def help():
    print "Usage: initialize_db.py [-c, --clean] [-s, --sample] [-h, --help]"
    print "-c, --clean - Wipe all data and start with fresh tables."
    print "-s, --sample - Must be used with 'clean', generates sample data"
    print "-h, --help - Display this helpful information."
    sys.exit(0)

clean = False
sample = False

try:
    long_flags = ['clean', 'sample', 'help']
    opts, args = getopt.getopt(sys.argv[1:], 'csh', long_flags)
except getopt.GetoptError:
    help()

for opt,args in opts:
    if opt in ('-c', '--clean'):
        print "Are you sure? This will wipe out ALL data and start",
        print "with a new database."
        decision = raw_input('Type "yes" to continue: ')
        if decision != 'yes':
            print "Exiting..."
            sys.exit(0)
        clean = True
    elif opt in ('-s', '--sample'):
        sample = True
    elif opt in ('-h', '--help'):
        help()

# sample data only allowed when cleaning the database
if sample is True and clean is not True:
    sample = False

try:
    conn = lite.connect('punchcard.db')
except lite.Error, e:
    print "Error %s:" % e.args[0]
    sys.exit(1)

cur = conn.cursor()
if clean is True:
    try:
        cur.execute("DROP TABLE data")
        print "Dropped table 'data'"
    except lite.Error, e:
        print "Table 'data' was not present"

    try:
        cur.execute("DROP TABLE views")
        print "Dropped table 'views'"
    except lite.Error, e:
        print "Table 'views' was not present"

    try:
        cur.execute("DROP TABLE sequences")
        print "Dropped table 'sequences'"
    except lite.Error, e:
        print "Table 'sequences' was not present"

try:
    cur.execute("CREATE TABLE data(sequence TEXT, date TEXT, value REAL)")
    print "Created table 'data'"
except lite.Error, e:
    print "Table 'data' already exists. Use --clean or -c to wipe data."

try:
    cur.execute("CREATE TABLE views(name TEXT, type, TEXT, color_info TEXT)")
    print "Created table 'views'"
except lite.Error, e:
    print "Table 'views' already exists. Use --clean or -c to wipe data."

try:
    cur.execute("CREATE TABLE sequences(name TEXT, label TEXT)")
    print "Created table 'sequences'"
except lite.Error, e:
    print "Table 'sequences' already exists. Use --clean or -c to wipe data."

if sample is True:
    print "Inserting sample data.."

### BINARY SAMPLE #############################################################
    color_info = {'color' : (255, 255, 0) }
    color_info = json.dumps(color_info)
    cur.execute("INSERT INTO sequences (name, label)" + 
        "VALUES ('worked_out', 'Worked Out')")
    cur.execute("INSERT INTO views (name, type, color_info)" +
        "VALUES ('worked_out', 'binary', ?)", [color_info])

    d = datetime.date.today()
    day = datetime.timedelta(days=1)
    for i in range(20):
        cur.execute("INSERT INTO data (sequence, date, value)" +
            "VALUES ('worked_out', ?, ?)", [d.__str__(), random.randrange(2)])
        d += day

### ABSOLUTE SAMPLE ###########################################################
    color_info = {'color' : (0, 0, 255), 'shades' : 4 }
    color_info = json.dumps(color_info)
    cur.execute("INSERT INTO sequences (name, label)" + 
        "VALUES ('sleeping', 'Sleeping Quality')")
    cur.execute("INSERT INTO views (name, type, color_info)" +
        "VALUES ('sleeping', 'absolute', ?)", [color_info])

    d = datetime.date.today()
    day = datetime.timedelta(days=1)
    for i in range(20):
        cur.execute("INSERT INTO data (sequence, date, value)" +
            "VALUES ('sleeping', ?, ?)", [d.__str__(), random.randrange(4)])
        d += day



conn.commit()
conn.close()
