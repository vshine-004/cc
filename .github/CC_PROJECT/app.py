from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///events.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(64))
    events = db.relationship('Event', backref='organizer', lazy=True)
    registrations = db.relationship('Registration', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    max_participants = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(200))
    category = db.Column(db.String(50), nullable=False)
    organizer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    registrations = db.relationship('Registration', backref='event', lazy=True)

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    now = datetime.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    # Get ongoing events (events happening today)
    ongoing_events = Event.query.filter(
        Event.date.between(today_start, today_end)
    ).order_by(Event.date).all()
    
    # Get upcoming events (future events)
    upcoming_events = Event.query.filter(
        Event.date > today_end
    ).order_by(Event.date).all()
    
    return render_template('index.html', 
                         ongoing_events=ongoing_events,
                         upcoming_events=upcoming_events)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')

        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('register'))

        user = User(email=email, name=name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))

        flash('Invalid email or password', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        date = datetime.strptime(request.form.get('date'), '%Y-%m-%dT%H:%M')
        location = request.form.get('location')
        max_participants = int(request.form.get('max_participants'))
        category = request.form.get('category')
        image_url = request.form.get('image_url')

        event = Event(
            title=title,
            description=description,
            date=date,
            location=location,
            max_participants=max_participants,
            category=category,
            image_url=image_url,
            organizer_id=current_user.id
        )

        db.session.add(event)
        db.session.commit()

        flash('Event created successfully!', 'success')
        return redirect(url_for('event_detail', event_id=event.id))

    return render_template('create_event.html')

@app.route('/event/<int:event_id>')
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    is_registered = False
    if current_user.is_authenticated:
        is_registered = Registration.query.filter_by(
            user_id=current_user.id,
            event_id=event_id
        ).first() is not None
    return render_template('event_detail.html', event=event, is_registered=is_registered)

@app.route('/register_event/<int:event_id>', methods=['POST'])
@login_required
def register_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    if Registration.query.filter_by(user_id=current_user.id, event_id=event_id).first():
        flash('You are already registered for this event.', 'warning')
        return redirect(url_for('event_detail', event_id=event_id))

    if len(event.registrations) >= event.max_participants:
        flash('Sorry, this event is full.', 'danger')
        return redirect(url_for('event_detail', event_id=event_id))

    registration = Registration(user_id=current_user.id, event_id=event_id)
    db.session.add(registration)
    db.session.commit()

    flash('Successfully registered for the event!', 'success')
    return redirect(url_for('event_detail', event_id=event_id))

@app.route('/unregister_event/<int:event_id>', methods=['POST'])
@login_required
def unregister_event(event_id):
    registration = Registration.query.filter_by(
        user_id=current_user.id,
        event_id=event_id
    ).first_or_404()
    
    db.session.delete(registration)
    db.session.commit()

    flash('Successfully unregistered from the event.', 'success')
    return redirect(url_for('event_detail', event_id=event_id))

@app.route('/api/events')
def get_events():
    category = request.args.get('category')
    query = Event.query
    
    if category:
        query = query.filter_by(category=category)
    
    events = query.all()
    return jsonify([{
        'id': event.id,
        'title': event.title,
        'description': event.description,
        'date': event.date.isoformat(),
        'location': event.location,
        'max_participants': event.max_participants,
        'current_participants': len(event.registrations),
        'category': event.category,
        'image_url': event.image_url
    } for event in events])

@app.route('/category/<category>')
def category_events(category):
    now = datetime.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    # Get ongoing events for this category
    ongoing_events = Event.query.filter(
        Event.category == category,
        Event.date.between(today_start, today_end)
    ).order_by(Event.date).all()
    
    # Get upcoming events for this category
    upcoming_events = Event.query.filter(
        Event.category == category,
        Event.date > today_end
    ).order_by(Event.date).all()
    
    # Get past events for this category
    past_events = Event.query.filter(
        Event.category == category,
        Event.date < today_start
    ).order_by(Event.date.desc()).all()
    
    category_info = {
        'music': {
            'title': 'Music Events',
            'description': 'Discover amazing concerts, live performances, and musical experiences.',
            'image': '/static/images/music-banner.jpg'
        },
        'food': {
            'title': 'Food & Drink Events',
            'description': 'Explore culinary festivals, wine tastings, and foodie gatherings.',
            'image': '/static/images/food-banner.jpg'
        },
        'sports': {
            'title': 'Sports Events',
            'description': 'Join exciting sports tournaments, matches, and athletic competitions.',
            'image': '/static/images/sports-banner.jpg'
        },
        'education': {
            'title': 'Educational Events',
            'description': 'Attend workshops, seminars, and learning opportunities.',
            'image': '/static/images/education-banner.jpg'
        }
    }
    
    return render_template('category.html',
                         category=category,
                         info=category_info.get(category, {}),
                         ongoing_events=ongoing_events,
                         upcoming_events=upcoming_events,
                         past_events=past_events)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 