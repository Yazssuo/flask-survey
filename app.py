from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

theSurvey = surveys["satisfaction"]

app = Flask(__name__)
app.config['SECRET_KEY'] = "this-is-a-key"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    return render_template('home.html', title=theSurvey.title, instrucs=theSurvey.instructions)

@app.route('/answer', methods=["POST"])
def answer_func():
    responses = session["responses"]
    response = request.form.get("response")
    responses.append(response)
    session["responses"] = responses
    return redirect(f'/{len(responses)}')

@app.route('/start', methods=["POST"])
def start_survey():
    session["responses"] = []
    return redirect('/0')

@app.route('/<int:questionNumb>')
def question_page(questionNumb):
    responses = session["responses"]
    if len(responses) == len(theSurvey.questions):
        return render_template('thank.html')
    if len(responses) != questionNumb:
        flash("You're trying to access an invalid question as part of your redirect.")
        return redirect(f"/{len(responses)}")
    target = theSurvey.questions[questionNumb]
    return render_template('question.html', question=target.question, choices=target.choices, allowtext=target.allow_text)
