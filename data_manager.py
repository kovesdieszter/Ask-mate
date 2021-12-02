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
def get_all_user_story(cursor, order_by='submission_time', direction='ASC', limit=''):
    query = f"""
        SELECT *
        FROM question
        ORDER BY {order_by} {direction}
        {limit}"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_searched_questions(cursor, q):
    query = f"""
            SELECT *
            FROM question
            WHERE UPPER(title) LIKE UPPER({"'%"}{ q }{"%'"}) 
            OR UPPER(message) LIKE UPPER({"'%"}{ q }{"%'"})
            ORDER BY vote_number DESC 
            """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_all_answer(cursor):
    query = """
        SELECT *
        FROM answer
        ORDER BY id """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def delete_question(cursor, question_id):
    query = """
        DELETE 
        FROM answer
        WHERE question_id = %(val)s"""
    cursor.execute(query, {'val': question_id})
    query = """
    DELETE
    FROM question
    WHERE id = %(val)s
    RETURNING *
    """
    cursor.execute(query, {'val': question_id})



@connection.connection_handler
def delete_answer(cursor, answer_id):
    query = """
    DELETE
    FROM answer
    WHERE id = %(val)s
    RETURNING *
    """
    cursor.execute(query, {'val': answer_id})
    return cursor.fetchone()


@connection.connection_handler
def add_comment_to_question(cursor, question_id, message):
    dt = datetime.datetime.now()
    submission_time = f'{dt.date()} {str(dt.time()).split(".")[0]}'
    query = """
    INSERT INTO 
    comment (submission_time, question_id, message, edited_count)
    VALUES (%(val0)s, %(val1)s, %(val2)s, %(count)s)
    RETURNING *
    """
    cursor.execute(query, {'val0': submission_time, 'val1': question_id, 'val2': message, 'count': 0})
    return cursor.fetchone()


@connection.connection_handler
def get_comment_by_question_id(cursor, question_id):
    query = """
        SELECT *
        FROM comment
        WHERE question_id = %(val1)s
        ORDER BY id """
    cursor.execute(query, {'val1': question_id})
    return cursor.fetchall()

@connection.connection_handler
def add_comment_to_answer(cursor, question_id, answer_id, message):
    dt = datetime.datetime.now()
    submission_time = f'{dt.date()} {str(dt.time()).split(".")[0]}'
    query = """
    INSERT INTO 
    comment (submission_time, question_id, answer_id, message)
    VALUES (%(val0)s, %(val1)s, %(val2)s, %(val3)s)
    RETURNING *
    """
    cursor.execute(query, {'val0': submission_time, 'val1': question_id, 'val2': answer_id, 'val3': message})
    return cursor.fetchone()


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


@connection.connection_handler
def get_all_tag_names(cursor):
    query = '''
            SELECT name
            FROM tag
            '''
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def update_tag_table(cursor, tag_name):
    query = '''
            INSERT INTO tag (name)
            VALUES (%(tag_n)s)
            ON CONFLICT DO NOTHING
            RETURNING *
            '''
    try:
        cursor.execute(query, {'tag_n': tag_name})
    finally:
        return cursor.fetchall()


@connection.connection_handler
def get_tag_id(cursor, tag_name):
    query = '''
        SELECT id
        FROM tag
        WHERE name = %(t_name)s
            '''
    cursor.execute(query, {'t_name': tag_name})
    return cursor.fetchall()


@connection.connection_handler
def update_question_tag_table(cursor, question_id, tag_id):
    query = '''
            INSERT INTO question_tag
            VALUES (%(q_id)s, %(t_id)s)
            ON CONFLICT
            DO NOTHING 
            RETURNING *
            '''
    try:
        cursor.execute(query, {'q_id': question_id, 't_id': tag_id})
    finally:
        return cursor.fetchall()


@connection.connection_handler
def get_question_tags(cursor, question_id):
    query = '''
            SELECT name
            FROM tag
            INNER JOIN question_tag
            ON tag.id = question_tag.tag_id
            WHERE question_id = %(q_id)s
            '''
    cursor.execute(query, {'q_id': question_id})
    return cursor.fetchall()


#  Dia

#  Eniko



@connection.connection_handler
def write_new_question(cursor, new_question, image):
    image = str(image).split("'")[1]
    submission_time = get_submission_time()
    query = """
        INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
        VALUES (%s, %s, %s, %s, %s, %s)
        returning question"""
    cursor.execute(query, (submission_time, 0000, 0000, new_question['title'], new_question['message'], image))
    query = """
        SELECT max(id) 
        FROM question"""
    cursor.execute(query)
    return cursor.fetchone()


def get_submission_time():
    dt = datetime.datetime.now()
    submission_time = f'{dt.date()} {str(dt.time()).split(".")[0]}'
    return submission_time


@connection.connection_handler
def write_edited_q(cursor, question_id, edited_question, image):
    image = str(image).split("'")[1]
    query = """
        UPDATE question
        SET title = %s, message = %s, image = %s
        WHERE id = %s 
        returning question"""
    cursor.execute(query, (edited_question['title'], edited_question['message'], image, question_id),)
# def write_edited_q(question_id, edited_question, view=False):
#     return connection.write_edited_q(question_id, edited_question, view=view)



@connection.connection_handler
def change_vote_q(cursor, question_id, changer):
    query = """
        UPDATE question
        SET vote_number = vote_number + %s
        WHERE id = %s
        returning question"""
    cursor.execute(query, (changer, question_id,))


@connection.connection_handler
def change_vote_a(cursor, answer_id, changer):
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
        WHERE id = %s
        ORDER BY id"""
    cursor.execute(query, (question_id,))
    return cursor.fetchone()


