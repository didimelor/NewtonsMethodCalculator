import sympy as sym
from sympy import *
import time
import numpy as np
from sympy.parsing.mathematica import mathematica
import random

x = sym.Symbol('x')
usrInput = "x**3"
expr = x**2
exprD = 2*x


def parse(usrInput):
    global expr
    usrInput = usrInput.replace("\\", "/")
    if(usrInput.find("Log" or "log") != -1):
        mathematica(usrInput)
    expr = parse_expr(usrInput)
    expr = simplify(expr)

def f(var):
    return expr.subs(x, var)

def df(x,f):
    h = .00001
    upper = f(x+h)
    lower = f(x)
    return (upper - lower) / h

def Validation(x,f):
    epsilon = .00001
    norm_fx = abs(f(x))
    if norm_fx < epsilon:
        return ["Correcto",1,norm_fx]
    else:
        return ["Incorrecto",0,norm_fx]

#Clase que guarda atrubutos de cada funcion insertada para verificar y validar el funcionamiento de la pagina
class function:
    def __init__(self, id, sol, it, t, acc, solved, message):
        self.id = id
        self.sol = sol
        self.it = it
        self.t = t
        self.acc = acc
        self.solved = solved #bool if solved
        self.message = message

def Solver11(x0,f):
    it = 0
    maxIt = 10000
    start = time.time()
    x_n  = x0
    x_n_1 = x_n + .01
    step = x_n_1-x_n
    while (abs(step) > 0.00001 and it < maxIt):
        it += 1
        denominator = df(x_n,f)
        if denominator != 0:
            function_result = f(x_n) 
            x_n_1 = x_n - function_result / denominator
        else:
            x_n = 0.0
            return function(usrInput, x_n, it, (round(time.time() - start,12)), 0.0, 0, "No solution found")

        step = x_n_1-x_n
        x_n = x_n_1
    if(it > maxIt):
        x_n = 0.0
        return function(usrInput, x_n, 0, (round(time.time() - start,12)), 0.0, 0, "No solution found")
    arr = Validation((round(x_n,12)), f)
    return function(usrInput, (round(x_n,12)), it, (round(time.time() - start,12)), (round(arr[2], 12)), 1, "Solved!")

'''
parse("3*(x)*(x)+4*(x)-10")
funcObj = Solver11(0.2,f)
print(funcObj.sol, funcObj.message)
'''
#Pruebas unitarias
def testSolver():
    functions = ["(x*x - 16)", 
                "cos(x)- x**3", 
                "x + 20",
                "sin(x) \ 20",
                "1.0 \ x",
                "x - cos(x)",
                "0.3**x-x**2+4",
                "2*cos(x)-(sqrt(x)/2)-1",
                "tan(x)",
                "x-cos(x)",
                "exp(0.3*x)-x**2+4",
                "2*cos(x)-(sqrt(x)/2)-1",
                "3*(x)*(x)+4*(x)-10"]
    for function in functions:
        parse(function)
        num = random.uniform(-1.0, 3.0)
        num = round(num,3)
        funcObj = Solver11(num,f)
        print(funcObj.message, ": " ,funcObj.sol, "x0: ", num)

parse("(2.718**(-0.005*x))*(1+0.005*x) - 0.5")
funcObj = Solver11(10,f)
print(funcObj.message, ": " ,funcObj.sol, ". Acc: ", funcObj.acc)

#(2.718**(-0.005*x))*(1+0.005*x) - 0.5
#(2.718**(x**2))-1