from flask import Flask, request, jsonify,session
import logging

from flask_migrate import Migrate
from models import db, bcrypt, PetOwner, PetSitter
from datetime import date

from flask_cors import CORS

app = Flask(__name__)
# CORS(app, origins=["http://localhost:3000"])

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

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


@app.route('/login', methods=['POST'])
def login():
  try:
    data = request.get_json()
    user_name = data.get('user_name')
    password = data.get('password')


    if not all([user_name, password]):
        return jsonify({'error': 'All fields are required'}), 400
    user = PetOwner.query.filter(PetOwner.user_name==user_name).first()
    if user and user.check_password(password):
       session['user_id'] = user.id
       return jsonify({'message': 'Successful login.'}), 200
    return jsonify({'error': 'Username or password not found.'}), 400
  except Exception as e:
     logging.error(f'An error occurred during login: {e}')
     return jsonify({'error': 'Network or server error.'}), 500

   

# @app.route('/login', methods=['POST'])
# def login():
#     try:
#         data = request.get_json()
#         user_name = data.get('user_name')
#         password = data.get('password')

#         if not all([user_name, password]):
#             return jsonify({'error': 'All fields are required'}), 400
        
#         user = PetOwner.query.filter(PetOwner.user_name == user_name).first()

#         if user:
#             logging.info(f"User found: {user.user_name}")
#             if user.check_password(password):
#                 session['user_id'] = user.id
#                 return jsonify({'message': 'Successful login.'}), 200
#             else:
#                 logging.error(f"Password mismatch for user: {user_name}")
#                 return jsonify({'error': 'Username or password not found.'}), 400
#         else:
#             logging.error(f"User not found: {user_name}")
#             return jsonify({'error': 'Username or password not found.'}), 400
#     except Exception as e:
#         logging.error(f'An error occurred during login: {e}')
#         return jsonify({'error': 'Network or server error.'}), 500

    
@app.route('/sitters')
def sitters():
   
   pet_sitters = PetSitter.query.all()
   if not pet_sitters:
      return jsonify({'error': 'Pet sitters not found.'}), 400
   return jsonify([sitter.to_dict() for sitter in pet_sitters]), 200

   
@app.route('/sitters/<int:id>')  
def sitter(id):
   pet_sitter = PetSitter.query.filter(PetSitter.id==id).first()
   if not pet_sitter:
      return jsonify({'error': 'Pet sitter not found'}), 400
   return jsonify(pet_sitter.to_dict()), 200
  

# if __name__ == "__main__":
#     app.run(debug=True, port=5000)


if __name__ == '__main__':
    with app.app_context():
        for rule in app.url_map.iter_rules():
            print(rule)
    app.run(debug=True)
