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
    header = data_manager.QUESTION_HEADER
    questions = data_manager.get_all_user_story("submission_time", "DESC", "LIMIT 5")
    return render_template('main.html', header=header, questions=questions)


# Eszter

#  Bea
@app.route('/list', methods=["POST", "GET"])
def sort_list():
    order_direction = request.args.get("order_direction")
    order_by = request.args.get("order_by")
    header = data_manager.QUESTION_HEADER
    if order_direction and order_by:
        questions = data_manager.get_all_user_story(order_by, order_direction)
    else:
        questions = data_manager.get_all_user_story("submission_time", "DESC")
    return render_template('list.html', header=header, questions=questions)


@app.route('/search', methods=["POST", "GET"])
def question():
    header = data_manager.QUESTION_HEADER
    q = request.args.get("q")
    questions = data_manager.get_searched_questions(q)
    return render_template('main.html', header=header, questions=questions)

#  Bea

#  Dia
@app.route('/question/<question_id>')
def display_question(question_id):
    question = data_manager.get_question_data_by_id(question_id)
    answers = data_manager.get_answer_by_question_id(question_id)
    tags = data_manager.get_question_tags(question_id)
    comments = data_manager.get_comment_by_question_id(question_id)
    return render_template('display_question.html', question=question, answers=answers, comments=comments, tags=tags)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def post_answer(question_id):
    questions = data_manager.get_all_user_story()
    for q in questions:
        if q['id'] == int(question_id):
            question_title = q['title']
            break
    if request.method == 'POST':
        image = request.form.get('image')
        message = request.form.get('message')
        data_manager.write_new_answer(question_id, message, image)
        return redirect(url_for('display_question', question_id=question_id))
    return render_template('post_answer.html', question_title=question_title)


@app.route('/question/<question_id>/new-tag', methods=['GET', 'POST'])
def add_tag(question_id):
    if request.method == 'POST':
        tag_names = list(request.form.listvalues())
        tags = sum(tag_names, [])
        print(tags)
        # tag_ids = data_manager.get_tag_id(tag_names)
        for tag in tags:
            data_manager.update_tag_table(tag)
        # data_manager.update_question_tag_table(question_id, tag_ids)
        return redirect(url_for('display_question', question_id=question_id))
    return render_template('add_tag.html')


@app.route('/answer/<answer_id>/vote_up')
def vote_answer_up(answer_id):
    data_manager.change_vote_a(answer_id, 1)
    question_id = data_manager.get_question_id_by_answer(answer_id)
    return redirect(url_for("display_question", question_id=question_id['question_id']))


@app.route('/answer/<answer_id>/vote_down')
def vote_answer_down(answer_id):
    data_manager.change_vote_a(answer_id, -1)
    question_id = data_manager.get_question_id_by_answer(answer_id)
    return redirect(url_for("display_question", question_id=question_id['question_id']))


#  Dia

#  Eniko
@app.route('/question/<question_id>/vote_up')
def vote_up(question_id):
    data_manager.change_vote_q(question_id, 1)
    return redirect('/')


@app.route('/question/<question_id>/vote_down')
def vote_down(question_id):
    data_manager.change_vote_q(question_id, -1)
    return redirect('/')


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method == 'POST':
        data_manager.write_edited_q(question_id, request.form)
        return redirect(url_for('display_question', question_id=question_id))
    question = data_manager.get_question_data_by_id(question_id)
    return render_template('edit_child.html', question=question)


@app.route('/add-question', methods=['GET', 'POST'])
def new_question():
    if request.method == 'POST':
        """file = request.files['image']
        name = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], name))"""
        question_id = data_manager.write_new_question(request.form)['max']
        return redirect(url_for('display_question', question_id=question_id))
    return render_template('add_question_child.html')


@app.route('/answer/<answer_id>', methods=['GET', 'POST'])
def edit_answer(answer_id):
    if request.method == 'POST':
        data_manager.write_edited_a(answer_id, request.form)
        question_id = data_manager.get_question_id_by_answer(answer_id)
        return redirect(url_for('display_question', question_id=question_id['question_id']))
    answer = data_manager.get_answer_data_by_id(answer_id)
    return render_template('edit_answer.html', answer=answer)
#  Eniko

# Eszter


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    data_manager.delete_question(question_id)
    return redirect(url_for("main_page"))


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    deleted_answer = data_manager.delete_answer(answer_id)
    return redirect(url_for("display_question", question_id=deleted_answer['question_id']))


@app.route('/question/<question_id>/new-comment', methods=["GET", "POST"])
def add_question_comment(question_id):
    if request.method == "POST":
        comment = data_manager.add_comment_to_question(question_id, request.form['message'])
        return redirect(url_for("display_question", question_id=question_id, comment=comment))
    question = data_manager.get_question_data_by_id(question_id)
    return render_template('comment_child.html', question=question)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
# Eszter