# I am using mediapipe as a hand landmark processing and prediction and landmark detector and a Random Forest classifier as sign classifier.

# Suppress sklearn InconsistentVersionWarning (model trained with 1.3.0, runtime 1.8+)
import warnings
try:
    from sklearn.exceptions import InconsistentVersionWarning
    warnings.filterwarnings('ignore', category=InconsistentVersionWarning)
except ImportError:
    pass

# ✅ STABILITY FIX: Use threading mode by default to avoid:
# - AttributeError: RequestContext.session has no setter (Flask 3.x + eventlet)
# - Eventlet deprecation warnings and ConnectionAbortedError on Windows
# Only load eventlet if SOCKETIO_ASYNC_MODE=eventlet (requires requirements_stable.txt + Python 3.11)
import os as _os_env
if _os_env.environ.get('SOCKETIO_ASYNC_MODE') == 'eventlet':
    import eventlet
    eventlet.monkey_patch()

from wsgiref.simple_server import WSGIServer
from flask import Flask, jsonify, render_template, url_for, redirect, flash, session, request, Response
import sys
import os
import glob
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, Email, EqualTo
from flask_bcrypt import Bcrypt
from datetime import datetime
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from flask_mail import Message, Mail
import random
import re
import pickle
from flask_socketio import SocketIO, emit
import threading
import time
import socket
import select

def dlog(msg):
    with open("diagnostic_debug.log", "a") as f:
        f.write(msg + "\n")
        f.flush()

app = Flask(__name__)

CORS(app)  # Allow cross-origin requests for all routes

# -------------------SocketIO Configuration-------------------
# Use threading mode (stable with Flask 3.x, no eventlet session/setter issues)
# Set SOCKETIO_ASYNC_MODE=eventlet in .env to use eventlet (requires Flask 2.3.x stack)
_async_mode = _os_env.environ.get('SOCKETIO_ASYNC_MODE', 'threading')
socketio = SocketIO(app, cors_allowed_origins="*", async_mode=_async_mode, manage_session=False)

# Shared camera instance with lock for thread safety
camera = None
camera_lock = threading.Lock()
camera_active = False

# -------------------Encrypt Password using Hash Func-------------------
bcrypt = Bcrypt(app)

# -------------------Database Model Setup-------------------
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///database.db')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'change-me-in-production')
serializer = Serializer(app.config['SECRET_KEY'])
db = SQLAlchemy(app)
app.app_context().push()


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# -------------------mail configuration-------------------
app.config["MAIL_SERVER"] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config["MAIL_PORT"] = int(os.environ.get('MAIL_PORT', 587))
app.config["MAIL_USERNAME"] = os.environ.get('MAIL_USERNAME', '')
app.config["MAIL_PASSWORD"] = os.environ.get('MAIL_PASSWORD', '')
app.config["MAIL_USE_TLS"] = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'
app.config["MAIL_USE_SSL"] = os.environ.get('MAIL_USE_SSL', 'false').lower() == 'true'
mail = Mail(app)
# --------------------------------------------------------


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# -------------------Database Model-------------------


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
# ----------------------------------------------------

# -------------------Welcome or Home Page-------------

import os
import glob

# ... (existing imports)

# -------------------Helper for Dynamic Background Video-------------------
def get_background_video():
    """
    Scans static/videos/ for the first available video file.
    Returns a dict with 'url' and 'timestamp' (for cache busting).
    Returns None if no video is found.
    """
    video_dir = os.path.join(app.root_path, 'static', 'videos')
    # Support common video formats
    video_files = glob.glob(os.path.join(video_dir, '*.mp4')) + \
                  glob.glob(os.path.join(video_dir, '*.webm'))
    
    if video_files:
        # Take the first video found
        video_path = video_files[0]
        video_filename = os.path.basename(video_path)
        # Get modification time for cache busting
        timestamp = int(os.path.getmtime(video_path))
        
        return {
            'url': url_for('static', filename=f'videos/{video_filename}'),
            'timestamp': timestamp
        }
    return None

# -------------------Welcome or Home Page-------------

