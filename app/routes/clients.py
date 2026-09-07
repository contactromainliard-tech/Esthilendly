from flask import Blueprint, jsonify, request, render_template
from app.models.client import Client
from app import db



clients_bp = Blueprint('clients', __name__, url_prefix='/clients')

@clients_bp.route('/')
def index():
        clients = Client.query.all()
        return render_template('clients/index.html', clients=clients)

@clients_bp.route('/new', methods=['POST'])
def create_client():
    data = request.get_json()
    
    # 1. Vérifier d'abord
    if not data or not data.get('name') or not data.get('email'):
        return jsonify({'error': 'Le nom et l\'email sont requis'}), 400
    
    # 2. Créer ensuite
    new_client = Client(
        name=data.get('name'),
        surname=data.get('surname'),
        email=data.get('email'),
        phone=data.get('phone')
    )
    db.session.add(new_client)
    db.session.commit()
    
    return jsonify({'message': 'Client créé avec succès'}), 201



@clients_bp.route('/<int:client_id>')
def get_client(client_id):
    client = Client.query.get_or_404(client_id)
    return render_template('clients/detail.html', client=client) 