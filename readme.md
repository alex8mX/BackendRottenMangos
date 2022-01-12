# RottenMangos API
This is the Backend API for Rotten Mangos! The latest website to complain about movies!

## Installation

After cloning the repository, go to the directory and you will find the requirements.txt, which specifies which version and project you need to install in order for the API to work properly. Once installed, in the command prompt write: 

```bash
python manage.py runserver
```
Hit enter and the API will be up for use.
## Endpoints


In order to see the available endpoints, there are 2 urls included which will help you use this API.
```python
http://127.0.0.1:8000/swagger/
http://127.0.0.1:8000/redoc/
```
They show what parameters you will need in each and every endpoint. In addition to  those two, these are the rest of the endpoints that don't require authentication, which are the following:

```python
# Allows access to the admin pages, it will need a super user in order to login
http://127.0.0.1:8000/admin/

# Grants Authorization token 
http://127.0.0.1:8000/api-token-auth/

# Returns a list of currently registered users
http://127.0.0.1:8000/users/

# Allows you to create a new user(not a superuser) and it also returns its auth token
http://127.0.0.1:8000/users/create

# Retrieve the information of a single user
http://127.0.0.1:8000/users/
```
All other endpoints require authentication in order to use them.
## Authentication
As mentioned before, unless specified, every endpoint requires authentication to use. This API has token authentication, which means that every call needs this token in the header, here is an example of a curl:

```python
curl -X GET "http://127.0.0.1:8000/movies/" -H  "accept: application/json" -H  "Authorization: Token f0581fb71dc97ddbadac56afee886ebcec4fd451"
```
The header must have the key 'Authorization' and the value must be the capitalized word "Token" followed by a one whitespace and then auth token. This token can be obtained when you create a user in the create user endpoint or request a new auth token in the api-token-auth endpoint. You can generate a new token using the credentials of a newly created user or a superuser.

## Usage
Using the swagger or the redoc as tools, the API lets you use crud actions to movies, reviews, add movies to watchlists and it even gives an average rating to each movie according to its reviews. Naturally, you can't modify or delete reviews that aren't your own, same situation if you try to delete a movie in a watchlist of another user. 