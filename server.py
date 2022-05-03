"""Server for Wanderlust app."""

from flask import (Flask, render_template, request, redirect, session, flash)
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = ""
app.jinja_env.undefined = StrictUndefined

# Complete routes and view functions



if __name__ == "__main__":

    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)