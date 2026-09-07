from flask import Blueprint, request, jsonify
from app.models.rdv import RDV, RDVStatus
from app import db
from datetime import datetime

rdv_bp = Blueprint('rdv', __name__, url_prefix='/rdv')

@rdv_bp.route('/')
def index():
    rdvs = RDV.query.all()
    return jsonify([{
        'id': rdv.id,
        'client_id': rdv.client_id,
        'date': rdv.date.isoformat(),
        'duration': rdv.duration,
        'status': rdv.status.value,
        'created_at': rdv.created_at.isoformat() if rdv.created_at else None
    } for rdv in rdvs])

@rdv_bp.route('/new', methods=['POST'])
def create_rdv():
    data = request.get_json()

    
    # 1. Vérifier d'abord
    if not data or not data.get('client_id') or not data.get('date'):
        return jsonify({'error': 'L\'ID du client et la date sont requis'}), 400
    
    # 2. Créer ensuite
    new_rdv = RDV(
        client_id=data.get('client_id'),
        date=datetime.fromisoformat(data.get('date')),
        status=RDVStatus.PENDING,
        duration=data.get('duration'),
        service=data.get('service')
    )
    db.session.add(new_rdv)
    db.session.commit()
    
    return jsonify({'message': 'Rendez-vous créé avec succès'}), 201

@rdv_bp.route('/<int:rdv_id>')
def get_rdv(rdv_id):
    rdv = RDV.query.get_or_404(rdv_id)
    return jsonify({
        'id': rdv.id,
        'client_id': rdv.client_id,
        'date': rdv.date.isoformat(),
        'duration': rdv.duration,
        'status': rdv.status.value,
        'created_at': rdv.created_at.isoformat() if rdv.created_at else None
    })

@rdv_bp.route('/<int:rdv_id>/update', methods=['PUT'])
def update_rdv(rdv_id):
    rdv = RDV.query.get_or_404(rdv_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Aucune donnée fournie pour la mise à jour'}), 400
    
    rdv.date = data.get('date', rdv.date)
    rdv.duration = data.get('duration', rdv.duration)
    rdv.status = data.get('status', rdv.status)
    
    db.session.commit()
    
    return jsonify({'message': 'Rendez-vous mis à jour avec succès'}), 200

@rdv_bp.route('/<int:rdv_id>/delete', methods=['DELETE'])
def delete_rdv(rdv_id):
    rdv = RDV.query.get_or_404(rdv_id)
    db.session.delete(rdv)
    db.session.commit()
    
    return jsonify({'message': 'Rendez-vous supprimé avec succès'}), 200