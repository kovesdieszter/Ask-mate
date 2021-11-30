# Eszter
import csv
import os
import time

####################################
# Creates a decorator to handle the database connection/cursor opening/closing.
# Creates the cursor with RealDictCursor, thus it returns real dictionaries, where the column names are the keys.
import os

import psycopg2
import psycopg2.extras


def get_connection_string():
    # setup connection string
    # to do this, please define these environment variables first
    user_name = os.environ.get('PSQL_USER_NAME')
    password = os.environ.get('PSQL_PASSWORD')
    host = os.environ.get('PSQL_HOST')
    database_name = os.environ.get('PSQL_DB_NAME')

    env_variables_defined = user_name and password and host and database_name

    if env_variables_defined:
        # this string describes all info for psycopg2 to connect to the database
        return 'postgresql://{user_name}:{password}@{host}/{database_name}'.format(
            user_name=user_name,
            password=password,
            host=host,
            database_name=database_name
        )
    else:
        raise KeyError('Some necessary environment variable(s) are not defined')


def open_database():
    try:
        connection_string = get_connection_string()
        connection = psycopg2.connect(connection_string)
        connection.autocommit = True
    except psycopg2.DatabaseError as exception:
        print('Database connection problem')
        raise exception
    return connection


def connection_handler(function):
    def wrapper(*args, **kwargs):
        connection = open_database()
        # we set the cursor_factory parameter to return with a RealDictCursor cursor (cursor which provide dictionaries)
        dict_cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        ret_value = function(dict_cur, *args, **kwargs)
        dict_cur.close()
        connection.close()
        return ret_value

    return wrapper

#####################################



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


def write_new_question(new_question, file_name):
    new_question = new_question.to_dict()
    data = get_all_user_story(DATA_FILE_PATH)
    new_id = str(int(data[-1]['id']) + 1)
    submission_time = str(int(time.time()))
    new_question['id'] = new_id
    new_question['submission_time'] = submission_time
    new_question['view_number'] = '0000'
    new_question['vote_number'] = '000'
    new_question['image'] = file_name
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
#  Eniko



