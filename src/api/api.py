from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import requests
from functools import wraps
import os

#Flask Configuration

app = Flask(__name__)
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
OPA_URL = os.environ.get('OPA_URL')
DB_FILE_PATH = os.path.join(os.path.dirname(__file__), 'sqlite.db')  # SQLite database file path
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_FILE_PATH  # SQLite connection string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
jwt = JWTManager(app)
db = SQLAlchemy(app)

#OPA validation function and this is invoked by decorator
def authorize_request(method, path, jwt_token, JWT_SECRET_KEY, authenticated):
    print(method, path, jwt_token, JWT_SECRET_KEY, authenticated)

    payload = {
        "input": {
            "method": method,
            "jwt_token": jwt_token,
            "secret_jwt": JWT_SECRET_KEY,
            "path": path,
            "authenticated": authenticated
        }
    }

    response = requests.post(OPA_URL, json=payload)

    print("response", response)
    print("response", response.status_code)
    if response.status_code == 200:
        print(response.json())
        return response.json().get("result", False)
    else:
        # Handle OPA service error
        return False

#Decorator for OPA
def authorize(method, path):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            global authenticated
            current_user = get_jwt_identity()
            print(request)
            jwt_token = request.headers.get('Authorization')
            # Print the token
            print("JWT Token:", jwt_token)

            if jwt_token:
                authenticated = True

            claim = get_jwt()
            print("JWT claim:", claim["role"])

            print(current_user)
            user = User.query.filter_by(username=current_user).first()
            print(user.role)
            # authorization_result = check_authorization(method, path, {"authenticated": current_user is not None, user.role: "admin" if current_user and user.role in current_user else None})
            authorization_result = authorize_request(method, path, jwt_token, JWT_SECRET_KEY, authenticated)
            if not authorization_result:
                return jsonify({"msg": "Unauthorized"}), 403

            return func(*args, **kwargs)

        return wrapper

    return decorator


# Local DB Initialization
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(120), nullable=True)


# Create the database tables (run this once before starting the app)
with app.app_context():
    db.create_all()
    admin_user = User.query.filter_by(username='admin').first()
    if admin_user is None:
        # Create a new User instance with the provided values
        admin_user = User(username=os.environ.get('INITIAL_USERNAME'), email=os.environ.get('INITIAL_EMAIL'), password=os.environ.get('INITIAL_PASSWORD'), role=os.environ.get('INITIAL_ROLE'))
        db.session.add(admin_user)
        db.session.commit()
    users = User.query.all()
    user_list = [{'id': user.id, 'username': user.username, 'email': user.email, 'role': user.role} for user in users]
    print(user_list)

# Login function which allows all traffic
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not username or not password:
        return jsonify({"msg": "Missing username or password or email"}), 400

    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        access_token = create_access_token(identity=username,
                                           additional_claims={"role": user.role, "email": user.email})
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Invalid username or password"}), 401

# Create user function which allows only Admin Role authorized by OPA
@app.route('/create', methods=['POST'])
@jwt_required()
@authorize("POST", "/create")
def register():
    print("Authorized")

    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    print(request.json)
    print(request.json.get('username'))

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    role = request.json.get('role', None)
    email = request.json.get('email', None)

    if not username or not password or not role or not email:
        return jsonify({"msg": "Missing username or password or role or email"}), 400

    new_user = User(username=username, password=password, role=role, email=email)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msg": "User registered successfully"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"msg": "Username already exists"}), 400

# Create user function which allows if you are authenticated and authorized by OPA
@app.route('/view', methods=['GET'])
@jwt_required()
@authorize("GET", "/view")
def view():
    current_user = get_jwt_identity()

    users = User.query.all()
    user_list = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]

    return jsonify(logged_in_as=current_user, Users_List=user_list), 200


if __name__ == '__main__':
    app.run(debug=True)
