### Enikő

from psycopg2 import sql
import datetime
from psycopg2.extras import RealDictCursor

import psycopg2
import psycopg2.extras
### Enikő



#  Eszter
import connection


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


@connection.connection_handler
def write_new_question(cursor, new_question):
    dt = datetime.datetime.now()
    submission_time = dt.date()
    query = """
        INSERT INTO question (submission_time, title, message)
        VALUES (%s, %s, %s)
        returning question"""
    cursor.execute(query, (submission_time, new_question['title'], new_question['message'],))
    query = """
        SELECT max(id) 
        FROM question"""
    cursor.execute(query)
    return cursor.fetchone()

def write_edited_q(question_id, edited_question, view=False):
    return connection.write_edited_q(question_id, edited_question, view=view)
#  Eniko

