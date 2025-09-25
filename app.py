from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/postgres')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define a simple model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/users')
def get_users():
    users = User.query.all()
    result = [{"id": user.id, "name": user.name} for user in users]
    return jsonify(result)

@app.route('/init-db')
def init_db():
    db.create_all()
    # Add a sample user if none exists
    if User.query.count() == 0:
        sample_user = User(name="Sample User")
        db.session.add(sample_user)
        db.session.commit()
    return 'Database initialized!'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
