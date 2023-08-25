from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.get("/")
def show_homepage():
    """Show the home page survey start"""
    session["responses"] = []
    session["questions_answered"] = []
    return render_template("survey_start.html",
                           title=survey.title,
                           instructions=survey.instructions)

@app.post("/begin")
def redirect_to_handle_questions():
    '''directs user to survey questions'''

    return redirect("/questions/0")

@app.get("/questions/<int:num_of_question>")
def handle_questions(num_of_question):
    '''Shows current question'''
    questions_answered = session["questions_answered"]

    if num_of_question in questions_answered:
        print("num_of_question=", num_of_question, "current_quest", questions_answered)
        return redirect(f"/questions/{len(questions_answered)}")

    if num_of_question not in questions_answered:

        if num_of_question != len(questions_answered):
            return redirect(f"/questions/{len(questions_answered)}")

    question = survey.questions[num_of_question]

    return render_template("question.html", question = question)

@app.post("/answer")
def handle_answer():
    """Append answer to list and redirect to next question
        If no more questions, redirect to survey completion page

    """
    answer = request.form["answer"]

    responses = session["responses"]
    responses.append(answer)
    session["responses"] = responses

    current_question = len(responses)

    questions_answered = session["questions_answered"]
    questions_answered.append(current_question - 1)
    session["questions_answered"] = questions_answered

    if current_question < len(survey.questions):
        return redirect(f"/questions/{current_question}")

    return redirect("/completion")

@app.get("/completion")
def show_completion_page():
    """Show thank you message and survey answers"""

    responses = session["responses"]
    prompts = [q.prompt for q in survey.questions]

    return render_template("completion.html", responses = responses, prompts = prompts)