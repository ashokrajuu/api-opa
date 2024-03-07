# Project: API calls with JWT Authentication and OPA Authorization

### Functionality:

- User can login to the app if the user exists
- Only Admin Role user can create the user and view the user created
- Only Authenticated user canview the users available

### Technical Components:

- Flask is used to serve API calls
- Sqllite DB is used to store the user info
- JWT provides authentication
- OPA provides Authorization

### Working

- Creates a Flask application instance (app)
- Initializes and Define the sql(db), jwt and opa config
- Login function,
  - Recieves all traffic and only existing users will be allowed
  - JWT token will be generated
- View function,
  - JWT token is verified
  - OPA parses the role from token and authroization decision is taken
  - Result will be dispalyed
- Create function,
  - JWT token is verified
  - OPA parses the role from token and authroization decision is taken
  - User will be created in DB and indicated in logline


## Usage:

> Note: While Launching the Application Admin user will be created and config can be controlled via <helm>
> Replace other values accordingly, Explaination purpose using dummy values

**Login:**

Run the below command to login to the api application,Role will be reatined automatically from DB 

```
curl -X POST -H "Content-Type: application/json" -d '{"username": "admin", "password": "<password>", "email": "admin@email"}' http://127.0.0.1:5000/login
```

Store the token generated for further purpose

![image](https://github.com/ashokrajuu/api-opa/assets/24654074/b92935d3-a9ce-4b38-848b-fa33b0f1a5fc)


**Create User:**

Command to create user,

```
curl -X POST -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"username": "test12", "password": "admin", "test": "test", "email": "test12@email"}' http://127.0.0.1:5000/create
```

![image](https://github.com/ashokrajuu/api-opa/assets/24654074/568e5ed0-6871-4183-853a-996d894ad490)

**View Users List:**

Command to view user,

```
curl -X GET -H "Authorization: Bearer <token>" http://127.0.0.1:5000/view
```

![image](https://github.com/ashokrajuu/api-opa/assets/24654074/aaf0f6b8-81f7-465b-8b9f-dc1bcaa7a05e)

**Authorized for Admin Role:**
- Login
- Create User
- View User List


**Authorized for other Role and users existing:**
- Login
- View User List

If normal users try to access create user api, ends up in Unauthorized error
![image](https://github.com/ashokrajuu/api-opa/assets/24654074/4d47eadd-dcef-4e46-9cc0-e47774ad970d)


## Setup

**Pre-Requesites:**

- Minikube
- Docker

Api Docker Repo: https://hub.docker.com/repository/docker/ashokrajume/api-opa/general

**Variable Configuration:**


**Running the application:**




