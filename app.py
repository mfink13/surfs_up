from flask import Flask

#create a new Flask app instance
app = Flask(__name__)

#create flask routes
@app.route('/')

#create a function called hello_world()
def hello_world():
    return 'Hello world'
# local host for output http://127.0.0.1:5000/

