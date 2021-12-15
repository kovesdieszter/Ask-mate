from flask import Flask, render_template, request, redirect, url_for, session
from bonus_questions import SAMPLE_QUESTIONS
from operator import itemgetter
import data_manager
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.secret_key = b'_fkm_%asdd=54?.12"<dkhifa-w\n\xec]/'

#Eszter


@app.route('/user/<user_id>')
def user_page(user_id):
    user = data_manager.get_user_by_('id', user_id)
    return render_template('user.html', user=user)


@app.route("/bonus-questions")
def main():
    return render_template('bonus_questions.html', questions=SAMPLE_QUESTIONS)


@app.route('/')
def main_page():
    header = data_manager.QUESTION_HEADER
    questions = data_manager.get_all_user_story("submission_time", "DESC", "LIMIT 5")
    if 'username' in session:
        user_id = data_manager.get_user_by_('username', session['username'])['id']
        return render_template('main.html', header=header, questions=questions, id=user_id)
    return render_template('main.html', header=header, questions=questions)


@app.route('/registration', methods=["GET", "POST"])
def register_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = data_manager.hash_password(request.form['password'])
        data_manager.add_new_user(username, email, password)
        return redirect(url_for('main_page', username=username,email=email, password=password))
    return render_template('registration.html')


@app.route('/users', methods=["GET", "POST"])
def list_users():
    if 'username' in session:
        table_data = data_manager.get_users()
        return render_template('users.html', data=table_data)
    return "You are not logged in, please login!"

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
    if request.args.get('view') == 'True':
        data_manager.increase_view(question_id)
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
        file = request.files['image']
        if file.filename != '':
            filename = secure_filename(file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(image_path)
        else:
            filename = None
        message = request.form.get('message')
        user_id = data_manager.get_user_id(session['username'])['id']
        data_manager.write_new_answer(question_id, message, filename, user_id)
        data_manager.write_user_actions(user_id, 'answers')
        return redirect(url_for('display_question', question_id=question_id))
    return render_template('post_answer.html', question_title=question_title)


@app.route('/question/<question_id>/new-tag', methods=['GET', 'POST'])
def add_tag(question_id):
    all_tag_names = data_manager.get_all_tag_names()
    if request.method == 'POST':
        tag_names = list(request.form.listvalues())
        tags = sum(tag_names, [])
        tag_ids = []
        for tag in tags:
            if tag != '':
                data_manager.update_tag_table(tag)
                tag_id_rdict = data_manager.get_tag_id(tag)
                for tag_id in tag_id_rdict:
                    tag_ids.append(tag_id['id'])
        for t_id in tag_ids:
            data_manager.update_question_tag_table(question_id, t_id)
        return redirect(url_for('display_question', question_id=question_id))
    return render_template('add_tag.html', all_tag_names=all_tag_names)


@app.route('/question/<question_id>/tag/<tag_id>/delete')
def delete_tag(question_id, tag_id):
    data_manager.delete_tag(question_id, tag_id)
    return redirect(url_for('display_question', question_id=question_id))


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
    if request.args.get('to') == 'list':
        return redirect('/list')
    return redirect('/')


@app.route('/question/<question_id>/vote_down')
def vote_down(question_id):
    data_manager.change_vote_q(question_id, -1)
    if request.args.get('to') == 'list':
        return redirect('/list')
    return redirect('/')


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method == 'POST':
        file = request.files['image']
        if file.filename != '':
            filename = secure_filename(file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(image_path)
        else:
            filename = None
        data_manager.write_edited_q(question_id, request.form, filename)
        return redirect(url_for('display_question', question_id=question_id))
    question = data_manager.get_question_data_by_id(question_id)
    return render_template('edit_child.html', question=question)


@app.route('/add-question', methods=['GET', 'POST'])
def new_question():
    if request.method == 'POST':
        file = request.files['image']
        if file.filename != '':
            filename = secure_filename(file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(image_path)
        else:
            filename = None
        user_id = data_manager.get_user_id(session['username'])['id']
        question_id = data_manager.write_new_question(request.form, filename, user_id)['max']
        data_manager.write_user_actions(user_id, 'asked_questions')
        return redirect(url_for('display_question', question_id=question_id))
    return render_template('add_question_child.html')


@app.route('/answer/<answer_id>', methods=['GET', 'POST'])
def edit_answer(answer_id):
    if request.method == 'POST':
        file = request.files['image']
        if file.filename != '':
            filename = secure_filename(file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(image_path)
        else:
            filename = None
        data_manager.write_edited_a(answer_id, request.form, filename)
        question_id = data_manager.get_question_id_by_answer(answer_id)
        return redirect(url_for('display_question', question_id=question_id['question_id']))
    answer = data_manager.get_answer_data_by_id(answer_id)
    return render_template('edit_answer.html', answer=answer)


@app.route('/comments/<comment_id>')
def delete_comment(comment_id):
    question_id = data_manager.get_question_id_by_comment(comment_id)
    data_manager.delete_comment(comment_id)
    return redirect(url_for('display_question', question_id=question_id['question_id']))


@app.route('/comment/<comment_id>', methods=['GET', 'POST'])
def edit_comment(comment_id):
    if request.method == 'POST':
        data_manager.write_edited_com(comment_id, request.form)
        question_id = data_manager.get_question_id_by_comment(comment_id)
        return redirect(url_for('display_question', question_id=question_id['question_id']))
    comment = data_manager.get_comment_data_by_id(comment_id)
    return render_template('edit_comment.html', comment=comment)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_names = data_manager.get_user_name()
        for username in user_names:
            if request.form['user_name'] in username['username']:
                if data_manager.verify_password(request.form['password'], data_manager.get_password(request.form['email'])['password']):
                    session['username'] = request.form['user_name']
                    return redirect(url_for('main_page'))
                else:
                    return render_template('login.html', message='Invalid login attempt')
        return render_template('login.html', message='Invalid login attempt')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main_page'))
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
        user_id = data_manager.get_user_id(session['username'])['id']
        comment = data_manager.add_comment_to_question(question_id, request.form['message'], user_id)
        data_manager.write_user_actions(user_id, 'comments')
        return redirect(url_for("display_question", question_id=question_id, comment=comment))
    question = data_manager.get_question_data_by_id(question_id)
    return render_template('comment_child.html', question=question)


@app.route('/answer/<answer_id>/new-comment', methods=["GET", "POST"])
def add_answer_comment(answer_id):
    question_id = data_manager.get_question_id_by_answer(answer_id)
    question_id = question_id['question_id']
    if request.method == "POST":
        user_id = data_manager.get_user_id(session['username'])['id']
        comment = data_manager.add_comment_to_answer(question_id, answer_id, request.form.get('message'), user_id)
        data_manager.write_user_actions(user_id, 'comments')
        return redirect(url_for("display_question", question_id=question_id, answer_id=answer_id, comment=comment))
    answer = data_manager.get_answer_data_by_id(answer_id)
    return render_template('ans_comment_child.html', answer=answer)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
# Eszter