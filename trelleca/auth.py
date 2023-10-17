from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from trelleca import users
from .models import User

auths = Blueprint('auths', __name__)

@auths.route('/login', methods=['GET', 'POST']) #Login
def login():
    if request.method == 'POST':                #Pega-se os dados do forms
        email = request.form.get('email')
        password = request.form.get('password')

        user = users.find_one({"email":email})
        if user:                                #Checamos se o usuário existe no banco (lembrando que ao criar a conta garantimos que não exista dois usuários com o mesmo email)
            if check_password_hash(user['password'], password): #Verificamos se a senha está correta
                flash(f"Welcome {user['fName']}!",category='success')
                user_id = str(user["_id"])
                user_obj = User(user_id)
                login_user(user_obj, remember=True)
                tasks = user['tasks']   
                return redirect(url_for('views.home', tasks = tasks)) #Passamos a lista de tarefas do usuário a ser exibida na página Home
            else:
                flash("Senha Incorreta", category='error')
        else:
            flash("Email incorreto", category='error')
    return render_template('login.html')

@auths.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auths.login'))

@auths.route('/sign-up', methods=['GET', 'POST']) #Criação da conta
def signup():
    if request.method == 'POST':                  #Pegamos os dados do forms
        email = request.form.get('email')
        fName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = users.find_one({"email":email})

        if user:                                                #Verificamos se o usuário já existe e se não vemos se os dados informados são válidos
            flash("Email aready registered", category='error')
        elif len(email) < 5:
            flash("The email must be longer than 2 characters", category='error')
        elif len(fName) < 2:
            flash("The name must be longer than 2 characters", category='error')
        elif len(password1) < 7:
            flash("Password too short", category='error')
        elif password1 != password2:
            flash("Passwords don't match")
        else:                                                   #Se estiver tudo certo os dados são inseridos no banco mongo e a conta é criada!
            users.insert_one({
                "email":email,
                "fName": fName,
                "password":generate_password_hash(password1, method='sha256'),
                "tasks":[]
            })
            flash("Account created!",category='success')

            return redirect(url_for('views.home'))
            
    return render_template("sign-up.html")


@auths.route('/task', methods=['GET','POST'])
def task():
    return render_template('task.html')