from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cowboys'
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 





@app.route('/')
def create_home_page():
    title = survey.title
    instructions = survey.instructions
    session['started-survey'] = False 

    return render_template('home.html', title = title, instructions = instructions)

@app.route('/start-survey', methods = ['POST'])
def start_survey():
    session['responses'] = []
    session['started-survey'] = True 


    return redirect("/question/0")

@app.route('/question/<int:num>')
def get_question(num):
    
    answers = session['responses'] 
    started_survey = session['started-survey']

    if started_survey is False:
        flash("Please start survey from the beginning")
        return redirect('/')
    if num > len(survey.questions):
        flash("This question does not exist. Please take survey in order")
        return redirect(f'/question/{len(answers)}')
    if len(answers) != num:
        flash("You attempted to answer a question out of order, please take survey in order")
        return redirect(f'/question/{len(answers)}')
    if len(answers) == len(survey.questions):
        flash("You have completed the survey, however you may your start survey over")
        return redirect("/complete")
    
    question = survey.questions[num]

    return render_template('questions.html', question = question.question, choices = question.choices, num = num )

@app.route('/answer', methods=["POST"])
def handle_answer():
    answer = request.form['answer']
    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses 


    if len(responses) == len(survey.questions):
        return redirect("/complete")
    else:
        return redirect(f"question/{len(responses)}")

@app.route('/complete')
def complete_page():

    responses = session['responses']

    # session['started_survey'] = False

    return render_template('complete.html', responses = responses)
