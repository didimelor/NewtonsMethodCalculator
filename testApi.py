import requests

BASE = "http://127.0.0.1:5000/"

#Este archvo contiene pruebas para checar que el funcionamiento del backend Flask RESTFUL funcione correctamente

#Hacer post en la db al resolver la ecuacion para guardar estadisticas
response = requests.put(BASE + "solve/0/sin(x)")
print(response.json())

#Prueba de respuesta del api
for i in range(1000):
    response = requests.get(BASE + "solve/0.0/x%2Ax%20-%2016#")
print("done")

#Obtener estadisticas sobre el funcionamiento de la calculadora. Por ejemplo las iteraciones que se utilizan en promedio
response = requests.get(BASE + "getStats")
print(response.json()) 