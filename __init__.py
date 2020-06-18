from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = '9486d71d0200e64548be400cb72e4700'

from Calender import routes