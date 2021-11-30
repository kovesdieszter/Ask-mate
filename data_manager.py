#  Eszter
import connection
import datetime


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

def write_new_question(new_question, file_name):
    return connection.write_new_question(new_question, file_name)

def write_edited_q(question_id, edited_question, view=False):
    return connection.write_edited_q(question_id, edited_question, view=view)
#  Eniko

