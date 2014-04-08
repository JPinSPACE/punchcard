from string import Template
import random
import model

def get_color_tmp(series, i):
    value = series['data'][i]
    if series['type'] == 'binary':
        if value == 1:
            return 'hsl(' + str(series['color']) + ', 80%, 50%)'
        else:
            return '#ffffff'
    elif series['type'] == 'absolute':
        inc = 70 / (series['max'] - series['min'])
        light = 100 - value * inc
        return "hsl(%d, 80%%, %d%%)" % (series['color'], light)
    elif series['type'] == 'relative':
        inc = 70 / (max(series['data']) - min(series['data']))
        light = 100 - value * inc
        return "hsl(%d, 80%%, %d%%)" % (series['color'], light)
    else:
        return '#ffffff'

def random_data(length, choices):
    sequence = []
    for i in range(length):
        sequence.append(random.randrange(choices))
    return sequence

def get_transformed_data():
    sequences = model.get_sequence_names()

    all_sequence_data = {}

    for sequence in sequences:
        data = model.get_sequence_data(sequence)
        view = model.get_view(sequence)
        all_sequence_data[sequence] = transform_data(data, view)

    return all_sequence_data

def transform_data(data, view):
    for i in range(len(data)):
        data[i] = get_color(data[i], view)

    return data

def get_color(value, view):
    color = view['color']
    if view['type'] == 'binary':
        if value == 1:
            return 'hsl(' + str(view['color']) + ', 80%, 50%)'
        else:
            return '#ffffff'
    elif view['type'] == 'absolute':
        inc = 70 / (view['max'] - view['min'])
        light = 100 - value * inc
        return "hsl(%d, 80%%, %d%%)" % (view['color'], light)
    elif view['type'] == 'relative':
        inc = 70 / (max(view['data']) - min(view['data']))
        light = 100 - value * inc
        return "hsl(%d, 80%%, %d%%)" % (view['color'], light)
    else:
        return '#ffffff'



def main():
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
    columns = 2

    # fake data is the best data
    data = []
    data.append({
        'data'  : random_data(grid_length, 2),
        'color' : random.randint(0, 359),
        'type'  : 'binary',
    })
    data.append({
        'data'  : random_data(grid_length, 2),
        'color' : random.randint(0, 359),
        'type'  : 'binary',
    })

    data.append({
        'data'  : random_data(grid_length, 4),
        'color' : random.randint(0, 359),
        'type'  : 'absolute',
        'min'   : 0,
        'max'   : 3,
    })
    data.append({
        'data'  : random_data(grid_length, 8),
        'color' : random.randint(0, 359),
        'type'  : 'absolute',
        'min'   : 0,
        'max'   : 7,
    })

    data.append({
        'data'  : random_data(grid_length, 8),
        'color' : random.randint(0, 359),
        'type'  : 'relative',
    })
    data.append({
        'data'  : random_data(grid_length, 8),
        'color' : random.randint(0, 359),
        'type'  : 'relative',
    })



    data[4]['data'][0] = 50
    
    for i in range(len(data[5]['data'])):
        if i % 5 != 0:
            data[5]['data'][i] += 20


    table_rows = ''
    for i in range(grid_length):
        this_row = ''
        for col in data:
            color = get_color_tmp(col, i)
            this_row += cell.substitute( {'color' : color })
        table_rows += row.substitute({'row_cells' : this_row})

    print main.substitute({'table_rows':table_rows})
