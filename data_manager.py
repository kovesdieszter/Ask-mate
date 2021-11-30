from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import connection
import sys
#Eszter

@connection.connection_handler
def get_question_header(cursor):
    query = """
    SELECT coloumn_name,*
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = 'question'
    ORDER BY ORDINAL_POSITION
    """
    cursor.execute(query)
    return cursor.fetchone()



@connection.connection_handler
def get_all_user_story(cursor):
    query = """
        SELECT *
        FROM question
        ORDER BY submission_time """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_all_answer(cursor):
    query = """
        SELECT *
        FROM answer
        ORDER BY submission_time """
    cursor.execute(query)


@connection.connection_handler
def delete_question(cursor, question_id):
    query = """
    DELETE *
    FROM question
    WHERE id = %(val)s
    RETURNING *
    """
    cursor.execute(query, {'val': question_id})
    return cursor.fetchall()


@connection.connection_handler
def delete_answer(cursor, answer_id):
    query = """
    DELETE *
    FROM answer
    WHERE id = %(val)s
    RETURNING *
    """
    cursor.execute(query, {'val': answer_id})
    return cursor.fetchall()


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

