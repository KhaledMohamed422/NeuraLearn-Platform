# User End-Points Authentication:

## Features
- Register
- Email active
- Login
- Send reset password
- Reset password
- Logout
- Get user info
- Change user info
- Change user password
- Get users info

## Installation steps

1. Ensure you have python3 installed
2. Clone the repository
3. create a virtual environment using `virtualenv venv`
4. Activate the virtual environment by running `source venv/bin/activate`
- On Windows use `source venv\Scripts\activate`
5. Install the dependencies using `pip install -r requirements.txt`
6. Make migration existing db tables by running `python manage.py makemigrations`
7. Migrate existing db tables by running `python manage.py migrate`
8. Run the django development server using `python manage.py runserver`

## End Points 
End Points  is accessible in /users/urls.py
## Run & Test 
- attach url patterns for evry endpoint to server url
- insert Json format in the Django rest framework inputs to get response 
# Json format for Endpoints

- ## `Creating a new user`
|Method|Endpoint|
|------|---|
|POST|`/auth/users/`| 

**Request:**
```
{"first_name": "","last_name": "","email": "", "password": "", "re_password": "" }
``` 
**Response:**
if error 
- `{"Error": "This email allredy exist"}`
- `{'ErrorPass': 'Your password must contain at least 8 characters.'}`
- `{'ErrorPass': 'Your password can’t be entirely numeric.'}`
- `{'ErrorPass': 'Your passwords not same!.'}`
  
if not error
- `{'email': email, 'first_name': first_name, 'last_name': last_name,'id': id}`
---

- #### `after registering the account is not activat and we will arrive for ueser on email included on uid and token , you will not be able to login you should activate your account by email check it and follow the link`

- ## `Activate`
|Method|Endpoint|
|------|---|
|POST|`/auth/users/activation/`

**Request:**
```
{"uid": "", "token": ""}
```

**Response:**

if error 
- `{"activated": 'Account activated successfully' }`
- if token is expired: `{'Expired': 'Please Create new cookie.'}`
---
- ## `User Login - Getting JWT Tokens`
|Method|End-Point|
|------|---|
|POST|`auth/jwt/create/`

**Request:**
```
{"email": "","password": ""}
```
**Response:**
if error 
`{"detail": "No active account found with the given credentials"}`

if not error 
`{'access': "", 'refresh': ""}`

- #### `tokens created with expired time 60 minutes.`

---

- # User
- ## `Get user info`
|Method|End-Point|
|------|---|
|GET|`auth/users/me`|

**Request**

`{"Authorization": "JWT <Token>"}`

**Response:**

`{"id": "", "email": "","first_name": "","last_name":  "" }`

---

- ## `Update user info`
|Method|End-Point|
|------|---|
|PUT|`auth/users/edit/me`|

**Request**

`- authenticated user token`
```
{ "email": "","first_name": "","last_name": "" }
```

**Response**
- `{'Error':'Should Login!'}`
- `{'Error': 'E-mail field is required.'}`
- `{'Error': 'first_name field is required.'}`
- `{'Error': 'last_name field is required.'}`
- `{'Error': 'This email allredy used'}`
- `{'email': ""'first_name':""'last_name':""}`
- `{'Expired': 'Please Create new cookie.'}`
- 
---------
