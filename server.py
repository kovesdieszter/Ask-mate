from flask import Flask, render_template, request, redirect, url_for

from operator import itemgetter
import data_manager

app = Flask(__name__)


#Eszter


@app.route('/')
def main_page():
    header = data_manager.get_header()
    questions = data_manager.get_data("questions")
    return render_template('list.html', header=header, questions=questions)


# Eszter

#  Bea
@app.route('/list', methods=["POST", "GET"])
def sort_list():
    header = data_manager.get_header()
    questions = data_manager.get_data()
    order_by = request.args.get("order_by")
    order_direction = request.args.get("order_direction")
    questions = sorted(questions, key=itemgetter(str(order_by)))
    if order_direction == "descending":
        questions = reversed(questions)
    return render_template('list.html', header=header, questions=questions)
#  Bea

#  Dia
@app.route('/question/<question_id>')
def display_question(question_id):
    questions = data_manager.get_data("questions")
    answers = data_manager.get_data("answers")
    answer_texts = []
    for q in questions:
        if q['id'] == question_id:
            question = q
            break
    for a in answers:
        if a['question_id'] == question_id:
            answer_texts.append(a['message'])

    return render_template('display_question.html', question=question, answer_texts=answer_texts)
#  Dia

#  Eniko
@app.route('/add-question')
def new_question():
    return render_template('add_question_child.html')
#  Eniko

# Eszter
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
# Eszter