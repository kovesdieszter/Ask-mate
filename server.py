from flask import Flask, render_template, request, redirect, url_for

import data_manager

app = Flask(__name__)


#Eszter


@app.route('/')
def main_page():
    header = data_manager.get_header()
    questions = data_manager.get_data()
    return render_template('list.html', header=header, questions=questions)


# Eszter

#  Bea
#  Bea

#  Dia
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