from flask import Flask, render_template, request, redirect, url_for

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
@app.route('/question/<question_id>/vote_up')
def vote_up(question_id):
    questions = data_manager.get_data('questions')
    for q in questions:
        if q['id'] == question_id:
            question = q
            data_manager.change_vote(question, 1)
    return redirect('/')


@app.route('/question/<question_id>/vote_down')
def vote_down(question_id):
    questions = data_manager.get_data('questions')
    for q in questions:
        if q['id'] == question_id:
            question = q
            data_manager.change_vote(question, -1)
    return redirect('/')


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method == 'POST':
        edited_question_id = data_manager.write_edited_q(question_id, request.form)
        return redirect(url_for('display_question', question_id=edited_question_id))
    questions = data_manager.get_data('questions')
    for q in questions:
        if q['id'] == question_id:
            question = q
    return render_template('edit_child.html', question=question)


@app.route('/add-question', methods=['GET', 'POST'])
def new_question():
    if request.method == 'POST':
        question_id = data_manager.write_new_question(request.form)
        return redirect(url_for('display_question', question_id=question_id))
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