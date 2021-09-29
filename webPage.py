from flask import Flask, render_template, redirect, url_for, request, jsonify
import requests
from flask_restful import Resource, Api, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from Solver import *
from sqlalchemy.sql import func
import json

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

BASE = "http://127.0.0.1:5000/"

class FunctionModel(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    expres = db.Column(db.String(100), nullable=False)
    solution = db.Column(db.Float, nullable=True)
    iterations = db.Column(db.Integer, nullable=False)
    t = db.Column(db.Float, nullable=False)
    accuracy = db.Column(db.Float, nullable=True)
    solved = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Solve(solution = {solution}, expres{expres}, iterations = {iterations}, t = {t}, accuracy = {accuracy}, solved = {solved}, message = {message})"

db.create_all() #Just one time to not override
resource_fields = {
    'id': fields.Integer,
    'expres': fields.String,
    'solution': fields.Float,
    'iterations': fields.Integer,
    't': fields.Float,
    'accuracy': fields.Float,
    'solved': fields.Integer,
    'message': fields.String
} 

class Solve(Resource):
    @marshal_with(resource_fields)
    def put(self, x0, func):
        parse(func)
        fObj = Solver11(x0,f)
        print(func)
        function = FunctionModel(expres=func, solution=fObj.sol, iterations=fObj.it, t=fObj.t, accuracy=fObj.acc, solved=fObj.solved, message=fObj.message)
        db.session.add(function)
        db.session.commit()
        return function, 201

class GetResponse(Resource):
    @marshal_with(resource_fields)
    def get(self, func):
        result = FunctionModel.query.filter_by(expres=func)
        m = "No se encontro ninguna funcion con esa id " + func
        if not result:
            abort(404, message=m)
        return result

class GetStats(Resource):
    def get(self):
        sol = FunctionModel.query.filter_by(solved=1).count()
        notSol = FunctionModel.query.filter_by(solved=0).count()
        itSum = FunctionModel.query.with_entities(func.avg(FunctionModel.iterations)).filter(FunctionModel.solved == 1).all()
        t = FunctionModel.query.with_entities(func.avg(FunctionModel.t)).filter(FunctionModel.solved == 1).all()
        acc = FunctionModel.query.with_entities(func.avg(FunctionModel.accuracy)).filter(FunctionModel.solved == 1).all()
        if (not sol or not notSol):
            abort(404, message="No se encontraron estadisticas")
        solPer = (sol / (sol + notSol)) * 100
        return {"Estadisticas": [
            {"Porcentaje resuelto": str(round(solPer, 2)) + '%'},
            {"Iteraciones en promedio para resolver": str(itSum)},
            {"Tiempo en promedio para resolver": str(t)},
            {"Precision en promedio": str(acc)}
            ]}

api.add_resource(Solve, "/solve/<float:x0>/<string:func>")
api.add_resource(GetResponse, "/solve/<string:func>")
api.add_resource(GetStats, "/getStats")

#Mostrar resultados con un get a la base de datos
@app.route("/", methods = ["PUT", "GET", "POST"])
def Home():
    if request.method == "POST":
        eq = request.form["eq"]
        x0 = request.form["x0"]
        return redirect(url_for("solving", x0=x0, func=eq))
    else:
        return render_template("home.html")

#Post funciones a la base de datos
@app.route("/solve/<float:x0>/<string:func>", methods = ["PUT", "GET", "POST"])
def solving(x0, func):
    response = requests.put(BASE + "solve/" + str(x0) + "/" + func) #Se manda la ecuación al solver
    jsonStr = json.dumps(response.json()) #La respuesta regresa en json y la convertimos a diccionario
    data = json.loads(jsonStr)
    if data["message"] == "No solution found": #Cuando no se encontro solucion
        return render_template("res.html", message=data["message"],func=func, resultado="no hay", p=data["accuracy"], id=data["id"], it=data["iterations"], t=data["t"]) #El objeto que se regresa del solver se muestra en el template con un resultado de que no hay solucion
    return render_template("res.html", message=data["message"], func=func, resultado=data["solution"], p=data["accuracy"], id=data["id"], it=data["iterations"], t=data["t"])#El objeto se muestra con su solucion

@app.route("/solve/<string:func>", methods = ["GET"])
def showFunc(func):
    response = requests.get(BASE + "/solve/" + func)
    return render_template("res.html", func=response)

#Estadisticas de la efectividad del solver con las funciones ingresadas
@app.route("/getStats", methods = ["GET"])
def showStats():
    response = requests.get(BASE + "/getStats")
    return render_template("stats.html", solved=response)

if __name__ == '__main__':
    app.run(debug=False)