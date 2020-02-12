from flask import Flask, request, render_template, jsonify
import serial, time
from tinydb import TinyDB, Query
import math

app = Flask(__name__)

@app.route("/")
def home():
	tit="Prueba COM2"
	return render_template("prueba.html",tit=tit)
	
@app.route("/sesion")
def sesion():
	
	nombre=request.args['nombre']
	
	port = "COM2"
	ser = serial.Serial(port, 9600)
	
	hr = ser.readline().decode()
	hr = hr.replace("\r\n", "")
	
	rr = ser.readline().decode()
	rr = rr.replace("\r\n", "")
	
	ser.close()
	
	aux = jsonify({"hr": str(hr), "rr": str(rr)})
	
	db = TinyDB('db.json')
	db.insert({"hr": str(hr), "rr": str(rr)})
	
	return aux
	
	
@app.route("/lista")
def lista():
	
	db = TinyDB('db.json')
	
	for item in db:
		print(item["hr"]+"-"+item["rr"])
		
	return "probando"
	
if __name__ == "__main__":
	app.run()
