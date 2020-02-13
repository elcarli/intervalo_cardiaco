from flask import Flask, request, render_template, jsonify
import serial, time
from tinydb import TinyDB, Query, where
import math, json

app = Flask(__name__)

@app.route("/")
def home():
	tit="Prueba COM2"
	return render_template("prueba.html",tit=tit)
	
@app.route("/historico")
def historico():
	tit="Historico"
	return render_template("historico.html",tit=tit)	
	
	
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
	
	#Es una lista pero con comillas simples
	#print(res)
	
	return jsonify(res)
	
	
@app.route("/consulta/<nombre>")
def consulta(nombre):
	
	db = TinyDB('db.json')
	
	res = db.search(where('nombre') == nombre)
	
	#print(nombre)
	
	#for item in res:
	#	print(item["hr"]+"-"+item["rr"])
		
	return jsonify(res)
	
if __name__ == "__main__":
	app.run()
