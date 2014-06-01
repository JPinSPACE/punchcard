import model
import view
import datetime
import json

GRID_LENGTH = 20

# Transform database data into values between 0.0 and 1.0, representing
# the intensity of that data point
def get_data():
    raw_data = {}
    values = {}
    views = {}
    max_value = {}
    min_value = {}

    transformed = {}

    seqs = model.get_sequence_names()

    # retrieve data
    for seq in seqs:
        max_value[seq] = 0
        min_value[seq] = None
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
                if views[seq]['type'] == 'relative':
                    value = raw_data[seq][date]
                    # since we're already iterating over this we may
                    # as well grab the max/min values now
                    if value > max_value[seq]:
                        max_value[seq] = raw_data[seq][date]

                    if min_value[seq] is None or value < min_value[seq]:
                        min_value[seq] = raw_data[seq][date]

                values[seq].append(raw_data[seq][date])
            else:
                values[seq].append(0)

        d -= day

    for seq in seqs:
        transformed[seq] = {}
        color_info = json.loads(views[seq]['color_info'])

        transformed[seq]['hue'] = color_info['hue']
        transformed[seq]['value'] = []

        view_type = views[seq]['type']

        if view_type == 'binary':
            for value in values[seq]:
                if value == 1:
                    transformed[seq]['value'].append(1)
                else:
                    transformed[seq]['value'].append(0)
        elif view_type == 'absolute' or view_type == 'relative':
            if view_type == 'relative':
                value_range = max_value[seq] - min_value[seq]
            else:
                value_range = color_info['shades']

            step = 1.0 / value_range
            for value in values[seq]:
                # run through min() to account for imprecise division
                fixed_value = min(1.0, value * step)
                transformed[seq]['value'].append(fixed_value)
        else: # unimplemented type, zero it out
            for value in values[seq]:
                transformed[seq]['value'].append(0)

    return transformed


def main():
    data = get_data()

    table = view.get_html_from_sequences(data)

    view.output_page(table)
