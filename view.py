from string import Template

def get_html_from_sequences(sequences):
    SATURATION = 80
    MAX_LIGHT = 100
    MIN_LIGHT = 50
    LIGHT_RANGE = MAX_LIGHT - MIN_LIGHT

    t = open('templates/row.html', 'r')
    row = Template(t.read())
    t = open('templates/cell.html', 'r')
    cell = Template(t.read())

    length = max([len(seq) for seq in sequences])

    table = ''

    for i in range(length):
        this_row = ''
        for seq in sequences:
            light = LIGHT_RANGE * (1.0 - sequences[seq]['value'][i]) + MIN_LIGHT
            color = "hsl(%d, %d%%, %d%%)" % (sequences[seq]['hue'],
                                             SATURATION,
                                             light)
            this_row += cell.substitute({ 'color' : color })
        table += row.substitute({'row_cells' : this_row })

    return table

def output_page(table):
    print "Content-Type: text/html;charset=utf-8"
    print

    t = open('templates/main.html', 'r')
    main_page = Template(t.read())

    print main_page.substitute({'table_rows' : table})
