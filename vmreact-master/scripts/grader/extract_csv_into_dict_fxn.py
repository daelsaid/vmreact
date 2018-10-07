import csv
def extract_data_from_csv_into_dict(csv_file_to_extract):
    dict_name = []
    with open(csv_file_to_extract, 'U') as file:
        input_csv_lines = csv.reader(file)
        input_csv_lines = map(list, zip(*input_csv_lines))
        dict_name = csv_file_to_extract.split('.')[0] + '_dict'
        new_dict = dict((rows[0], rows[1:]) for rows in input_csv_lines)
        return new_dict