@connection.connection_handler
def get_answer_by_question_id(cursor, question_id):
    query = """
        SELECT *
        FROM answer
        WHERE question_id = %s
        ORDER BY id"""
    cursor.execute(query, (question_id,))
    return cursor.fetchall()


@connection.connection_handler
def get_question_id_by_answer(cursor, answer_id):
    query = """
        SELECT question_id
        FROM answer
        WHERE id = %s"""
    cursor.execute(query, (answer_id,))
    return cursor.fetchone()


@connection.connection_handler
def get_answer_data_by_id(cursor, answer_id):
    query = """
        SELECT * 
        FROM answer
        WHERE id = %s"""
    cursor.execute(query, (answer_id,))
    return cursor.fetchone()


@connection.connection_handler
def write_edited_a(cursor, answer_id, edited_answer):
    query = """
        UPDATE answer
        SET message = %s
        WHERE id = %s 
        returning answer"""
    cursor.execute(query, (edited_answer['message'], answer_id,))

@connection.connection_handler
def get_question_id_by_comment(cursor, comment_id):
    query = """
        SELECT question_id
        FROM comment
        WHERE id = %s"""
    cursor.execute(query, (comment_id,))
    return cursor.fetchone()


@connection.connection_handler
def delete_comment(cursor, comment_id):
    query = """
        DELETE 
        FROM comment
        WHERE id = %s
        returning comment"""
    cursor.execute(query, (comment_id,))


@connection.connection_handler
def write_edited_com(cursor, comment_id, edited_comment):
    submission_time = get_submission_time()
    query = """
        UPDATE comment
        SET message = %s, submission_time = %s, edited_count = edited_count + 1
        WHERE id = %s 
        returning comment"""
    cursor.execute(query, (edited_comment['message'], submission_time, comment_id,))


@connection.connection_handler
def get_comment_data_by_id(cursor, comment_id):
    query = """
        SELECT * 
        FROM comment
        WHERE id = %s"""
    cursor.execute(query, (comment_id,))
    return cursor.fetchone()


@connection.connection_handler
def increase_view(cursor, question_id):
    query = """
        UPDATE question
        SET view_number = view_number + 1
        WHERE id = %s
        returning question"""
    cursor.execute(query, (question_id,))
# Enikő
