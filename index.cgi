#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
cgitb.enable()

from string import Template
import random

def get_color(series, i):
    value = series['data'][i]
    if value == 1:
        return 'hsl(' + str(series['color']) + ', 100%, 50%)'
    else:
        num = random.randint(220,240)
        return '#%02x%02x%02x' % (num, num, num)

def random_data(n):
    sequence = []
    for i in range(n):
        sequence.append(random.randrange(2))
    return sequence

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

# temporary nonsense
grid_length = 80
columns = 30
r = lambda: random.randint(0,255)

data = []
for i in range(columns):
    data.append({
        'data'  : random_data(grid_length),
        'color' : random.randint(0, 359),
        'type'  : 'binary',
    })


table_rows = ''

for i in range(grid_length):
    this_row = ''
    for col in data:
        color = get_color(col, i)
        this_row += cell.substitute( {'color' : color })
    table_rows += row.substitute({'row_cells' : this_row})

print main.substitute({'table_rows':table_rows})


