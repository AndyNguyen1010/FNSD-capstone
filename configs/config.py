import os
from dotenv import load_dotenv,find_dotenv

env_file = find_dotenv(f'.env.{os.getenv("ENV", "development")}')
load_dotenv(env_file) 

DATABASE_URL = os.environ.get('DATABASE_URL')

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
API_AUDIENCE = os.environ.get("API_AUDIENCE") 
AUTH0_CLIENT_ID= os.environ.get("AUTH0_CLIENT_ID") 
AUTH0_CLIENT_SECRET= os.environ.get("AUTH0_CLIENT_SECRET") 
APP_SECRET_KEY= os.environ.get("APP_SECRET_KEY") 