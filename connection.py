# Eszter
import csv
import os
import time

DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/question.csv'
DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']


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
def write_new_question(new_question):
    new_question = new_question.to_dict()
    data = get_all_user_story()
    new_id = str(int(data[-1]['id']) + 1)
    submission_time = str(int(time.time()))
    new_question['id'] = new_id
    new_question['submission_time'] = submission_time
    with open(DATA_FILE_PATH, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=DATA_HEADER)
        writer.writeheader()
        for question_data in data:
            writer.writerow(question_data)
        writer.writerow(new_question)
    return new_id
#  Eniko



