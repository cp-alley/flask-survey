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
    return render_template("question.html",
                           question = survey.questions[num_of_question]) #pull this out into a variable

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

    if current_question < len(survey.questions):
        return redirect(f"/questions/{current_question}")

    return redirect("/completion")

@app.get("/completion")
def show_completion_page():
    """Show thank you message and survey answers"""

    prompts = [q.prompt for q in survey.questions]
    data = {prompts[i]: responses[i] for i in range(len(responses))}

    return render_template("completion.html", responses = data)