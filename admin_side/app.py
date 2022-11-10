from flask import Flask, render_template, redirect, url_for, flash, abort, request, make_response
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user, \
    fresh_login_required
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm
import pandas as pd
import json
import htmlentities


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///admin.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
# app.config.update(
#     SESSION_COOKIE_SECURE=True,
#     SESSION_COOKIE_HTTPONLY=True,
#     SESSION_COOKIE_SAMESITE='Lax',
#
# )
login_manager.refresh_view = "login"
login_manager.needs_refresh_message = (
    u"To protect your account, please reauthenticate to access this page."
)

with open("../user_side/configure.json", "r") as fd:
    json_data = json.load(fd)
pwd = json_data["user_side_loc"]
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    uname = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=False)


db.create_all()
login_manager.needs_refresh_message_category = "info"


# admin = User(uname="admin",password=generate_password_hash("123456",method='pbkdf2:sha256',salt_length=8))
# db.session.add(admin)
# db.session.commit()


@app.route('/', methods=["POST", "GET"])
def login():  # put application's code here
    if not current_user.is_authenticated:  # if the user isnt log in
        form = LoginForm()  # call the login form from forms.py
        if form.validate_on_submit():
            uname = htmlentities.encode(form.uname.data)  # prevent xss
            password = htmlentities.encode(form.password.data)  # prevent xss

            user = User.query.filter_by(uname=uname).first()
            # Email doesn't exist or password incorrect.
            if not user:
                flash("משתמש לא קיים")
                return redirect(url_for('login'))
            elif not check_password_hash(user.password, password):
                flash('סיסמה לא נכונה נסה שוב')
                return redirect(url_for('login'))
            else:
                login_user(user)
                return redirect(url_for("admin_panel"))
        return render_template("index.html", form=form)
    else:
        return redirect(url_for("admin_panel"))


@app.route("/admin panel", methods=["POST", "GET"])
def admin_panel():
    if not current_user.is_authenticated:
        return url_for("login")
    if request.method == "POST":
        if "web_name" in request.form:
            if "block" in request.form:
                with open("c:\Windows\System32\Drivers\etc\hosts", "a") as fd:
                    fd.write("127.0.0.1 "+request.form["web_name"])
                    data_web = pd.read_csv(pwd+"web_checker.csv")
                    data_web = data_web.iloc[1:]
                    data_web.to_csv(pwd + "web_checker.csv", index=False, header=True)

            else:
                pass
        else:
            if "yes" in request.form:
                df = pd.read_csv(pwd+"user_anomaly_detection.csv")
                df["accept"][0] = 1
                df.to_csv(pwd+"user_anomaly_detection.csv",index=False,header=True)
            elif "no" in request.form:
                pass



            data = pd.read_csv(pwd+"user_anomaly_detection.csv").to_dict()
        return redirect(url_for("admin_panel"))

    if request.method == "GET":
        data = pd.read_csv(pwd+"user_anomaly_detection.csv").to_dict()
        data_web = pd.read_csv(pwd+"web_checker.csv").to_dict()
        if data['accept'] and data["accept"][0] == 0:
            data_html = "<div><h1><u>An exception found</u></h1>" \
                        "<br>" \
                        "<p>" \
                        "details:<br>user: "+str(data["user"][0])+"<br>command: "+str(data['command'][0])+"<br> location"+str(data['location'][0])+"<br>time to write: " + str(data["time_to_write"][0]) + "<br> time in day: " + str(data["hour"][0])+":"\
                        +str(data["minute"][0])+"</div>"
        else:
            data_html = False
        if len(data_web["protocol"]) > 0:
            forms = ""
            web_checker = "<table class='table table-bordered table-hover table-dark'><thead><tr><th>website name</th><th>protocol</th><th>reason</th><th>block</th></tr></thead><tbody>"
            for i in range(len(data_web["reason"])):
                web_checker += "<tr>"
                for key in data_web.keys():
                    web_checker += "<td><input type='text' name='web_name' form='form"+str(i)+"' value=" + data_web[key][i] + " readonly></td>"
                web_checker += "<td><input type='submit' form='form" + str(i) + "' name='block' value='block the website'><br>" \
                               "<input type='submit' form='form" + str(i) + "' name='safe' value='the website is safe'></td>"
                web_checker += "</tr>"
                forms += "<form method='post' id='form"+str(i)+"'> </form>"
            web_checker += "</tbody></table>"
        else:
            web_checker=False
            forms = False
        return render_template("admin_panel.html", file_tables=[
            (pd.read_csv(pwd+"file_system.csv").sort_values(by='date_and_time',ascending=False)).to_html(classes='table table-bordered table-hover table-dark', index=False,
                                                                table_id='file_system_table').replace("<thead>",
                                                                                                      "<thead class='sticky-top bg-white'")],rdp_tables=[
            (pd.read_csv(pwd+"rdp_connections.csv").sort_values(by='date_and_time',ascending=False)).to_html(classes='table table-bordered table-dark table-hover', index=False,
                                                                table_id='file_system_table').replace("<thead>",
                                                                                                      "<thead class='sticky-top bg-white'")],data_html=data_html,web_checker=web_checker,forms=forms)
@app.route("/logout")
@fresh_login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
