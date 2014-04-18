import model
import datetime

GRID_LENGTH = 20

def get_data():
    raw_data = {}
    values = {}

    seqs = model.get_sequence_names()

    # retrieve data and build dictionary keyed on date
    for seq in seqs:
        values[seq] = []

        seq_dict = {}
        seq_data = model.get_sequence_data(seq)

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
                values[seq].append(raw_data[seq][date])
            else:
                values[seq].append(0)

        d -= day

    return values



        

def main():
    values = get_data()

main()
