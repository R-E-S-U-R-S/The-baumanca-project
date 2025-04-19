from flask import Flask, render_template, request, flash,redirect,url_for, session
from src.service import Service
from forms import *
from src.entity import *
from src.errors import UserAlreadyExists
# todo сделать странички (главную и по набору) - красивыми :)

app = Flask(__name__)
app.config["SECRET_KEY"] = "1112"

MAX_PARTS_QUERY_ARG="max_parts"

service=Service()
#todo добавить нормальные декораторы для login check

@app.route('/setid/<id>')
def setpage(id):
    if session.get("login") is None:
        return redirect(url_for("login"))
    get_set_by_id=id
    setinfo=service.get_set_info_by_id(get_set_by_id)
    return render_template("set.html", setinfo=setinfo)

@app.route('/', methods=["GET","POST"])
def search():
    if session.get("login") is None:
        return redirect(url_for("login"))
    
    form=SearchForm()
    user_sets=service.get_sets_by_user(session.get("login"))
    if form.validate_on_submit():
        search_string = form.search_string.data
        search_results=service.search_set_by_string(search_string)    
        user_sets_ids=[]
        for user_set in user_sets:
            user_sets_ids.append(user_set.id)
        return render_template("mainpage.html", user_sets=user_sets, user_sets_ids=user_sets_ids, form=form, results=search_results )
    return render_template("mainpage.html", user_sets=user_sets, form=form )


@app.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user_data=UserData(login=form.username.data, password=form.password.data)
        if service.check_user_password(user_data) == False:
            flash("Проверь логин или пароль", "danger")
        else:
            session['login']=user_data.login
            return redirect(url_for('search'))

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
            flash("аккаунт был  создан!", "success")
            return redirect(url_for('login'))

    return render_template("register.html", form=form)

@app.route('/logout')
def logout():
    session.pop('login', None)
    return redirect(url_for('login'))


@app.route("/add_set_to_user/<set_id>", methods=["POST"])
def add_to_user(set_id):
    if session.get("login") is None:
        return redirect(url_for("login"))

    service.add_set_to_user(session["login"], set_id)
    flash("набор успешно добавлен", "success")
    return redirect(url_for("search"))


@app.route("/delete_set_from_user/<set_id>", methods=["POST"])
def delete_from_user(set_id):
    if session.get("login") is None:
        return redirect(url_for("login"))

    service.delete_set_from_user(session["login"], set_id)
    flash("набор успешно удалён", "success")
    return redirect(url_for("search"))

@app.route("/search_by_users_sets", methods=["GET","POST"])
def get_search_by_sets():
    if session.get("login") is None:
        return redirect(url_for("login"))
    form=SearchSetsBySets()
    if form.validate_on_submit():
        max_parts=form.max_parts.data
        login=session.get("login")
        search_result=service.search_sets_depending_on_user_sets(login, max_parts)
        return render_template("search_by_sets.html", results=search_result, form=form)

    return render_template("search_by_sets.html", form=form)





if __name__ == '__main__':
    app.run(debug=True)

