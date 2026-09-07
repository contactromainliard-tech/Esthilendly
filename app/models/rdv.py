from app import db
import enum

class RDVStatus(enum.Enum):
    PENDING = 'en attente'
    CONFIRMED = 'confirmé'
    COMPLETED = 'terminé'
    CANCELLED = 'annulé'

class RDV(db.Model):
    __tablename__ = 'rdvs'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    service = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # Durée en minutes
    status = db.Column(db.Enum(RDVStatus), default=RDVStatus.PENDING)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    client = db.relationship('Client', backref=db.backref('rdvs', lazy=True))

    def __repr__(self):
        return f'<RDV {self.id} - Client {self.client_id} - Date {self.date}>'