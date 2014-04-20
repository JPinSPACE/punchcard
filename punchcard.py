import model
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

    # retrieve data and build dictionary keyed on date
    for seq in seqs:
        max_value[seq] = 0
        values[seq] = []
        views[seq] = {}

        seq_dict = {}
        seq_data = model.get_sequence_data(seq)

        view = model.get_view(seq)
        views[seq]['type'] = view[0]
        views[seq]['color_info'] = view[1]

        for datum in seq_data:
            seq_dict[datum[0]] = datum[1]

        raw_data[seq] = seq_dict

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
        transformed[seq] = []
        color_info = json.loads(views[seq]['color_info'])

        if views[seq]['type'] == 'binary':
            for value in values[seq]:
                if value == 1:
                    transformed[seq].append(color_info['color'])
                else:
                    transformed[seq].append([0, 0, 0])

    print transformed




        

def main():
    data = get_data()


main()
