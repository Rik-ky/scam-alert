from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from functools import wraps
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scam_alert.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email config (Gmail SMTP)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'richland4040@gmail.com'
app.config['MAIL_PASSWORD'] = 'qezi vfor vles juju'
app.config['MAIL_DEFAULT_SENDER'] = 'richland4040@gmail.com'

mail = Mail(app)
db = SQLAlchemy(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# ------------------ Models ------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)

# ------------------ Auth Helpers ------------------

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("You must be logged in to access this page.", "danger")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def current_user():
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None

# ------------------ Routes ------------------

@app.route('/')
def home():
    return render_template('home.html', user=current_user())

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']

        if password != confirm:
            flash("Passwords do not match", "danger")
            return redirect(url_for('register'))

        existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
        if existing_user:
            flash("Email or username already exists", "danger")
            return redirect(url_for('register'))

        hashed_pw = generate_password_hash(password)
        user = User(email=email, username=username, password=hashed_pw)
        db.session.add(user)
        db.session.commit()

        # Send verification email
        token = s.dumps(email, salt='email-confirm')
        link = url_for('confirm_email', token=token, _external=True)
        msg = Message('Confirm Your Email', recipients=[email])
        msg.body = f'Click the link to verify your email: {link}'
        mail.send(msg)

        flash("Account created! Check your email to verify your account.", "info")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except SignatureExpired:
        flash("The confirmation link has expired.", "danger")
        return redirect(url_for('login'))
    except BadSignature:
        flash("Invalid or broken confirmation link.", "danger")
        return redirect(url_for('login'))

    user = User.query.filter_by(email=email).first()
    if user:
        user.is_verified = True
        db.session.commit()
        flash("Email verified. You can now log in.", "success")
        return redirect(url_for('login'))

    flash("User not found.", "danger")
    return redirect(url_for('register'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            if not user.is_verified:
                flash("Please verify your email before logging in.", "warning")
                return redirect(url_for('login'))

            session['user_id'] = user.id
            flash(f"Welcome, {user.username}!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials", "danger")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Logged out successfully.", "info")
    return redirect(url_for('login'))

@app.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        description = request.form['description']
        new_report = Report(name=name, phone=phone, description=description)
        db.session.add(new_report)
        db.session.commit()
        flash("Scam report submitted successfully!", "success")
        return redirect(url_for('home'))

    return render_template('report.html', user=current_user())

@app.route('/reports')
@login_required
def reports():
    all_reports = Report.query.all()
    return render_template('reports.html', reports=all_reports, user=current_user())

# ------------------ Main ------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
