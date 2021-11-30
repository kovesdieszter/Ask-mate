#  Eszter
from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import datetime
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


@connection.connection_handler
def write_new_answer(cursor, question_id, message, image):
    submission_time = datetime.datetime.now()
    vote_number = 0  # initial vote number

    query = '''
                INSERT INTO answer (submission_time, vote_number, question_id, message, image)
                VALUES (%(s_time)s, %(vt_nr)s, %(q_id)s, %(m_sage)s, %(im_g)s)
                RETURNING *
                '''

    cursor.execute(query, {'s_time': submission_time, 'vt_nr': vote_number, 'q_id': question_id, 'm_sage': message, 'im_g': image})
    return cursor.fetchall()


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

