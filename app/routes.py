from flask import render_template,flash,redirect,url_for
from app import app
from app.forms import LoginForm
from flask_login import current_user,login_user
import sqlalchemy as sa
from app import db
from app.models import User
from flask_login import logout_user

@app.route('/')
@app.route('/index')
def index():
    user={'username':'Miguel'}
    posts=[
        {
            'author':{'username':'John'},
            'body':'Beautiful day in Potland!'
        },
        {
            'author':{'username':'Susan'},
            'body':'The avenger movie was so cool!'
        }
    ]
    return render_template('index.html',title='Home',user=user,posts=posts)

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=LoginForm()
    if form.validate_on_submit(): #form.validate_on_submit() method does all the form processing work. 
        user=db.session.scalar(
            sa.select(User).where(User.username==form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user,remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html',title='Sign In',form=form)
#When the browser sends the GET request to receive the web page with the form, this method is going to return False, so in that case the function skips the if statement and goes directly to render the template in the last line of the function.

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))