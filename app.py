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
    """Show the home page survey start"""
    return render_template("survey_start.html",
                           title=survey.title,
                           instructions=survey.instructions)

@app.post("/begin")
def redirect_to_handle_questions():
    '''directs user to survey questions'''
    current_question = len(responses)

    return redirect(f"/questions/{current_question}")

@app.get("/questions/<int:num_of_question>")
def handle_questions(num_of_question):

    return render_template("question.html",
                           question = survey.questions[num_of_question])

@app.post("/answer")
def handle_answer():
    """Append answer to list and redirect to next question
        If no more questions, redirect to survey completion page

    """
    answer = request.form["answer"]
    responses.append(answer)

    current_question = len(responses)

    if current_question < len(survey.questions):
        return redirect(f"/questions/{current_question}")

    return redirect("/completion")

@app.get("/completion")
def show_completion_page():
    """Show thank you message and survey answers"""

    data = {}
    prompts = [q.prompt for q in survey.questions]
    for prompt in prompts:
        data[prompt]

    return render_template("completion.html")