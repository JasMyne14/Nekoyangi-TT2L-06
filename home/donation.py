from flask import Flask,Blueprint,render_template

donation = Blueprint('donation',__name__)

app = Flask(__name__,static_url_path='/static')
app.config['SECRET_KEY'] = 'love'