from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
db = SQLAlchemy(app)


# Crear Modelo de base de datos

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(11), nullable=False)

    def serealize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone
        }


# Crea las tablas en la base de datos
with app.app_context():
    db.create_all()

# Status
OK = 200
CREATED = 201
NOT_FOUND = 404


# Rutas API-REST
@app.route('/contacts', methods=['GET'])
def get_contacts():
    contacts = Contact.query.all()
    list_contact = []
    for contact in contacts:
        list_contact.append(contact.serealize())
    return jsonify({'contacts': list_contact}), OK
    # return jsonfy({
    # 'contacts': [contact.serealize() for contact in contacts]
    # }) esta es otra forma de hacerlo


@app.route('/contacts', methods=['POST'])
def create_contact():
    data = request.get_json()
    contact = Contact(
        name=data['name'],
        email=data['email'],
        phone=data['phone']
        )
    db.session.add(contact)
    db.session.commit()
    return jsonify({
        'Message': 'Contacto creado con exito',
        'contact': contact.serealize()
        }), CREATED


@app.route('/contacts/<int:id>', methods=['GET'])
def get_contact_byID(id):
    contact = Contact.query.get(id)
    if not contact:
        return jsonify({'Message': 'Contact not found'}), NOT_FOUND

    return jsonify(contact.serealize()), OK


@app.route('/contacts/<int:id>', methods=['PUT'])
def update_contact(id):
    contact = Contact.query.get_or_404(id)
    data = request.get_json()
    if 'name' in data:
        contact.name = data['name']
    if 'email' in data:
        contact.email = data['email']
    if 'phone' in data:
        contact.phone = data['phone']
    # guardar los cambios
    db.session.commit()

    return jsonify({
        'Message': 'Contact updated',
        'contact': contact.serealize()
        }), OK


@app.route('/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    contact = Contact.query.get(id)
    if not contact:
        return jsonify({'Message': 'Contact not found'}), NOT_FOUND
    db.session.delete(contact)
    db.session.commit()

    return jsonify({
        'Message': 'Contact deleted',
        'contact': contact.serealize()
        }), OK
