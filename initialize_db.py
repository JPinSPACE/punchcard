#!/usr/bin/python

import sqlite3 as lite
import sys
import getopt
import random

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
    cur.execute("DROP TABLE data")
    cur.execute("DROP TABLE views")
    cur.execute("DROP TABLE sequences")

try:
    cur.execute("CREATE TABLE data(sequence TEXT, date TEXT, value REAL)")
except lite.Error, e:
    print "Table 'data' already exists. Use --clean or -c to wipe data."

try:
    cur.execute("CREATE TABLE views(name TEXT, type, TEXT, color_info BLOB")
except lite.Error, e:
    print "Table 'views' already exists. Use --clean or -c to wipe data."

try:
    cur.execute("CREATE TABLE sequences(name TEXT, view TEXT)")
except lite.Error, e:
    print "Table 'sequences' already exists. Use --clean or -c to wipe data."


# TODO: generate sample data if requested