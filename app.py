# -*- coding:utf-8 -*-

from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crud.db'

db = SQLAlchemy(app)

class Clientes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(250), nullable=False)
    endereco = db.Column(db.String(250), nullable=False)
    telefone = db.Column(db.String(250), nullable=True)
    data_de_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Cliente %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        nome_do_cliente = request.form['nome']
        endereco_do_cliente = request.form['end']
        telefone_do_cliente = request.form['fone']
        novo_cliente = Clientes(nome = nome_do_cliente, endereco = endereco_do_cliente, telefone = telefone_do_cliente)

        try:
            db.session.add(novo_cliente)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error adding to database!'
    else:
        clientes = Clientes.query.order_by(Clientes.data_de_cadastro).all()
        return render_template('index.html', clientes=clientes)

if __name__ == "__main__":
    app.run(debug=True)
