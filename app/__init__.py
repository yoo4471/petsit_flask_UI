from flask import Flask

app = Flask(__name__)
from app import views
# from app import login
from . import function
from . import views

views.remove_DBfiles()
function.Make_db_member()
function.Make_db_house()
function.Make_db_pet()
function.Make_db_petsitter()
function.Make_db_image()
function.Make_db_tran()


views.loop_insert()
