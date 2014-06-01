import model
import view
import datetime
import json

GRID_LENGTH = 20

def get_data():
    raw_data = {}
    values = {}
    views = {}
    max_value = {}

    transformed = {}

    seqs = model.get_sequence_names()

    # retrieve data
    for seq in seqs:
        max_value[seq] = 0
        values[seq] = []
        views[seq] = {}

        seq_dict = {}
        raw_data[seq] = model.get_sequence_data(seq)

        views[seq] = model.get_view(seq)


    d = datetime.date.today()
    day = datetime.timedelta(days=1)

    # build out grid substituting zeroes for no-data days
    for i in range(GRID_LENGTH):
        date = d.__str__()

        for seq in seqs:
            if date in raw_data[seq].keys():
                # since we're already iterating over this we may
                # as well grab the maximum value now
                if raw_data[seq][date] > max_value[seq]:
                    max_value[seq] = raw_data[seq][date]
                values[seq].append(raw_data[seq][date])
            else:
                values[seq].append(0)

        d -= day

    for seq in seqs:
        transformed[seq] = {}
        color_info = json.loads(views[seq]['color_info'])

        transformed[seq]['hue'] = color_info['hue']
        transformed[seq]['light'] = []

        if views[seq]['type'] == 'binary':
            for value in values[seq]:
                if value == 1:
                    transformed[seq]['light'].append(50)
                else:
                    transformed[seq]['light'].append(100) # full light is white
        else: #temporarily pad with zeros
            for value in values[seq]:
                transformed[seq]['light'].append(100)

    return transformed


def main():
    data = get_data()

    table = view.get_html_from_sequences(data)

    view.output_page(table)
