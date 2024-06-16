from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask import render_template


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:root@localhost:5432/test_db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    age = db.Column(db.Integer)
    email = db.Column(db.String(255))
    job = db.Column(db.String(255))

class Application(db.Model):
    __tablename__ = 'application'
    id = db.Column(db.Integer, primary_key=True)
    appname = db.Column(db.String(255))
    username = db.Column(db.String(255))
    lastconnection = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    user = db.relationship('User', backref=db.backref('applications', lazy=True))


@app.route('/home')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route("/style.css")
def styles():
    return send_from_directory("static", "style.css")

@app.route('/application')
def index2():
    applications = Application.query.all()
    return render_template('index2.html', applications=applications)

'''@app.route('/add', methods=['POST'])
def new_user():
    new_user = User(
        firstname='ines',
        lastname='blancke',
        age=21,
        email='ines.blancke@gmail.com',
        job='student'
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'New user added successfully'}), 201'''