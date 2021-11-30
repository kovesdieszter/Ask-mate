from flask import Flask, render_template, request, redirect, url_for

from operator import itemgetter
import data_manager
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "./static"


#Eszter


@app.route('/')
def main_page():
   # header = data_manager.get_header()
    questions = data_manager.get_all_user_story()
    return render_template('list.html', questions=questions)


# Eszter

#  Bea
@app.route('/list', methods=["POST", "GET"])
def sort_list():
    header = data_manager.get_header()
    questions = data_manager.get_data("questions")
    order_by = request.args.get("order_by")
    order_direction = request.args.get("order_direction")
    questions = sorted(questions, key=itemgetter(str(order_by)))
    if order_direction == "descending":
        questions = reversed(questions)
    return render_template('list.html', header=header, questions=questions)
#  Bea

#  Dia
@app.route('/question/<question_id>')
def display_question(question_id, view=True):
    questions = data_manager.get_all_user_story()
   # answers = data_manager.get_data("answers")
    answer_texts = []
    question = None
    if request.args.get('view') == 'False':
        view_counter = request.args.get('view')
    else:
        view_counter = view
    for q in questions:
        if q['id'] == question_id:
            question = q
            data_manager.write_edited_q(question_id, question, view_counter)
            break
    for a in answers:
        if a['question_id'] == question_id:
            answer_texts.append(a['message'])

    return render_template('display_question.html', question=question, answer_texts=answer_texts, answers=answers)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def post_answer(question_id):
    questions = data_manager.get_all_user_story()
    for q in questions:
        if q['id'] == int(question_id):
            question_title = q['title']
            break
    if request.method == 'POST':
        image = request.args.get('image')
        message = request.args.get('message')
        data_manager.write_new_answer(question_id, message, image)
        return redirect(url_for('display_question', question_id=question_id))
    return render_template('post_answer.html', question_title=question_title)


@app.route('/answer/<answer_id>/vote_up')
def vote_answer_up(answer_id):
    answers = data_manager.get_data('answers')
    for a in answers:
        if a['id'] == answer_id:
            answer = a
            data_manager.change_vote(answer, 1, "answers")
    return redirect(url_for("display_question", question_id=answer['question_id']))


@app.route('/answer/<answer_id>/vote_down')
def vote_answer_down(answer_id):
    answers = data_manager.get_data('answers')
    for a in answers:
        if a['id'] == answer_id:
            answer = a
            data_manager.change_vote(answer, -1, "answers")
    return redirect(url_for("display_question", question_id=answer['question_id']))


#  Dia

#  Eniko
@app.route('/question/<question_id>/vote_up')
def vote_up(question_id):
    questions = data_manager.get_data('questions')
    for q in questions:
        if q['id'] == question_id:
            question = q
            data_manager.change_vote(question, 1, "questions")
    return redirect('/')


@app.route('/question/<question_id>/vote_down')
def vote_down(question_id):
    questions = data_manager.get_data('questions')
    for q in questions:
        if q['id'] == question_id:
            question = q
            data_manager.change_vote(question, -1, "questions")
    return redirect('/')


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method == 'POST':
        edited_question_id = data_manager.write_edited_q(question_id, request.form)
        return redirect(url_for('display_question', question_id=edited_question_id, view=False))
    questions = data_manager.get_data('questions')
    for q in questions:
        if q['id'] == question_id:
            question = q
    return render_template('edit_child.html', question=question)


@app.route('/add-question', methods=['GET', 'POST'])
def new_question():
    if request.method == 'POST':
        """file = request.files['image']
        name = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], name))"""
        question_id = data_manager.write_new_question(request.form)
        return redirect(url_for('display_question', question_id=question_id))
    return render_template('add_question_child.html')
#  Eniko

# Eszter


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    data_manager.delete_question(question_id)
    return redirect(url_for("main_page"))


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    deleted_id = data_manager.delete_answer(answer_id)
    return redirect(url_for("display_question", question_id=deleted_id))


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
# Eszter