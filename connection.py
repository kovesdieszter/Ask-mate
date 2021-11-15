# Eszter
import csv
import os

DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/question.csv'
DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']


def get_header():
    return DATA_HEADER


def get_all_user_story():
    data = []
    with open(DATA_FILE_PATH, mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    return data

#Eszter


#  Bea
#  Bea

#  Dia
#  Dia

#  Eniko
#  Eniko



