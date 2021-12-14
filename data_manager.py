
from typing import List, Dict
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import datetime
import connection
import bcrypt


QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']

@connection.connection_handler
def add_new_user(cursor, username, email, password):
    date = get_submission_time()
    query = """
    INSERT INTO 
    users (username, email, password, asked_questions, answers, comments, reputation, date)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(query, (username, email, password, 00, 00, 00, 00, date))
    query = """
                SELECT max(id) 
                FROM question"""
    cursor.execute(query)
    return cursor.fetchone()


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
def add_comment_to_question(cursor, question_id, message, user_id):
    dt = datetime.datetime.now()
    submission_time = f'{dt.date()} {str(dt.time()).split(".")[0]}'
    query = """
    INSERT INTO 
    comment (submission_time, question_id, message, edited_count, user_id)
    VALUES (%(val0)s, %(val1)s, %(val2)s, %(count)s, %(user_id)s)
    RETURNING *
    """
    cursor.execute(query, {'val0': submission_time, 'val1': question_id, 'val2': message, 'count': 0, 'user_id': user_id})
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
def add_comment_to_answer(cursor, question_id, answer_id, message, user_id):
    submission_time = get_submission_time()
    query = """
    INSERT INTO 
    comment (submission_time, question_id, answer_id, message, edited_count, user_id)
    VALUES (%(val0)s, %(val1)s, %(val2)s, %(val3)s, %(count)s, %(user_id)s)
    RETURNING *
    """
    cursor.execute(query, {'count': 0, 'val0': submission_time, 'val1': question_id, 'val2': answer_id, 'val3': message, 'user_id': user_id})
    return cursor.fetchone()


def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'),hashed_bytes_password)


#  Eszter
#  Dia

@connection.connection_handler
def write_new_answer(cursor, question_id, message, image, user_id):
    submission_time = get_submission_time()
    vote_number = 0  # initial vote number

    query = '''
                INSERT INTO answer (submission_time, vote_number, question_id, message, image, user_id)
                VALUES (%(s_time)s, %(vt_nr)s, %(q_id)s, %(m_sage)s, %(im_g)s, %(user_id)s )
                RETURNING *
                '''

    cursor.execute(query, {'s_time': submission_time, 'vt_nr': vote_number, 'q_id': question_id, 'm_sage': message, 'im_g': image, 'user_id':user_id})
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
            SELECT id, name
            FROM tag
            INNER JOIN question_tag
            ON tag.id = question_tag.tag_id
            WHERE question_id = %(q_id)s
            '''
    cursor.execute(query, {'q_id': question_id})
    return cursor.fetchall()


@connection.connection_handler
def delete_tag(cursor, question_id, tag_id):
    query = '''
            DELETE 
            FROM question_tag
            WHERE question_id = %(q_id)s AND tag_id = %(t_id)s
            RETURNING *
            '''
    cursor.execute(query, {'q_id': question_id, 't_id': tag_id})
    return cursor.fetchall()

#  Dia

#  Eniko
@connection.connection_handler
def get_user_id(cursor, username):
    cursor.execute(sql.SQL("""
    SELECT id
    FROM users
    WHERE username = {username}""")
    .format(username=sql.Literal(username)))
    return cursor.fetchone()


@connection.connection_handler
def write_new_question(cursor, new_question, image, user_id):
    submission_time = get_submission_time()
    cursor.execute(sql.SQL("""
        INSERT INTO question (submission_time, view_number, vote_number, title, message, image, user_id)
        VALUES ({time}, {view}, {vote}, {title}, {message}, {image}, {user_id})
        returning question"""
    ).format(time=sql.Literal(submission_time),
             view=sql.Literal(0000),
             vote=sql.Literal(0000),
             title=sql.Literal(new_question['title']),
             message=sql.Literal(new_question['message']),
             image=sql.Literal(image),
             user_id=sql.Literal(user_id)))
    cursor.execute(sql.SQL("""
        SELECT max(id) 
        FROM question"""))

    return cursor.fetchone()


def get_submission_time():
    dt = datetime.datetime.now()
    submission_time = f'{dt.date()} {str(dt.time()).split(".")[0]}'
    return submission_time


@connection.connection_handler
def write_edited_q(cursor, question_id, edited_question, image):
    cursor.execute(sql.SQL("""
        UPDATE question
        SET title = {title}, message = {message}, image = {image}
        WHERE id = {q_id} 
        returning question"""
    ).format(title=sql.Literal(edited_question['title']),
             message=sql.Literal(edited_question['message']),
             image=sql.Literal(image),
             q_id=sql.Literal(question_id)))


@connection.connection_handler
def change_vote_q(cursor, question_id, changer):
    cursor.execute(sql.SQL("""
        UPDATE question
        SET vote_number = vote_number + {changer}
        WHERE id = {q_id}
        returning question"""
    ).format(changer=sql.Literal(changer),
             q_id=sql.Literal(question_id)))


@connection.connection_handler
def change_vote_a(cursor, answer_id, changer):
    cursor.execute(sql.SQL("""
        UPDATE answer
        SET vote_number = vote_number + {changer}
        WHERE id = {a_id}
        returning answer""")
    .format(changer=sql.Literal(changer),
            a_id=sql.Literal(answer_id)))


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
def write_edited_a(cursor, answer_id, edited_answer, image):
    cursor.execute(sql.SQL("""
        UPDATE answer
        SET message = {message}, image= {image}
        WHERE id = {a_id} 
        returning answer"""
    ).format(message=sql.Literal(edited_answer['message']),
             image=sql.Literal(image),
             a_id=sql.Literal(answer_id)))


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
    cursor.execute(sql.SQL("""
        UPDATE comment
        SET message = {message}, submission_time = {time}, edited_count = edited_count + 1
        WHERE id = {c_id} 
        returning comment"""
    ).format(message=sql.Literal(edited_comment['message']),
             time=sql.Literal(submission_time),
             c_id=sql.Literal(comment_id)))


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


@connection.connection_handler
def get_user_name(cursor):
    cursor.execute(sql.SQL("""
    SELECT username
    FROM users"""
    ))
    return cursor.fetchall()


@connection.connection_handler
def get_password(cursor, email):
    cursor.execute(sql.SQL("""
    SELECT password
    FROM users
    WHERE email={email}""")
    .format(email=sql.Literal(email)))
    return cursor.fetchone()


@connection.connection_handler
def write_user_actions(cursor, user_id, action):
    cursor.execute(sql.SQL("""
    UPDATE users
    SET {column} = {column} + 1
    WHERE id = {user_id}
    returning users""")
    .format(column=sql.Identifier(action),
            user_id=sql.Literal(user_id)))
# Enikő