@app.route('/', methods=['GET', 'POST'])
def home():
    session.clear()
    video_data = get_background_video()
    return render_template('home.html', video_data=video_data)
# ----------------------------------------------------

# -------------------feed back Page-----------------------
@app.route('/feed', methods=['GET', 'POST'])
def feed():
    return render_template('feed.html')
# ----------------------------------------------------


# -------------------Discover More Page---------------
@app.route('/discover_more', methods=['GET', 'POST']) 
def discover_more():
    return render_template('discover_more.html')
# ----------------------------------------------------

# ------------------- New Unified Pages (Navigation Restructure) --------

# Sign-Text & Text-Sign Converter (combines Sign → Text camera + Text → Sign images)
@app.route('/sign-text-converter', methods=['GET'])
def sign_text_converter():
    name = session.get('name', 'Guest')
    return render_template('sign_text_converter.html', name=name)

# Voice-Sign & Sign-Voice Converter (combines Voice → Sign + Sign → Voice)
@app.route('/voice-converter', methods=['GET'])
def voice_converter():
    return render_template('voice_converter.html')


@app.route('/sign-language', methods=['GET'])
def sign_language():
    # Old Text → Sign generator - redirect to new unified page
    flash('This page has moved! Redirecting to Sign-Text & Text-Sign converter.', 'info')
    return redirect(url_for('sign_text_converter'))

@app.route('/generate_sign_video_api', methods=['POST'])
def generate_sign_video_api():
    data = request.get_json()
    text = data.get('text')
    language = data.get('language', 'ASL')
    
    result = sign_service.generate_sign_video(text, language)
    return jsonify(result)
# ----------------------------------------------------


