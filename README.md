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

## Installation With Docker
1. Clone the repository
2. Run the following command to start the Docker containers `docker-compose up`
3. Apply the migrations to the database `docker compose exec web python /code/manage.py migrate`
4. Load some initial data `docker compose exec web python /code/manage.py loaddata subjects.json`
5. Access the app at [http://localhost:8000](http://localhost:8000)

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

- ## `Creating a course`
|Method|Endpoint|
|------|---|
|POST|`/api/courses/create/`| 


**Request**
```json
{
  "subject": 1, // Required
  "title": "Introduction to Programming", // Required
  "overview": "A comprehensive course on programming  concepts.",  // Required
  "price": 29.99,  // Required
  "image": "image"  // Optional 
}
```

**Response**
* A course object response with a 200 OK status.

* Errors
    - `{'detail': 'Authentication credentials were not provided.'} 403`
    - `{'detail': 'You do not have permission to perform this action.'} 403`
    - `{'subject': ['Incorrect type. Expected pk value, received str.']}`
    - `{'subject': ['Invalid pk - object does not exist.']} 400` 
    - `{'subject': ['This field may not be null.'] 400`
    - `{'title': ['This field may not be blank.']} 400`
    - `{'title': ['Ensure this field has no more than 200 characters.']} 400`
    - `{'overview': ['Ensure this field has no more than 5000 characters.']}`
     - `{'overview': ['This field may not be blank.']} 400`
    - `{'price': ['Ensure that there are no more than 10 digits in total.']} 400`
    - `{'price': ['A valid number is required.']} 400`
    - `"{image": [ "Upload a valid image. The file you uploaded was either not an image or a corrupted image."]}`
-----
- ## `Instructor List My courses`
|Method|Endpoint|
|------|---|
|GET|`/api/courses/mine/?limit=x&offset=x`|


**Request**
- No request body is required for this endpoint.

**Response**

* A list of courses owned by the authenticated instructor with a 200 OK status.

* Example 
```json
{
  "count": 19,
  "next": null,
  "previous": "previous": "http:/localhost:8000/api/courses/mine/?limit=10",
  "results": [
    {
      "subject": "Programming",
      "title": "dsafdf",
      "slug": "dsafdf-l4nn",
      "overview": "sdfs",
      "price": "1.00",
      "image": null,
      "created": "2024-03-08T13:16:41.088005Z",
      "updated": "2024-03-08T13:16:41.088141Z",
      "detail_url": "http://localhost:8000/api/courses/dsafdf-l4nn/detail/",
      "edit_url": "http://localhost:8000/api/courses/dsafdf-l4nn/edit/",
      "delete_url": "http://localhost:8000/api/courses/dsafdf-l4nn/delete/",
      "modules_url": "http://localhost:8000/api/courses/dsafdf-l4nn/modules/"
    },
    // ... additional course objects
  ]
}

```
* Errors
    - `{'detail': 'Authentication credentials were not provided.'} 403`
    - `{'detail': 'You do not have permission to perform this action.'} 403`
-------
- ## `Course Detail`
|Method|Endpoint|
|------|---|
|GET|`/api/courses/<slug>/detail/`|

**Response**
* A course object response with a 200 OK status.
* Errors
    - `{'detail': 'Authentication credentials were not provided.'} 403`
    - `{'detail': 'You do not have permission to perform this action.'} 403`
    - `{'detail': 'Not found.'} 404`
---------
- ## `Instructor edit course`
|Method|Endpoint|
|------|---|
|PUT|`/api/courses/<slug>/edit/`|

**Response**
* A course object response with a 200 OK status.
* Errors
    - `{'detail': 'Authentication credentials were not provided.'} 403`
    - `{'detail': 'You do not have permission to perform this action.'} 403`
    - `{'detail': 'Not found.'} 404`
    - `{'subject': ['Incorrect type. Expected pk value, received str.']}`
    - `{'subject': ['Invalid pk - object does not exist.']} 400` 
    - `{'subject': ['This field may not be null.'] 400`
    - `{'title': ['This field may not be blank.']} 400`
    - `{'title': ['Ensure this field has no more than 200 characters.']} 400`
    - `{'overview': ['Ensure this field has no more than 5000 characters.']}`
     - `{'overview': ['This field may not be blank.']} 400`
    - `{'price': ['Ensure that there are no more than 10 digits in total.']} 400`
    - `{'price': ['A valid number is required.']} 400`
    - `{image": [ "Upload a valid image. The file you uploaded was either not an image or a corrupted image."]}`
-----------
- ## `Instructor delete course`
|Method|Endpoint|
|------|---|
|DELETE|`/api/courses/<slug>/delete/`|

**Response**
* A Empty Response 200 OK status.
* Errors
    - `{'detail': 'Authentication credentials were not provided.'} 403`
    - `{'detail': 'You do not have permission to perform this action.'} 403`
    - `{'detail': 'Not found.'} 404`

--------------
- ## `List Modules Of a Course`
|Method|Endpoint|
|------|---|
|GET|`/api/courses/<slug>/modules/`|

**Response**
* A course object with modules response with a 200 OK status.

* Example
    ```json
    {
        "title": "dsafdf",
        "create_new_module_url": "http://localhost:8000/api/courses/dsafdf-ez8o/module/create/",
        "modules": [
            {
                "title": "first module",
                "description": "this is module",
                "slug": "first-module",
                "edit_url": "http://localhost:8000/api/courses/module/first-module/update/",
                "delete_url": "http://localhost:8000/api/courses/module/first-module/delete/",
                "contents_url": "http://localhost:8000/api/courses/module/first-module/contents/"
            },
            {
                "title": "another module",
                "description": "this is another module",
                "slug": "another-module",
                "edit_url": "http://localhost:8000/api/courses/module/another-module/update/",
                "delete_url": "http://localhost:8000/api/courses/module/another-module/delete/",
                "contents_url": "http://localhost:8000/api/courses/module/another-module/contents/"
            }
        ]
    } 
    ```
* Errors
    - `{'detail': 'Authentication credentials were not provided.'} 403`
    - `{'detail': 'You do not have permission to perform this action.'} 403`
    - `{'detail': 'Not found.'} 404`
-----------
- ## `Create New Module Of a Course`
|Method|Endpoint|
|------|---|
|POST|`/api/courses/<slug:slug>/module/create/`|

**Request**
```json
{
  "title": "Introduction to Programming", // Required
  "description": "A comprehensive course on programming  concepts.",  // Optional
}
```
* Errors
    - `{'detail': 'Authentication credentials were not provided.'} 403`
    - `{'detail': 'You do not have permission to perform this action.'} 403`
    - `{'title': ['This field may not be blank.']} 400`
    - `{'title': ['Ensure this field has no more than 200 characters.']} 400`
    - `{'Description': ['Ensure this field has no more than 5000 characters.']}`
------------
- ## `Edit Module Of a Course`
|Method|Endpoint|
|------|---|
|PUT|`/api/courses/module/<slug:slug>/update/`|

**Request**
```json
{
  "title": "Introduction to Programming", // Required
  "description": "A comprehensive course on programming  concepts.",  // Optional
}
```
* Errors
    - `{'detail': 'Authentication credentials were not provided.'} 403`
    - `{'detail': 'You do not have permission to perform this action.'} 403`
    - `{'detail': 'Not found.'} 404`
    - `{'title': ['This field may not be blank.']} 400`
    - `{'title': ['Ensure this field has no more than 200 characters.']} 400`
    - `{'Description': ['Ensure this field has no more than 5000 characters.']}`
-----------
- ## `Delete Module Of a Course`
|Method|Endpoint|
|------|---|
|DELETE|`/api/courses/module/<slug:slug>/delete/`|

**Request**

* Errors
    - `{'detail': 'Authentication credentials were not provided.'} 403`
    - `{'detail': 'You do not have permission to perform this action.'} 403`
    - `{'detail': 'Not found.'} 404`
----------
- ## `List Content Of a Module`
|Method|Endpoint|
|------|---|
|GET|`/api/courses/module/<slug>/contents/`|

**Response**
* A Module object with its contents response with a 200 OK status.

* Example
    ```json
    {
    "title": "sdfads",
    "add_text_url": "http://localhost:8000/api/courses/module/sdfads/content/text/create/",
    "add_file_url": "http://localhost:8000/api/courses/module/sdfads/content/file/create/",
    "add_image_url": "http://localhost:8000/api/courses/module/sdfads/content/image/create/",
    "add_video_url": "http://localhost:8000/api/courses/module/sdfads/content/video/create/",
    "contents": [
        {
            "text": {
                "title": "asdf",
                "content": "asdf",
                "edit_url": "http://localhost:8000/api/courses/module/content/text/480d7e96-9d36-43d0-9d01-5c9a6491e72e/",
                "delete_url": "http://localhost:8000/api/courses/module/content/text/480d7e96-9d36-43d0-9d01-5c9a6491e72e/"
            }
        },
        {
            "image": {
                "title": "this is image content",
                "file": "http://localhost:8000/media/images/2024/03/09/test.jpg",
                "edit_url": "http://localhost:8000/api/courses/module/content/image/7882e2b7-9024-4e96-8d2d-61c295c06275/",
                "delete_url": "http://localhost:8000/api/courses/module/content/image/7882e2b7-9024-4e96-8d2d-61c295c06275/"
            }
        }
    ]
    }
    ```
* Errors
    - `{'detail': 'Authentication credentials were not provided.'} 403`
    - `{'detail': 'You do not have permission to perform this action.'} 403`
    - `{'detail': 'Not found.'} 404`

------------
- ## `Create New Content Of a Module`
|Method|Endpoint|
|------|---|
|POST|`/api/courses/module/<module_slug>/content/<content_name>/create/`|

**Request**
* For text
    ```json
    {
    "title": "Introduction to Programming", // Required
    "content": "A comprehensive course on programming  concepts.",  // Required
    }
    ```
* For file
    ```json
    {
    "title": "Introduction to Programming", // Required
    "file": "file",  // Required
    }
    ```
* For image
    ```json
    {
    "title": "Introduction to Programming", // Required
    "file": "image",  // Required
    }
    ```
* For video
    ```json
    {
    "title": "Introduction to Programming", // Required
    "file": "video",  // Required
    }
    ```
* Errors
    - `{'detail': 'Authentication credentials were not provided.'} 403`
    - `{'detail': 'You do not have permission to perform this action.'} 403`
    - `{'title': ['This field may not be blank.']} 400`
    - `{'title': ['Ensure this field has no more than 200 characters.']} 400`
    - `{'content': ['Ensure this field has no more than 5000 characters.']} 400`
    - `{"file": ["File extension “XY” is not allowed. Allowed extensions are: mp4."]} 400`
    - `{"file": ["File extension “XY” is not allowed. Allowed extensions are: jpeg."]} 400`
---------
- ## `Edit Content`
|Method|Endpoint|
|------|---|
|PUT|`/api/courses/module/content/<content_name>/uuid/`|

**Request**
Same request of creation

* Errors
    same errors of create content
------------
- ## `Delete Content`
|Method|Endpoint|
|------|---|
|DELETE|`/api/courses/module/content/<content_name>/uuid/`|

- ## `List available courses in to public (without authentication)`
|Method|Endpoint|
|------|---|
|GET|`/api/public/courses/?limit=2&offset=2`|


**Request**
- No request body is required for this endpoint.

**Response**

* A list of avaliable with a 200 OK status.

* Example 
```json
{
    "count": 5,
    "next": "http://localhost:8000/api/public/courses/?limit=2&offset=4",
    "previous": "http://localhost:8000/api/public/courses/?limit=2",
    "results": [
        {
            "subject": "Programming",
            "title": "dsafdf",
            "image": null,
            "instructor": "mahmoud",
            "slug": "dsafdf-tbvv",
            "overview": "sdfs",
            "price": "1.00",
            "detail_url": "http://localhost:8000/api/public/course/dsafdf-tbvv/detail/"
        },
        {
            "subject": "Programming",
            "title": "dsafdf",
            "image": null,
            "instructor": "mahmoud",
            "slug": "dsafdf-xlzq",
            "overview": "sdfs",
            "price": "1.00",
            "detail_url": "http://localhost:8000/api/public/course/dsafdf-xlzq/detail/"
        }
    ]
}
```
-------
- ## `List available courses in to public (without authentication) filter with subject`
|Method|Endpoint|
|------|---|
|GET|`/api/public/subject/<slug:subject>/?limit=2&offset=2`|


**Request**
- No request body is required for this endpoint.

**Response**

* A list of avaliable filtered with subject with a 200 OK status.

* Example 
```json
{
    "count": 5,
    "next": "http://localhost:8000/api/public/courses/?limit=2&offset=4",
    "previous": "http://localhost:8000/api/public/courses/?limit=2",
    "results": [
        {
            "subject": "Programming",
            "title": "dsafdf",
            "image": null,
            "instructor": "mahmoud",
            "slug": "dsafdf-tbvv",
            "overview": "sdfs",
            "price": "1.00",
            "detail_url": "http://localhost:8000/api/public/course/dsafdf-tbvv/detail/"
        },
        {
            "subject": "Programming",
            "title": "dsafdf",
            "image": null,
            "instructor": "mahmoud",
            "slug": "dsafdf-xlzq",
            "overview": "sdfs",
            "price": "1.00",
            "detail_url": "http://localhost:8000/api/public/course/dsafdf-xlzq/detail/"
        }
    ]
}
```
-------

- ## `See course detail`
|Method|Endpoint|
|------|---|
|GET|`/api/public/course/<course_slug>/detail/`|


**Request**
- No request body is required for this endpoint.

**Response**

* A detail of Course with 200 OK status.

* Example 
```json
{
    "title": "dsafdf",
    "overview": "sdfs",
    "image": null,
    "price": "1.00",
    "instructor": "mahmoud",
    "enrollments": 1,
    "updated": "2024-03-13T08:08:10.279792Z",
    "modules": [
        {
            "title": "module",
            "description": "moduel",
            "slug": "module",
            "contents": [
                {
                    "text": {
                        "title": "dsfasd f"
                    }
                },
                {
                    "file": {
                        "title": "this is file"
                    }
                },
                {
                    "file": {
                        "title": "sdf"
                    }
                },
                {
                    "image": {
                        "title": "image"
                    }
                },
                {
                    "video": {
                        "title": "dsaf"
                    }
                }
            ]
        },
        {
            "title": "module 2",
            "description": "moduel 2",
            "slug": "module-2",
            "contents": []
        }
    ]
}
```
-------