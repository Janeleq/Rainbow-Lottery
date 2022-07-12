from flask import Flask, flash, redirect, url_for, render_template, request
from flask_login import UserMixin, login_user, login_required, LoginManager, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message

#initialise database
app = Flask(__name__)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///database.db'
app.config['SECRET_KEY'] = '123SHEEP'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#models
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)  #nullable means user have to enter this field in

    def _init_(self, username, password):
        self.username = username
        self.password = password
        return f'User {self.username}'

#forms
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=5, max=15)], render_kw={"placeholder": "Username"})
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=15)], render_kw={"placeholder": "Password"})
    remember = BooleanField('Remember Me')
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=5, max=15)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=15)], render_kw={"placeholder": "Password"})
  
    submit = SubmitField("Register")

@app.route("/")
def home():
    return render_template('base.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        email_subject = request.form.get("email-subject")
        message = request.form.get("message")

        msg = Message(email_subject, sender = "janelim2001@gmail.com", recipients = [email])
        msg.body = message
        mail.send(msg)
        success = "Hi" + name + ", your message is sent"

        return render_template("result.html", success=success)
    return render_template("contact.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                flash(user.username)
                return redirect(url_for('game'))

        
        flash('Unsucessful Login. Please try again')
    return render_template('login.html', form=form)

@app.route("/game", methods=['GET', 'POST'])
@login_required
def game():
    return render_template('game.html')

@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    print("here")
    logout_user()
    return render_template('base.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    print(request.form) 
    print(request.method, form.validate())


    if request.method == 'POST' and form.validate():
        print("hi")
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        is_existing_user = User.query.filter_by(username=form.username.data).first()
        print(is_existing_user)
    
        if is_existing_user:
            flash('Register error, username might have been taken, try again!')

        else:
            db.session.add(new_user)
            db.session.commit()
            flash('Thanks for registering, please key in your credentials to log in')
            flash(new_user.username)
            return redirect(url_for('login'))

    return render_template('register.html', form=form)


    
# testing output of routing URLs
# with app.test_request_context():
#     print(url_for('profile', username='John Doe'))
if __name__ == '__main__':
    app.run(debug=True)