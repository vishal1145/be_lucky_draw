from flask.cli import FlaskGroup
from wsgi import app
from app import db

cli = FlaskGroup(app=app)

if __name__ == '__main__':
    cli() 