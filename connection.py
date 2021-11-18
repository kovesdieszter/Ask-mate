# Eszter
import csv
import os
import time

DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/question.csv'
ANSWER_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/answer.csv'
DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_all_user_story(datatype_file):
    data = []
    with open(datatype_file, mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    return data


def delete_q(id):
    data = get_all_user_story(DATA_FILE_PATH)
    with open(DATA_FILE_PATH, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=DATA_HEADER)
        writer.writeheader()
        for item in data:
            if item['id'] != id:
                writer.writerow(item)


def delete_a(id):
    data = get_all_user_story(ANSWER_FILE_PATH)
    with open(ANSWER_FILE_PATH, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=ANSWER_HEADER)
        writer.writeheader()
        for item in data:
            if item['id'] != id:
                writer.writerow(item)
            else:
                question_id = item['question_id']
    return question_id
#Eszter


#  Bea
#  Bea

#  Dia
def write_new_answer(new_answer, question_id):
    new_answer = new_answer.to_dict()
    data = get_all_user_story(ANSWER_FILE_PATH)
    new_id = str(int(data[-1]['id']) + 1)
    submission_time = str(int(time.time()))
    new_answer['question_id'] = question_id
    new_answer['id'] = new_id
    new_answer['submission_time'] = submission_time
    new_answer['vote_number'] = 0  # initial vote number
    del new_answer['title']
    with open(ANSWER_FILE_PATH, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=ANSWER_HEADER)
        writer.writeheader()
        for question_data in data:
            writer.writerow(question_data)
        writer.writerow(new_answer)
    return new_id
#  Dia

#  Eniko
def change_vote(question, changer, datatype_file):
    data = get_all_user_story(datatype_file)
    with open(datatype_file, 'w', newline='') as file:
        if datatype_file == DATA_FILE_PATH:
            writer = csv.DictWriter(file, fieldnames=DATA_HEADER)
        elif datatype_file == ANSWER_FILE_PATH:
            writer = csv.DictWriter(file, fieldnames=ANSWER_HEADER)
        writer.writeheader()
        for question_data in data:
            if question_data['id'] == question['id']:
                if int(question_data.get('vote_number')) == 0 and changer == -1:
                    question_data['vote_number'] = 0  # Do not -1 from vote number if it is already zero
                else:
                    question_data['vote_number'] = int(question_data.get('vote_number', 0)) + changer
                while len(str(question_data['vote_number'])) != 3:
                    question_data['vote_number'] = "0" + str(question_data['vote_number'])
                writer.writerow(question_data)
            else:
                writer.writerow(question_data)


def write_new_question(new_question):
    new_question = new_question.to_dict()
    data = get_all_user_story(DATA_FILE_PATH)
    new_id = str(int(data[-1]['id']) + 1)
    submission_time = str(int(time.time()))
    new_question['id'] = new_id
    new_question['submission_time'] = submission_time
    new_question['view_number'] = '0000'
    new_question['vote_number'] = '000'
    with open(DATA_FILE_PATH, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=DATA_HEADER)
        writer.writeheader()
        for question_data in data:
            writer.writerow(question_data)
        writer.writerow(new_question)
    return new_id


def write_edited_q(id, edited_question, view=False):
    data = get_all_user_story(DATA_FILE_PATH)
    if view is False:
        edited_question = edited_question.to_dict()
    with open(DATA_FILE_PATH, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=DATA_HEADER)
        writer.writeheader()
        for item in data:
            if item['id'] == id:
                edited_question['id'] = id
                edited_question['submission_time'] = item['submission_time']
                edited_question['vote_number'] = item['vote_number']
                if view is True:
                    edited_question['view_number'] = int(edited_question.get('view_number')) + 1
                    while len(str(edited_question['view_number'])) != 4:
                        edited_question['view_number'] = "0" + str(edited_question['view_number'])
                else:
                    edited_question['view_number'] = item['view_number']
                writer.writerow(edited_question)
            else:
                writer.writerow(item)
    return id


def delete_all_answers(question_id):
    answer_data = get_all_user_story(ANSWER_FILE_PATH)
    with open(ANSWER_FILE_PATH, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=ANSWER_HEADER)
        writer.writeheader()
        for answer in answer_data:
            if answer['question_id'] != question_id:
                writer.writerow(answer)

#  Eniko



