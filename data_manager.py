#  Eszter
import connection

def get_header():
    return connection.DATA_HEADER

def get_data(data):
    if data == "questions":
        return connection.get_all_user_story(connection.DATA_FILE_PATH)
    elif data == "answers":
        return connection.get_all_user_story(connection.ANSWER_FILE_PATH)


#  Eszter


#  Bea
#  Bea

#  Dia
def write_new_answer(new_answer, question_id):
    return connection.write_new_answer(new_answer, question_id)
#  Dia

#  Eniko
def change_vote(question, changer):
    return connection.change_vote(question, changer)

def write_new_question(new_question):
    return connection.write_new_question(new_question)

def write_edited_q(question_id, edited_question):
    return connection.write_edited_q(question_id, edited_question)
#  Eniko

