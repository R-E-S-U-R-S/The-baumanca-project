from flask import Flask, render_template, request, flash,redirect,url_for, session
from src.service import Service
from forms import *
from src.entity import *
from src.errors import UserAlreadyExists
# todo сделать странички (главную и по набору) - красивыми :)
# todo сделать кнопки (Залогиниться/Зарегестрироваться\выйти) в шапке сайта

app = Flask(__name__)
app.config["SECRET_KEY"] = "1112"

service=Service()
#todo добавить нормальные декораторы для login check
@app.route('/')
def index():
    if session.get("login") is None:
        return redirect(url_for("login"))

    return render_template("mainpage.html")
@app.route('/setid/<int:id>')
def setpage(id):
    if session.get("login") is None:
        return redirect(url_for("login"))
    get_set_by_id=id
    setinfo=service.get_set_info_by_id(get_set_by_id)
    return render_template("set.html", setinfo=setinfo)

@app.route('/search/')
def search():
    if session.get("login") is None:
        return redirect(url_for("login"))
    search_string = request.args.get('search_string')
    results=service.search_set_by_string(search_string)
    return render_template("search_main.html", results=results, )


@app.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user_data=UserData(login=form.username.data, password=form.password.data)
        if service.check_user_password(user_data) == False:
            flash("Проверь логин или пароль", "danger")
        else:
            session['login']=user_data.login
            return redirect(url_for('index'))

    return render_template("login.html", form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        user_data=UserData(login=form.username.data, password=form.password.data)
        try:
            service.create_user(user_data)
        except UserAlreadyExists:
            flash("аккаунт с таким имнем уже создан", "danger")
        else:
            flash("аккаунт был  создан!!!!111!!1", "success")
        return redirect(url_for('login'))

    return render_template("register.html", form=form)

@app.route('/logout')
def logout():
    session.pop('login', None)
    return redirect(url_for('login'))


@app.route("/add_set_to_user/<int:set_id>", methods=["POST"])
def add_to_user(set_id):
    if session.get("login") is None:
        return redirect(url_for("login"))

    service.add_set_to_user(session["login"], set_id)
    flash("набор успешно добавлен", "success")


if __name__ == '__main__':
    app.run(debug=True)