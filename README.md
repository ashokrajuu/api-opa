# Project: API calls with JWT Authentication and OPA Authorization

### Functionality:

- Users can log in to the application if the user exists
- Only Admin Role can create the user and view the available users
- Only Authenticated user can view the available users

### Technical Components:

- Flask is used to serve API calls.
- Sqlite DB is used to store the user information.
- JWT (Java Web Token)provides Authentication.
- OPA (Open Policy Agent) provides Authorization

### Working

- Creates a Flask application instance (app)
- Initializes and Define the sql(db), jwt and opa config
- Login function,
  - Receives all traffic and only existing users will be allowed
  - JWT token will be generated
  - View function,
  - JWT token is verified
  - OPA parses the role from token and authorization decision is taken
  - Result will be displayed
- Create function,
  - JWT token is verified
  - OPA parses the role from token and authorization decision is taken
  - User will be created in DB and indicated in logline

> Docker image will vary based on platform,
> If linux(amdx64x86), OPA Image: openpolicyagent/opa:edge-rootless and API Image: ashokrajume/api-opa:linux
> if Mac(arm),OPA Image: openpolicyagent/opa:edge-static and API Image: ashokrajume/api-opa:arm 

## Usage:

> Note: While Launching the Application Admin user will be created and config can be controlled via <helm>
> Replace other values accordingly, Explanation purpose using dummy values

**Login:**

Run the below command to log in to the api application,Role will be retained automatically from DB 

```
curl -X POST -H "Content-Type: application/json" -d '{"username": "admin", "password": "<password>", "email": "admin@email"}' http://127.0.0.1:5000/login
```

Stores the token generated for further purpose.

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

If normal users try to access create user API, ends up in Unauthorized error
![image](https://github.com/ashokrajuu/api-opa/assets/24654074/4d47eadd-dcef-4e46-9cc0-e47774ad970d)


## Setup

**Prerequisites**

- Minikube
- Docker
- kubectl

Api Docker Repo: https://hub.docker.com/repository/docker/ashokrajume/api-opa/general


### Install using Kubernetes

If you don't need customization, simply run

```
kubectl create -f deployment.yaml

kubectl port-forward service/release-name-helm-api-opa 5000:5000

curl http://127.0.0.1:5000
```

**Variable Configuration:**

`K8's` folder has config files (Modify accordingly)

-  api-config: Values of OPA URL (resolves using service DNS in macOS and for Linux expose the service & modify the url), Admin user info(created during initialization)
-  api-secret: JWT Secret token and Admin user password (encoded)
-  opa-policy: Allow and Deny policy based on role, Check `src\config\jwt.rego` 


**Running the application:**

Create configs and secrets,
```
kubectl create -f api-config.yaml
kubectl create -f api-secret.yaml
kubectl create -f opa-policy.yaml
```

Create OPA server and service,
```
kubectl create -f opa.yaml
```
Create (Flask)API server and service,
```
kubectl create -f api.yaml
```

Next,

Check whether pods are in running state,

```
kubectl get pods
```

Port-forward the API service,

```
kubectl port-forward service/api 5000:5000
```

**Testing:**

Using 'curl',

> curl http://127.0.0.1:5000

This will return 404 html response,as there are no api for path "/"

**Logs of API:**

> kubectl logs api-pod-name

![image](https://github.com/ashokrajuu/api-opa/assets/24654074/6ae66357-094d-4948-8ad3-b1e507c530ea)

For testing purpose, I'm printing some sensitive info logs.
Please modify the print statement accordingly in 'src/api/api.py' and create a new image with the Dockerfile provided


**Logs of OPA:**

> kubectl logs opa-pod-name

![image](https://github.com/ashokrajuu/api-opa/assets/24654074/aae993c7-9c2a-4b9e-bcd0-471e2e313062)


### Install using Helm

Validate template,

```
helm template helm-api-opa -f helm-api-opa/values.yaml
```
Install using Helm Chart,
```
helm install helm-api-opa-release helm-api-opa
```
```
kubectl port-forward service/helm-api-opa-release 5000:5000
```
upgrade,
```
helm upgrade helm-api-opa-release helm-api-opa
```

## Customization

Inside `src` folder, 

api folder has api logic
config folder has opa policy config (jwt.rego)

Modify the configuration and Recreate the Docker image,
```
docker build -t <name>:tag .
```
Move image inside the minikube docker by,
```
minikube image load <name>:tag 
```