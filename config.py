import os
from dotenv import load_dotenv
from database import BaseCRUD 

load_dotenv()
# config


TOKEN = os.environ.get('TOKEN') # .env: TOKEN=********-*******

db_name = 'database/database.db'
users = BaseCRUD(db_name, 'users')
tests = BaseCRUD(db_name, 'tests')

steps = {
    'main_menu': 0,
    'new_quiz_title': 1,
    'new_quiz_description': 2,
    'new_quiz_file':3,
    
}