import csv
#  Bea
#  Bea

#  Dia


def read_from_csv(csv_title):
    lines_to_read = []
    with open(csv_title, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            lines_to_read.append(row)
    return lines_to_read  # a list of the lines(dictionaries) read out from the csv file

#  Dia

#  Eniko
#  Eniko

#  Eszter
#  Eszter
