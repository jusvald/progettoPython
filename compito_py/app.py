from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import ListaSpesa, db

app = Flask(__name__)
lista =[]


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lista.db' #questa riga definisce url del database 

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #questa riga tiene traccia delle modifiche apportate agli oggetti nel database

db.init_app(app)#inizializzazione DB

with app.app_context():#creazione contesto    
    db.create_all() # Questo esamina tutti i modelli  nel codice e crea le tabelle nel DB


#rotta principale


@app.route('/')
def home():
    lista= ListaSpesa.query.all() #

    return render_template('index.html',lista=lista)

@app.route('/aggiungi', methods=['POST'])
def aggiungi():
   elemento = request.form['elemento']
   if elemento:

        nuovo_elemento = ListaSpesa(elemento=elemento) #crea un nuovo oggetto lista

        db.session.add(nuovo_elemento) # Aggiunge il nuovo elemento al database

        db.session.commit()#salva l'elemento nel database

        return redirect(url_for('home'))

@app.route('/rimuovi/<int:indice>', methods=['POST'])
def rimuovi(indice):

    elemento = ListaSpesa.query.get_or_404(indice) #Cerca l'elemento per e da errore 404 se non trovato

    db.session.delete(elemento) #Elimina l'elemento  dal database

    db.session.commit() #salva l'elemento nel database

    return redirect(url_for('home'))

@app.route('/svuota_lista', methods=['POST'])
def svuota_lista():


    ListaSpesa.query.delete() #Elimina tutti gli elementi dal database
    db.session.commit() #salva le modifiche del database



    return redirect(url_for('home'))

if __name__ == '__main__':
 app.run(debug=True)