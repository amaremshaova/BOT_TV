from sqlalchemy import create_engine
import os.path
from sqlalchemy.orm import sessionmaker
import json 

with open(os.path.dirname(os.path.realpath(__file__)) + '\\data_connection.json', 'r', encoding = 'utf-8') as file_json:
    data = json.load(file_json)
    
engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(data['user'],data['password'],data['host'],data['port'],data['database']))

Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()