# -------------------Login Page-------------------
class LoginForm(FlaskForm):
    username = StringField(label='username', validators=[InputRequired()], render_kw={"placeholder": "Username"})
    email = StringField(label='email', validators=[InputRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField(label='password', validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # Check if the user has registered before showing the login form
    if 'registered' in session and session['registered']:
        session.pop('registered', None)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data) and User.query.filter_by(email=form.email.data).first():
            login_user(user)
            flash('Login successfully.', category='success')
            name = form.username.data
            session['name'] = name
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash(f'Login unsuccessful for {form.username.data}.', category='danger')
    return render_template('login.html', form=form)
# ----------------------------------------------------


# -------------------Dashboard or Logged Page-------------------
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    name = session.get('name', 'Tester')
    return render_template('dashboard.html', name=name)
# ----------------------------------------------------

# -------------------About Page-----------------------
@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')
# ----------------------------------------------------

# -------------------Logged Out Page-------------------

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    session.clear()
    logout_user()
    flash('Account Logged out successfully.', category='success')
    return redirect(url_for('login'))
# ----------------------------------------------------

# -------------------Register Page-------------------

class RegisterForm(FlaskForm):
    username = StringField(label='username', validators=[InputRequired()], render_kw={"placeholder": "Username"})
    email = StringField(label='email', validators=[InputRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField(label='password', validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField(label='confirm_password', validators=[InputRequired(), EqualTo('password')], render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            flash('That Username already exists. Please choose a different one.', 'danger')
            raise ValidationError('That username already exists. Please choose a different one.')


@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data,email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        # Set a session variable to indicate successful registration
        session['registered'] = True
        flash(f'Account Created for {form.username.data} successfully.', category='success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)
# ----------------------------------------------------

# -------------------Update or reset Email Page-------------------


class ResetMailForm(FlaskForm):
    username = StringField(label='username', validators=[InputRequired()], render_kw={"placeholder": "Username"})
    email = StringField(label='email', validators=[InputRequired(), Email()], render_kw={"placeholder": "Old Email"})
    new_email = StringField(label='new_email', validators=[InputRequired(), Email()], render_kw={"placeholder": "New Email"})
    password = PasswordField(label='password', validators=[InputRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login', validators=[InputRequired()])


@app.route('/reset_email', methods=['GET', 'POST'])
@login_required
def reset_email():
    form = ResetMailForm()
    if 'logged_in' in session and session['logged_in']:
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data) and User.query.filter_by(email=form.email.data).first():
                user.email = form.new_email.data  # Replace old email with new email
                db.session.commit()
                flash('Email reset successfully.', category='success')
                session.clear()
                return redirect(url_for('login'))
            else:
                flash('Invalid email, password, or combination.', category='danger')

        return render_template('reset_email.html', form=form)
    return redirect(url_for('login'))
# --------------------------------------------------------------

# -------------------Forgot Password With OTP-------------------

class ResetPasswordForm(FlaskForm):
    username = StringField(label='username', validators=[InputRequired()], render_kw={"placeholder": "Username"})
    email = StringField(label='email', validators=[InputRequired(), Email()], render_kw={"placeholder": "Email"})
    submit = SubmitField('Submit', validators=[InputRequired()])


class ForgotPasswordForm(FlaskForm):
    username = StringField(label='username', validators=[InputRequired()], render_kw={"placeholder": "Username"})
    email = StringField(label='email', validators=[InputRequired(), Email()], render_kw={"placeholder": "Email"})
    new_password = PasswordField(label='new_password', validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "New Password"})
    confirm_password = PasswordField(label='confirm_password', validators=[InputRequired(), EqualTo('new_password')], render_kw={"placeholder": "Confirm Password"})
    otp = StringField(label='otp', validators=[InputRequired(), Length(min=6, max=6)], render_kw={"placeholder": "Enter OTP"})
    submit = SubmitField('Submit', validators=[InputRequired()])


@staticmethod
def send_mail(name, email, otp):
    msg = Message('Reset Email OTP Password',sender='handssignify@gmail.com', recipients=[email])
    msg.body = "Hii " + name + "," + "\nYour email OTP is :"+str(otp)
    mail.send(msg)


    # Generate your OTP logic here
def generate_otp():
    return random.randint(100000, 999999)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    otp = generate_otp()
    session['otp'] = otp
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and User.query.filter_by(email=form.email.data).first():
            send_mail(form.username.data, form.email.data, otp)
            flash('Reset Request Sent. Check your mail.', 'success')
            return redirect(url_for('forgot_password'))
        else:
            flash('Email and username combination is not exist.', 'danger')
    return render_template('reset_password_request.html', form=form)


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        otp = request.form['otp']
        valid = (otp == request.form['otp'])

        if valid:
            user = User.query.filter_by(username=form.username.data).first()
            if user and User.query.filter_by(email=form.email.data).first():
                user.password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
                db.session.commit()
                flash('Password Changed Successfully.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Email and username combination is not exist.', 'danger')
        else:
            flash("OTP verification failed.", 'danger')
    return render_template('forgot_password.html', form=form)
# ---------------------------------------------------------------

# ------------------------- Update Password ---------------------

class UpdatePasswordForm(FlaskForm):
    username = StringField(label='username', validators=[InputRequired()], render_kw={"placeholder": "Username"})
    email = StringField(label='email', validators=[InputRequired(), Email()], render_kw={"placeholder": "Email"})
    new_password = PasswordField(label='new_password', validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "New Password"})
    confirm_password = PasswordField(label='confirm_password', validators=[InputRequired(), EqualTo('new_password')], render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Submit', validators=[InputRequired()])


@app.route('/update_password', methods=['GET', 'POST'])
@login_required
def update_password():
    form = UpdatePasswordForm()
    if form.validate_on_submit() and 'logged_in' in session and session['logged_in']:

            user = User.query.filter_by(username=form.username.data).first()
            if user and User.query.filter_by(email=form.email.data).first():
                user.password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
                db.session.commit()
                flash('Password Changed Successfully.', 'success')
                session.clear()
                return redirect(url_for('login'))
            else:
                flash("Username and email combination is not exist.", 'danger')
    return render_template('update_password.html', form=form)
# -----------------------------  end  ---------------------------


# --------------------------- Machine Learning# -------------------Background UDP Listeners-------------------
latest_frame_jpeg = None
frame_lock = threading.Lock()

def udp_video_listener():
    """Listens for JPEG frames from the standalone camera engine process."""
    global latest_frame_jpeg
    dlog("DIAGNOSTIC: UDP Video Listener Starting on 5555")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', 5555))
    sock.settimeout(1.0)
    
    while True:
        try:
            data, _ = sock.recvfrom(65507)
            if data:
                dlog(f"DIAGNOSTIC: Received UDP Packet, length={len(data)}")
                with frame_lock:
                    latest_frame_jpeg = data
        except socket.timeout:
            continue
        except Exception as e:
            dlog(f"UDP VIDEO ERROR: {e}")
            time.sleep(1)

def udp_prediction_listener():
    """Listens for predictions from standalone camera engine process."""
    dlog("DIAGNOSTIC: UDP Prediction Listener Starting on 5556")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', 5556))
    sock.settimeout(1.0)
    
    labels_dict = {
        '0': 'A', '1': 'B', '2': 'C', '3': 'D', '4': 'E', '5': 'F', '6': 'G', '7': 'H', '8': 'I', 
        '9': 'J', '10': 'K', '11': 'L', '12': 'M', '13': 'N', '14': 'O', '15': 'P', '16': 'Q', 
        '17': 'R', '18': 'S', '19': 'T', '20': 'U', '21': 'V', '22': 'W', '23': 'X', '24': 'Y', 
        '25': 'Z', '26': 'Hello', '27': 'Done', '28': 'Thank You', '29': 'I Love you', 
        '30': 'Sorry', '31': 'Please', '32': 'You are welcome.'
    }
    
    last_prediction = None
    stable_count = 0
    STABILITY_THRESHOLD = 5
    
    while True:
        try:
            data, _ = sock.recvfrom(1024)
            if data:
                predicted_label = data.decode('utf-8')
                dlog(f"DIAGNOSTIC: Received prediction: {predicted_label}")
                predicted_character = labels_dict.get(predicted_label, predicted_label)
                
                # Emit to socketio
                socketio.emit('prediction', {
                    'character': predicted_character,
                    'timestamp': datetime.now().isoformat()
                }, namespace='/')
                
                if predicted_character == last_prediction:
                    stable_count += 1
                else:
                    stable_count = 0
                    last_prediction = predicted_character
                
                if stable_count == STABILITY_THRESHOLD:
                    socketio.emit('stable_prediction', {
                        'character': predicted_character,
                        'timestamp': datetime.now().isoformat()
                    }, namespace='/')
                    stable_count = 0 
                
        except socket.timeout:
            continue
        except Exception as e:
            time.sleep(1)

# Start listeners automatically
vid_thread = threading.Thread(target=udp_video_listener, daemon=True)
vid_thread.start()

pred_thread = threading.Thread(target=udp_prediction_listener, daemon=True)
pred_thread.start()

# -------------------WebSocket Event Handlers-------------------
@socketio.on('disconnect')
def handle_disconnect():
    pass

# -------------------Video Frame Generation-------------------
def generate_frames():
    """Yield MJPEG frames from the background UDP buffer."""
    global latest_frame_jpeg
    
    # Wait for the first frame
    timeout = 100
    while latest_frame_jpeg is None and timeout > 0:
        time.sleep(0.05)
        timeout -= 1
        
    while True:
        with frame_lock:
            frame_bytes = latest_frame_jpeg
        if frame_bytes is not None:
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        time.sleep(0.033)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/shutdown', methods=['POST'])
def shutdown():
    # Only allow shutdown from localhost for security
    if request.remote_addr != '127.0.0.1':
        return jsonify({"success": False, "message": "Unauthorized"}), 403
    
    import os
    import signal
    
    # Graceful shutdown using a signal
    os.kill(os.getpid(), signal.SIGINT)
    return jsonify({"success": True, "message": "Server shutting down..."})

# -----------------------------  end  ---------------------------

if __name__ == '__main__':
    print("HandSignify starting... (SocketIO async_mode=%s)" % _async_mode)
    try:
        socketio.run(app, debug=True, use_reloader=False, host='127.0.0.1', port=5000,
                     allow_unsafe_werkzeug=True)  # Required by Werkzeug 3.x in development
    except Exception as e:
        sys.stderr.write("FATAL: Server failed to start: %s\n" % e)
        raise