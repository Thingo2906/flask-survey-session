from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey 

# key names will use to store some things in the session;
# put here as constants so we're guaranteed to be consistent in
# our spelling of these
responses = []

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route("/")
def show_survey_start():
    """Select a survey."""
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template("home_page.html", title = title, instructions = instructions )


@app.route("/start", methods=["POST"])
def start_survey():
    """Clear the session of responses."""

    session["responses"] = []

    return redirect("/questions/0")


@app.route("/answer", methods=["POST"])
def handle_question():
    """Save response and redirect to next question."""

    # get the response choice
    choice = request.form['answer']

    # add this response to the session
    responses = session["responses"]
    responses.append(choice)
    session["responses"] = responses

    if (len(responses) == len(satisfaction_survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/questions/<int:id>")
def show_question(id):
    """Display current question."""
    responses = session.get("responses")

    if (responses is None):
        # trying to access question page too soon
        return redirect("/")

    if (len(responses) == len(satisfaction_survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    if (len(responses) != id):
        # Trying to access questions out of order.
        flash("Invalid question id")
        return redirect(f"/questions/{len(responses)}")
    question = satisfaction_survey.questions[id]
    return render_template("question.html", question_num=id, question=question)


@app.route("/complete")
def complete():
    """Survey complete. Show completion page."""

    return render_template("complete.html")
