from flask import Flask,Blueprint,render_template

login = Blueprint('login',__name__)

app = Flask(__name__,static_url_path='/static')
app.config['SECRET_KEY'] = 'lasklskal'