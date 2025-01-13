from flask import Flask, request, jsonify,session
import logging

from flask_migrate import Migrate
from models import db, bcrypt, PetOwner
from datetime import date

from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)
bcrypt.init_app(app)

migrate = Migrate(app, db)  
app.config['DEBUG'] = True



@app.route("/")
def home():
    return "Welcome to the Pet Sitter app!"


@app.route('/signup', methods=['POST'])
def signup():
  try:
    data = request.get_json()
    user_name = data.get('user_name')
    password = data.get('password')

    confirm_password = data.get('confirm_password')


    if not all([user_name, password, confirm_password]):
        return jsonify({'error': 'All fields are required'}), 400
    if PetOwner.query.filter(PetOwner.user_name == user_name).first():
        return jsonify({'error': 'Username already exists. Please choose another one.'}), 400
    if password != confirm_password:
       return jsonify({'error': 'Passwords do not match'}), 400
    
    new_user = PetOwner(
        user_name = user_name,
        password = password
    )

    db.session.add(new_user)
    db.session.commit()


    session['user_id'] = new_user.id
    return jsonify({'message': 'Successful signup.'}), 201
  except Exception as e:
     logging.error(f'An error occurred during signup: {e}')
     return jsonify({'error': 'Server or network error.'}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)


