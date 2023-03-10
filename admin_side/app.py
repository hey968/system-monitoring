import os

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user, \
    fresh_login_required
from werkzeug.security import generate_password_hash, check_password_hash
from admin_side.forms import LoginForm
import pandas as pd
import json
import htmlentities

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'admin.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.refresh_view = "login"
login_manager.needs_refresh_message = (
    u"To protect your account, please reauthenticate to access this page."
)


def get_conf():
    cwd = os.getcwd()
    return cwd[:cwd.rfind("project") + len("project")] + "\\user_side\\configure.json"


with open(get_conf(), "r") as fd:
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


class rdp_connections(db.Model):
    __tablename__ = "rdp_connections"
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.TEXT)
    date_and_time = db.Column(db.TEXT)


class file_system(db.Model):
    __tablename__ = "file_system"
    id = db.Column(db.Integer, primary_key=True)
    date_and_time = db.Column(db.TEXT)
    event = db.Column(db.TEXT)
    file = db.Column(db.TEXT)


with app.app_context():
    db.create_all()
    # admin = file_system(uname="admin", password=generate_password_hash("123456", method='pbkdf2:sha256', salt_length=8))
    # db.session.add(admin)

login_manager.needs_refresh_message_category = "info"


@app.route('/', methods=["POST", "GET"])
def login():
    if not current_user.is_authenticated:  # if the user isnt log in
        form = LoginForm()  # call the login form from forms.py
        if form.validate_on_submit():
            uname = form.uname.data
            password = form.password.data
            with app.app_context():
                user = User.query.filter_by(uname=uname).first()
            if not user:
                flash("username doesn't exist")
                return redirect(url_for('login'))
            elif not check_password_hash(user.password, password):
                flash('password incorrect')
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
            """
                if the admin send post request about blocking a website
            """
            if "block" in request.form:
                with open("c:\Windows\System32\Drivers\etc\hosts", "a") as fd:
                    fd.write("127.0.0.1 " + request.form["web_name"])
                    unsafe_web_df = pd.read_csv(pwd + "web_checker.csv")
                    unsafe_web_df = unsafe_web_df[unsafe_web_df['website name'] != request.form['web_name']]
                    unsafe_web_df.to_csv(pwd + "web_checker.csv", index=False, header=True)

            else:
                data_web = pd.read_csv(pwd + "web_checker.csv")
                data_web = data_web[data_web['website name'] != request.form['web_name']]
                data_web.to_csv(pwd + "web_checker.csv", index=False, header=True)
        else:
            """
                if the admin approve or disapprove to user keep using the computer
            """
            if "yes" in request.form:
                user_anomaly_detection_df = pd.read_csv(pwd + "user_anomaly_detection.csv")
                user_anomaly_detection_df["accept"][0] = 1
                user_anomaly_detection_df.to_csv(pwd + "user_anomaly_detection.csv", index=False, header=True)
            elif "no" in request.form:
                pass
        return redirect(url_for("admin_panel"))

    if request.method == "GET":
        user_anomaly_detection_df = pd.read_csv(pwd + "user_anomaly_detection.csv").to_dict()
        unsafe_web_df = pd.read_csv(pwd + "web_checker.csv").to_dict()
        if user_anomaly_detection_df['accept'] and user_anomaly_detection_df["accept"][0] == 0:
            """
                create an alert message for admin about exception of user
            """
            user_anomaly_alert = "<div id='details'><h1><u>An exception found</u></h1>" \
                        "<br>" \
                        "<p>" \
                        "details:<br>user: " + str(user_anomaly_detection_df["user"][0]) + "<br>command: " +\
                        str(user_anomaly_detection_df['command'][0]) + "<br> location" + str(user_anomaly_detection_df['location'][0]) + "<br>time to write: " +\
                        str(user_anomaly_detection_df["time_to_write"][0]) + "<br> time in day: " + str(user_anomaly_detection_df["hour"][0]) + ":" \
                        + str(user_anomaly_detection_df["minute"][0]) + "</div>"
        else:
            user_anomaly_alert = False
        if len(unsafe_web_df["protocol"]) > 0:
            forms = ""
            web_table = "<table class='table table-bordered table-hover table-dark'><thead><tr><th>website name</th><th>protocol</th><th>reason</th><th>block</th></tr></thead><tbody>"
            for i in range(len(unsafe_web_df["reason"])):

                """
                    create a table for the suspected websites for admin  
                """

                web_table += "<tr>"
                web_table += "<td><input type='text' name='web_name' form='form" + str(i) + "' value='" + htmlentities.encode(unsafe_web_df["website name"][i]) + "' readonly></td>"
                web_table += "<td><textarea readonly >" + htmlentities.encode(unsafe_web_df["protocol"][i]) + "</textarea></td>"
                web_table += "<td><textarea readonly style='width:100%'>" + htmlentities.encode(unsafe_web_df["reason"][i]) + "</textarea></td>"
                web_table += "<td><input type='submit' style='background-color:red;width:100%' form='form" + str(i) + "' name='block' value='block the website'>"
                web_table += "<br>"
                web_table += "<input type='submit' style='background-color:green;width:100%' form='form" + str(i) + "' name='safe' value='the website is safe'></td>"
                web_table += "</tr>"
                forms += "<form method='post' id='form" + str(i) + "'> </form>"
            web_table += "</tbody></table>"
        else:
            web_table = False
            forms = False
        with app.app_context():
            file_system_table = db.session.query(file_system).order_by(file_system.id.desc()).limit(20).all()
            rdp_table = db.session.query(rdp_connections).order_by(rdp_connections.id.desc()).limit(10).all()
        return render_template("admin_panel.html",
                               file_system_table=file_system_table
                               , rdp_table=rdp_table,
                               user_anomaly_alert=user_anomaly_alert,
                               web_table=web_table,
                               forms=forms)


@app.route("/logout")
@fresh_login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


def run_app():
    app.run('0.0.0.0')


if __name__ == '__main__':
    run_app()
