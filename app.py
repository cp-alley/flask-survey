from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.get("/")
def show_homepage():
    return render_template("survey_start.html",
                           title=survey.title,
                           instructions=survey.instructions)

@app.post("/begin")
def redirect_to_handle_questions():
    '''directs user to survey questions'''

    return redirect("/questions/<int:num_of_question>")

@app.get("/questions/<int:num_of_question>")
def handle_questions(num_of_question):

    return render_template("question.html",
                           question = survey.questions[num_of_question])