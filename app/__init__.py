from flask import Flask

app = Flask(__name__)
from app import views
# from app import login
from . import function

function.Make_db()
function.Make_db_house()
function.Make_db_pet()
