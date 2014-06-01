from string import Template

def get_html_from_sequences(sequences):
    SATURATION = 80

    t = open('templates/row.html', 'r')
    row = Template(t.read())
    t = open('templates/cell.html', 'r')
    cell = Template(t.read())

    length = max([len(seq) for seq in sequences])

    table = ''

    for i in range(length):
        this_row = ''
        for seq in sequences:
            color = "hsl(%d, %d%%, %d%%)" % (sequences[seq]['hue'],
                                             SATURATION,
                                             sequences[seq]['light'][i])
            this_row += cell.substitute({ 'color' : color })
        table += row.substitute({'row_cells' : this_row })

    return table

def output_page(table):
    print "Content-Type: text/html;charset=utf-8"
    print

    t = open('templates/main.html', 'r')
    main_page = Template(t.read())

    print main_page.substitute({'table_rows' : table})
