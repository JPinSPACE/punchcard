#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
cgitb.enable()

from string import Template

def get_color(value, color):
    if value == 1:
        return color
    else:
        return 'ffffff'

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

colors = {
    'alpha' : '9999ff',
    'beta'  : '00ff00',
    'delta' : '0000ff',
    'gamma' : '00ffff',
}

fake_data = {
    'alpha' : (0, 0, 1, 1, 0),
    'beta'  : (1, 1, 1, 1, 0),
    'delta' : (0, 0, 0, 1, 0),
    'gamma' : (1, 1, 1, 0, 0),
}

table_rows = ''

for i in range(5):
    this_row = ''
    for col in fake_data.keys():
        this_row += cell.substitute({'color' : get_color(fake_data[col][i], colors[col])})
    table_rows += row.substitute({'row_cells' : this_row})

print main.substitute({'table_rows':table_rows})


