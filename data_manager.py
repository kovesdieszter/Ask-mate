from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import connection
#Eszter


@connection.connection_handler
def get_all_user_story(cursor):
    query = """
        SELECT *
        FROM question
        ORDER BY submission_time """
    cursor.execute(query)
    return cursor.fetchall()


def delete_q(cursor, id):
    data = get_all_user_story(DATA_FILE_PATH)
    with open(DATA_FILE_PATH, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=DATA_HEADER)
        writer.writeheader()
        for item in data:
            if item['id'] != id:
                writer.writerow(item)


def delete_a(id):
    print(id)
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




def get_header():
    return connection.DATA_HEADER


def get_data(data):
    if data == "questions":
        return connection.get_all_user_story(connection.DATA_FILE_PATH)
    elif data == "answers":
        return connection.get_all_user_story(connection.ANSWER_FILE_PATH)


def delete_question(question_id):
    return connection.delete_q(question_id)


def delete_answer(answer_id):
    return connection.delete_a(answer_id)
#  Eszter


#  Bea
#  Bea

#  Dia
def write_new_answer(new_answer, question_id):
    return connection.write_new_answer(new_answer, question_id)
#  Dia

#  Eniko
def change_vote(question, changer, datatype):
    if datatype == "questions":
        return connection.change_vote(question, changer, connection.DATA_FILE_PATH)
    elif datatype == "answers":
        return connection.change_vote(question, changer, connection.ANSWER_FILE_PATH)

def write_new_question(new_question, file_name):
    return connection.write_new_question(new_question, file_name)

def write_edited_q(question_id, edited_question, view=False):
    return connection.write_edited_q(question_id, edited_question, view=view)
#  Eniko

