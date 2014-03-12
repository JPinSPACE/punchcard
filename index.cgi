#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
cgitb.enable()

from string import Template

def get_color(value):
    if value == 1:
        return 'ffffff'
    else:
        return '000000'

# print header
print "Content-Type: text/html;charset=utf-8"
print


# read in all templates
t = open('templates/main.html', 'r')
main = Template(t.read())
t = open('templates/row.html', 'r')
row = Template(t.read())
t = open('templates/cell.html', 'r')
cell = Template(t.read())

fake_data = {
    'alpha' : (0, 0, 1, 1, 0),
    'beta'  : (1, 1, 1, 1, 0),
    'delta' : (0, 0, 0, 1, 0),
    'gamma' : (1, 1, 1, 0, 0),
}

table_rows = ''

for i in range(5):
    row = ''
    for col in fake_data.keys():
        row += cell.substitute({'color' : get_color(fake_data[col][i])})
    table_rows += row

print main.substitute({'table_rows':table_rows})


