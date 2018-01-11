from flask_wtf import Form
from wtforms import PasswordField, SelectField, BooleanField, StringField
from wtforms.validators import DataRequired, Length, EqualTo

class RegisterForm(Form):
    name = StringField('name', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=3, max=25)])
    confirm = PasswordField('confirm', validators=[DataRequired(), EqualTo('password', message='Both passwords must match!!')])

class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class QuestionForm(Form):
    question = StringField('question', validators=[DataRequired()])
    option1 = StringField('option1', validators=[DataRequired()])
    option2 = StringField('option2', validators=[DataRequired()])
    option3 = StringField('option3', validators=[DataRequired()])
    option4 = StringField('option4', validators=[DataRequired()])
    answer = SelectField('answer', choices=[('option1', 'A'), ('option2', 'B'), ('option3', 'C'), ('option4', 'D')], validators=[DataRequired()])
    topic = SelectField('topic',
                           choices=[('artificial_intelligence','Artificial Intelligence'),
                                    ('networking','Networking'),
                                    ('introduction_to_computer_science','Introduction to Computer Science'),
                                    ('software_engineering','Software Engineering'),
                                    ('databases','Databases'),
                                    ('machine_learning', 'Machine Learning'),
                                    ('operating_systems', 'Operating Systems'),
                                    ('other', 'Other')],
                           validators=[DataRequired()])
    difficulty = SelectField('Difficulty',
                             choices=[('easy', 'Easy'), ('moderate', 'Moderate'), ('hard', 'Hard'), ('insane', 'Insane')],
                             validators=[DataRequired()])

class QuizForm(Form):
    attempted_answer = SelectField('attempted_answer', choices=[('option1', 'A'), ('option2', 'B'), ('option3', 'C'), ('option4', 'D')],
                                   validators=[DataRequired()])
