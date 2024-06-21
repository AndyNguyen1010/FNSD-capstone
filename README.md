# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.12

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server
To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.




### API DOCUMENTATION


##### Roles

Create two roles for users under `Users & Roles` section in Auth0
* Manage
	* All permissions 
* Barista
	* Can view actors and movies

### Login App
http://127.0.0.1:5000/login

http://a663da6d9ddfd4667885f6cbef6c1417-461432304.us-east-2.elb.amazonaws.com/login


### User Test

#### Manage role 
tannv20@udacity.com/Udacity@1235
#### Barista role
view_user@udacity.com/Udacity@1235

#### SwaggerUI
##### get token from `http://a663da6d9ddfd4667885f6cbef6c1417-461432304.us-east-2.elb.amazonaws.com/login`
after login

http://127.0.0.1:5000/apidocs
http://a663da6d9ddfd4667885f6cbef6c1417-461432304.us-east-2.elb.amazonaws.com/apidocs/


##### Permissions

Following permissions should be created under created API settings.

- `view:movies`
- `delete:movie`
- `update:movie`
- `post:movie`
- `delete:actor`
- `post:actor`
- `update:actor`
- `view:actors`

`GET '/movies'` 
- Fetches a set of questions,
- Require `view:movies` permission
- Returns: array movie
```json
	{
		"movies": [
			{
            "id": 2,
            "release_date": "Mon, 01 APR 2024 00:00:00 GMT",
            "title": "avatar"
         }
		],
		"success": true
    }
```

`DELETE '/movies/<int:id>'`

- Deletes a specified movie using the id of the movie
- Require `delete:movies` permission
- Request Arguments: `id` - integer
- Returns: success = true if delete success


`POST '/movies'`

- Sends a post request in order to add a new movie
- Requires `post:movies` permission
- Requires the title and release date.
- Request Body:

```json
{
   "release_date": "Mon, 01 APR 2024 00:00:00 GMT",
   "title": "avatar"
}
```
- Returns: return any new data if create success

`PATCH '/movies/<id>'`

- Sends a post request in order to update a exists movie
- Require `update:movies` permission
- Request Arguments: `id` - integer
- Request Body:

```json
{
   "release_date": "Mon, 01 APR 2024 00:00:00 GMT",
   "title": "avatar"
}
```

- Returns:
   - Responds with a 404 error if <id> is not found
   - Update the corresponding fields for Movie with id <id> and return new movie
	
 `GET '/actors'` 
- Fetches a set of questions,
- Require `view:actors` permission
- Returns: array actors
```json
	{
		"actors": [
			{
            {
               "age": 20,
               "gender": "M",
               "id": 1,
               "name": "Peter Pan"
            }  
         }
		],
		"success": true
    }
```

`DELETE '/actors/<int:id>'`

- Deletes a specified movie using the id of the movie
- Require `delete:actors` permission
- Request Arguments: `id` - integer
- Returns: success = true if delete success


`POST '/actors'`

- Sends a post request in order to add a new movie
- Requires `post:actors` permission
- Requires the title and release date.
- Request Body:

```json
{
	"age": 20,
	"gender": "M",
	"name": "Peter Pan"
}
```
- Returns: return any new data if create success

`PATCH '/actors/<id>'`

- Sends a post request in order to update a exists movie
- Require `update:actors` permission
- Request Arguments: `id` - integer
- Request Body:
```json
{
	"age": 20,
	"gender": "M",
	"name": "Peter Pan"
}
```
- Returns:
   - Responds with a 404 error if <id> is not found
   - Update the corresponding fields for Movie with id <id> and return new movie
	
 ## Testing
To run the tests, run
```
python test_app.py
```