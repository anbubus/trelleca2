from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from trelleca import db

auths = Blueprint('auths', __name__)

@auths.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = db.users.find_one({"email":email})
        if user:
            if check_password_hash(user['password'], password):
                flash(f"Bem vindo {user['fName']}",category='success')

                return redirect(url_for('views.home'))
            else:
                flash("Senha Incorreta",category='error')
    return render_template('login.html')

@auths.route('/logout')
def logout():
    #logout_user()
    return redirect(url_for('auths.login'))

@auths.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        fName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 5:
            flash("Email tem que ser masior q 5 caracteres", category='error')
        elif len(fName) < 2:
            flash("O nome deve ter mais q 2 caracteres", category='error')
        elif len(password1) < 7:
            flash("Senha muito pequena", category='error')
        elif password1 != password2:
            flash("Senhas n batem")
        else:
            db.users.insert_one({
                "email":email,
                "fName": fName,
                "password":generate_password_hash(password1, method='sha256')
            })

            flash("Conta criada cm sucesso!!",category='success')

            return redirect(url_for('views.home'))
            #create account
    return render_template("sign-up.html")


@auths.route('/task', methods=['GET','POST'])
def task():
    return render_template('task.html')