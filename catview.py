from flask import Flask, Blueprint
from catprofile import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)