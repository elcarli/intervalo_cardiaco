from flask import Flask, request, render_template, jsonify
import serial, time
from tinydb import TinyDB, Query, where
import math, json

from operator import itemgetter
from itertools import groupby

import numpy as np
import statistics

app = Flask(__name__)

@app.route("/")
def home():
	tit="Prueba COM2"
	return render_template("prueba.html",tit=tit)
	
@app.route("/historico")

def historico():
	tit="Historico"
	return render_template("historico.html",tit=tit)	
	
def analisis():
	tit="Analisis de sesiones"
	return render_template("analisis.html",tit=tit)	
	
@app.route("/sesion")
def sesion():
	
	nombre=request.args['name']
	
	print(nombre)
	
	port = "COM2"
	ser = serial.Serial(port, 9600)
	
	hr = ser.readline().decode()
	hr = hr.replace("\r\n", "")
	
	rr = ser.readline().decode()
	rr = rr.replace("\r\n", "")
	
	ser.close()
	
	aux = jsonify({"hr": str(hr), "rr": str(rr)})
	
	db = TinyDB('db.json')
		
	db.insert({"nombre": str(nombre), "hr": str(hr), "rr": str(rr)})
	
	return aux
	
	
@app.route("/lista")
def lista():
	
	db = TinyDB('db.json')
	res = db.all()
	
	#Es una lista de diccionarios
	print(res)
	
	return jsonify(res)
	
	
@app.route("/consulta/<nombre>")
def consulta(nombre):
	
	db = TinyDB('db.json')
	
	res = db.search(where('nombre') == nombre)
	
	#print(nombre)
	
	#for item in res:
	#	print(item["hr"]+"-"+item["rr"])
		
	return jsonify(res)

@app.route("/analizar")
def analizar():
	
	db = TinyDB('db.json')
	res = db.all()
	
	data = []
	
	# Now iterate through groups (here we will group by the year born)
	for nombre, items in groupby(res, key=itemgetter('nombre')):
		print (nombre)
		grupo=[]
				
		for i in items:
			#se separan las mediciones por nombre
			grupo.append(i)
		
		listaHR = [x['hr'] for x in grupo]
		listaHR = list(map(int, listaHR))
		
		listaRR = [x['rr'] for x in grupo]
		listaRR = list(map(int, listaRR))
		
		#dato necesario para hallar el pRR50
		count50 = 0
		aux = len(listaRR)
		
		
		for i in range(0, aux-1):
			#Si intervalos RR sucesivos tienen diferencia mayor a 50 milisegundos. 
			
			print(abs(listaRR[i] - listaRR[i+1]))
			print(" ")
			
			if(abs(listaRR[i] - listaRR[i+1])> 50):
				count50+=1
		
		prr50 = count50 / (aux-1)
		
		dicc = {'nombre': nombre, 'meanHR': np.mean(listaHR), 'maxHR': max(listaHR), 'minHR': min(listaHR), 'sdHR': np.std(listaHR), 
			'meanRR': np.mean(listaRR), 'maxRR': max(listaRR), 'minRR': min(listaRR), 'sdRR': np.std(listaRR), 'prr50': prr50}
		
		data.append(dicc)
				
			
	#Debo retornar varios conjuntos de datos (meanHR, maxHR, minHR, sdHR --- meanRR, maxRR, minRR, sdRR --- pRR50) filtrados por nombre
	return jsonify(data)
	
if __name__ == "__main__":
	app.run()
