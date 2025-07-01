from flask import render_template
from app import app
from gestor.core import FinanceManager

fm = FinanceManager()
fm.load_excel()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/transacciones")
def mostrar_transacciones():
    transacciones = fm.df_transactions.to_dict(orient='records')
    return render_template("transacciones.html", transacciones=transacciones)

@app.route("/nueva", methods=["GET"])
def nueva_transaccion():
    return render_template("nueva_transaccion.html")
