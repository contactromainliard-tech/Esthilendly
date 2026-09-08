from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from app.models.client import Client
from app import db
import re


clients_bp = Blueprint('clients', __name__, url_prefix='/clients')

@clients_bp.route('/')
def index():
        clients = Client.query.all()
        return render_template('clients/index.html', clients=clients)

@clients_bp.route('/new', methods=['GET', 'POST'])
def create_client():

    # Gestion de la requête POST pour créer un nouveau client
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        surname = request.form.get('surname', '').strip()
        email = request.form.get('email', '').strip().lower()
        phone = request.form.get('phone', '').strip() or None

        # Validation des champs obligatoires
        if not name or not surname or not email:
            return render_template('clients/new.html', error="Le nom, prénom et email sont obligatoires.")

        # Validation de l'email format et unicité
        if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return render_template('clients/new.html', error="Adresse email invalide.")
        existing = Client.query.filter_by(email=email).first()
        if existing:
            return render_template('clients/new.html', error="Un client avec cet email existe déjà.")

        new_client = Client(name=name, surname=surname, email=email, phone=phone)
        db.session.add(new_client)
        db.session.commit()

        return redirect(url_for('clients.index'))
    #Si Méthode GET, afficher le formulaire vide
    return render_template('clients/new.html')



@clients_bp.route('/<int:client_id>')
def get_client(client_id):
    client = Client.query.get_or_404(client_id)
    return render_template('clients/detail.html', client=client) 