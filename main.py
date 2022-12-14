import datetime
import sqlalchemy as db
from flask import Flask, request
import json
from sqlalchemy import Integer, ForeignKey, String, Column, REAL, DateTime, Text, text
from sqlalchemy.orm import sessionmaker
from Models import *
from flask_swagger_ui import get_swaggerui_blueprint

engine = db.create_engine('postgresql+psycopg2://postgres:miku@localhost/lab2')

conn = engine.connect()

app = Flask(__name__)

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Seans-Python-Flask-REST-Boilerplate"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime.date):
            return (str(z))
        else:
            return super().default(z)



Session = sessionmaker(bind=engine)
session = Session()

models = {
    "Employees": Employees,
    "Address": Address,
    "Post": Post,
    "Order": Order,
    "Ingredient": Ingredient,
    "Unit": Unit,
    "Provider": Provider,
    "Product": Product,
    "Snack": Snack,
    "Drink": Drink,
    "DrinkOrder": DrinkOrder,
    "SnackOrder": SnackOrder,
    "City": City,
    "BankDetail": BankDetail
}

def query_list(class_, data):
    if data["StartId"] != -1:
        query = session.query(class_).filter(class_.id > data["StartId"]).order_by(class_.id)
    elif data["EndId"] != -1:
        query = session.query(class_).filter(class_.id < data["EndId"]).order_by(-class_.id)
    else:
        query = session.query(class_)

    if len(data["Condition"]) != 0:
        query = query.filter(text(data["Condition"]))

    if data["Count"] > 0:
        query = query.limit(data["Count"])

    result = []

    for entity in query:
        result.append(entity.to_json())
    return json.dumps(result)


def get_by_id(class_, id_):
    obj = session.query(class_).get(id_)
    return json.dumps(obj.to_json())


def upsert_entity(class_, data):
    obj = class_(data, session)
    if obj.id == -1:
        obj.id = None
    if obj.id is None:
        session.add(obj)
    else:
        session.merge(obj)

    session.commit()

    return str(obj.id)


def delete_entity(class_, id_):
    session.query(class_).filter(class_.id == id_).delete()


@app.route("/api/list")
def get_list():
    data = request.get_json()

    if data["Table"] in models:
        return query_list(models[data["Table"]], data)
    return json.dumps([])


@app.route("/api/get")
def get_entity():
    entity_id = int(request.args.get("id"))

    if request.args.get("table") in models:
        return get_by_id(models[request.args.get("table")], entity_id)
    return json.dumps({})


@app.route("/api/upsert", methods=["POST"])
def upsert():
    data = request.get_json()
    if request.args.get("table") in models:
        return upsert_entity(models[request.args.get("table")], data)
    return "0"


@app.route("/api/delete", methods=["POST"])
def delete():
    entity_id = int(request.args.get("id"))
    if request.args.get("table") in models:
        delete_entity(models[request.args.get("table")], entity_id)
    return ""
