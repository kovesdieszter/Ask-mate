#  Eszter
from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import datetime
import connection
import sys
#Eszter


QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


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
    return cursor.fetchall()


@connection.connection_handler
def delete_question(cursor, question_id):
    query = """
    DELETE
    FROM question
    WHERE id = %(val)s
    RETURNING *
    """
    cursor.execute(query, {'val': question_id})
    return cursor.fetchall()


@connection.connection_handler
def delete_answer(cursor, answer_id):
    query = """
    DELETE
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

@connection.connection_handler
def write_new_answer(cursor, question_id, message, image):
    dt = datetime.datetime.now()
    submission_time = dt.date()
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



@connection.connection_handler
def write_new_question(cursor, new_question):
    dt = datetime.datetime.now()
    submission_time = f'{dt.date()} {str(dt.time()).split(".")[0]}'
    query = """
        INSERT INTO question (submission_time, view_number, vote_number, title, message)
        VALUES (%s, %s, %s, %s, %s)
        returning question"""
    cursor.execute(query, (submission_time, 0000, 0000, new_question['title'], new_question['message'],))
    query = """
        SELECT max(id) 
        FROM question"""
    cursor.execute(query)
    return cursor.fetchone()


@connection.connection_handler
def write_edited_q(cursor, question_id, edited_question):
    query = """
        UPDATE question
        SET title = %s, message = %s
        WHERE id = %s 
        returning question"""
    cursor.execute(query, (edited_question['title'], edited_question['message'], question_id),)
# def write_edited_q(question_id, edited_question, view=False):
#     return connection.write_edited_q(question_id, edited_question, view=view)
#  Eniko

@connection.connection_handler
def change_vote(cursor, question_id, changer):
    query = """
        UPDATE question
        SET vote_number = vote_number + %s
        WHERE id = %s
        returning question"""
    cursor.execute(query, (changer, question_id,))

@connection.connection_handler
def change_vote(cursor, answer_id, changer):
    query = """
        UPDATE answer
        SET vote_number = vote_number + %s
        WHERE id = %s
        returning answer"""
    cursor.execute(query, (changer, answer_id,))


@connection.connection_handler
def get_question_data_by_id(cursor, question_id):
    query = """
        SELECT *
        FROM question
        WHERE id = %s"""
    cursor.execute(query, (question_id,))
    return cursor.fetchone()


@connection.connection_handler
def get_answer_by_question_id(cursor, question_id):
    query = """
        SELECT *
        FROM answer
        WHERE question_id = %s"""
    cursor.execute(query, question_id)
    return cursor.fetchall()
