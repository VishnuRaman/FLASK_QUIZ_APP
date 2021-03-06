from flask import Flask, render_template, url_for, request, session, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, user_logged_in

# pickle module implements binary protocols for serializing and de-serializing a Pytohn object structure.
# "Pickling" is the process whereby an object hierarchy is converted into byte stream, and
# "unpickling" is the inverse
# "loads" reads a pickled object hierarchy from a bytes object and return the reconstituted object hierarchy specified
# therein.
# "dumps" return pickled representation of the object as a bytes object, instead of writing it to a file.
from pickle import loads, dumps
import json
from forms import LoginForm, RegisterForm, QuestionForm, QuizForm

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)


#importing models after app is created
from models import *

#creating instance of LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

#configuring login_manager instance
login_manager.login_view = 'login'
login_manager.login_message = 'Please login to have access to this page.'

@login_manager.user_loader
def load_user(userid):
    return User.query.filter(User.id==int(userid)).first()

def getScoreboard():
    users = User.query.order_by(User.score.desc())
    return users

@app.route('/')
def home():
    return render_template('index.html', users=getScoreboard())

@app.route('/login', methods=['GET', 'POST'])
def login():
    logout_user()
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=request.form['username']).first()
            if user is not None and bcrypt.check_password_hash(user.password, request.form['password']):
                login_user(user)
                flash('You have logged in.')
                return redirect(url_for('home'))
            else:
                error = 'Invalid credentials, try again.'
        else :
            error = 'Invalid credentials, try again.'
            render_template('login.html', form=form, error=error)
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(name=form.name.data,username=form.username.data,password=form.password.data,score=0)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('You been registered and logged in')
            return redirect(url_for('home'))
    logout_user()
    flash('You have been logged out')
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('login'))

@app.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    form = QuestionForm()
    if form.validate_on_submit():
        questiondata = Questions(question=form.question.data,option1=form.option1.data,option2=form.option2.data,
                                 option3=form.option3.data,option4=form.option4.data,answer=form.answer.data,
                                 creatorid=current_user.id,category=form.topic.data,difficulty=form.difficulty.data)
        db.session.add(questiondata)
        db.session.commit()
        flash('Your question has been nestled deep within the Flask Quiz App')
        return render_template('submit.html', form=form, users=getScoreboard())
    return render_template('submit.html', form=form, users=getScoreboard())


@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    form = QuizForm()
    if current_user.answered is None:
        current_user.answered = dumps([])
        db.session.commit()
        questions_to_display = Questions.query.filter(Questions.creatorid != str(current_user.id)).all()
        return render_template('quiz.html', questions_to_display=questions_to_display, form=form, users=getScoreboard())

    else:
        alreadyAns = loads(current_user.answered)
        # Check the questions to display
        questions_to_display = Questions.query.filter(Questions.creatorid != str(current_user.id)).filter(
            ~Questions.questionid.in_(alreadyAns)).all()
        return render_template('quiz.html', questions_to_display=questions_to_display, form=form, users=getScoreboard())


@app.route('/answer')
def fetch_answer():
    # id is the question id and userid is the User id
    # Storing the data from the request
    id = request.args.get('id', 0, type=int)
    value = request.args.get('value', 0, type=str)
    userId = request.args.get('userid', 0, type=int)

    # Fetching question and student data
    attempted_question = Questions.query.filter(Questions.questionid == id).all()
    presentUser = User.query.get(userId)
    presentScore = presentUser.score

    # Appropriately changing the student's score
    if attempted_question[0].answer == value:
        if attempted_question[0].difficulty == 'easy':
            presentScore = presentScore + 1
        elif attempted_question[0].difficulty == 'moderate':
            presentScore = presentScore + 2
        elif attempted_question[0].difficulty == 'hard':
            presentScore = presentScore + 3
        elif attempted_question[0].difficulty == 'insane':
            presentScore = presentScore + 4

        presentUser.score = presentScore
        correct = 1
    else:
        presentScore = presentScore - 1
        presentUser.score = presentScore
        correct = 0

    beforePickle = current_user.answered
    afterPickle = loads(beforePickle)

    afterPickle.append(id)
    current_user.answered = dumps(afterPickle)
    db.session.commit()

    return jsonify(score=presentScore, correct=correct)




@app.route('/quiz/<string:topic>')
@login_required
def topicwise(topic):
    topicList = ['artificial_intelligence','networking','introduction_to_computer_science','software_engineering',
                    'databases','machine_learning','operating_systems','other',]
    if topic in topicList:
        form = QuizForm()
        if current_user.answered is None:
            current_user.answered = dumps([])
            db.session.commit()

        alreadyAns = loads(current_user.answered)
    #Check the questions to display
        questions_to_display = Questions.query.filter(Questions.creatorid != str(current_user.id)).filter(~Questions.questionid.in_(alreadyAns)).filter(Questions.topic == topic).all()
        if len(questions_to_display) is 0:
            flash("We're so sorry but it seems that there are no questions on this topic")
        return render_template('quiz.html', questions_to_display=questions_to_display, form=form, users=getScoreboard())
    else:
        form = QuizForm()
        if current_user.answered is None:
            current_user.answered = dumps([])
            db.session.commit()

        alreadyAns = loads(current_user.answered)
        #Check the questions to display
        questions_to_display = Questions.query.filter(Questions.creatorid != str(current_user.id)).filter( ~Questions.questionid.in_(alreadyAns)).all()
        flash('Please enter a url where the topic is any one of' + str(topicList))
        return redirect(url_for('quiz.html', questions_to_display=questions_to_display, form=form, users=getScoreboard()))

@app.route('/score')
@login_required
def scoreboard():

    users = User.query.order_by(User.score.desc())
    return render_template('scoreboard.html', users=users)

#Starting the server with the run method
if __name__ == '__main__':
    app.run()




























