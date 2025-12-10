import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)

# --- HYBRID DATABASE CONFIGURATION ---
# 1. Check if running on a server (Production)
database_url = os.environ.get('DATABASE_URL')

if database_url:
    # Fix for cloud providers using postgres://
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # 2. Local development fallback (SQLite)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

# --- DATABASE MODELS ---
class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=False)

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    designation = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)

class ContactQuery(db.Model):
    __tablename__ = 'contact_queries'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Subscriber(db.Model):
    __tablename__ = 'subscribers'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)

# --- INITIALIZATION ---
with app.app_context():
    db.create_all()

# --- ROUTES: PAGES ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

# --- ROUTES: API ---
@app.route('/api/projects', methods=['GET', 'POST'])
def handle_projects():
    if request.method == 'POST':
        name = request.form['name']
        desc = request.form['description']
        image = request.files['image']
        
        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_project = Project(name=name, description=desc, image_url=filename)
            db.session.add(new_project)
            db.session.commit()
            return jsonify({'message': 'Project added!'}), 201
            
    projects = Project.query.all()
    output = [{'id': p.id, 'name': p.name, 'description': p.description, 'image': p.image_url} for p in projects]
    return jsonify(output)

@app.route('/api/clients', methods=['GET', 'POST'])
def handle_clients():
    if request.method == 'POST':
        name = request.form['name']
        desc = request.form['description']
        designation = request.form['designation']
        image = request.files['image']
        
        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_client = Client(name=name, description=desc, designation=designation, image_url=filename)
            db.session.add(new_client)
            db.session.commit()
            return jsonify({'message': 'Client added!'}), 201

    clients = Client.query.all()
    output = [{'id': c.id, 'name': c.name, 'description': c.description, 'designation': c.designation, 'image': c.image_url} for c in clients]
    return jsonify(output)

@app.route('/api/contact', methods=['GET', 'POST'])
def handle_contact():
    if request.method == 'POST':
        data = request.json
        new_contact = ContactQuery(
            full_name=data['full_name'],
            email=data['email'],
            mobile=data['mobile'],
            city=data['city']
        )
        db.session.add(new_contact)
        db.session.commit()
        return jsonify({'message': 'Query received!'}), 201
        
    contacts = ContactQuery.query.order_by(ContactQuery.timestamp.desc()).all()
    output = [{'full_name': c.full_name, 'email': c.email, 'mobile': c.mobile, 'city': c.city} for c in contacts]
    return jsonify(output)

@app.route('/api/subscribe', methods=['GET', 'POST'])
def handle_subscribe():
    if request.method == 'POST':
        data = request.json
        if not Subscriber.query.filter_by(email=data['email']).first():
            new_sub = Subscriber(email=data['email'])
            db.session.add(new_sub)
            db.session.commit()
        return jsonify({'message': 'Subscribed!'}), 201
        
    subs = Subscriber.query.all()
    output = [{'email': s.email} for s in subs]
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True, port=5000)