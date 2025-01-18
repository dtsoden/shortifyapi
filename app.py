from flask import Flask, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
import string

# Initialize Flask application
app = Flask(__name__)

# Configure SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.shortifyapi.com.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the database models
class ShortLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), nullable=False)
    destination_url = db.Column(db.String(2048), nullable=False)
    unique_id = db.Column(db.String(10), unique=True, nullable=False)
    redirect_count = db.Column(db.Integer, default=0)

class RedirectLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(10), db.ForeignKey('short_link.unique_id'), nullable=False)
    redirect_date = db.Column(db.DateTime, default=datetime.utcnow)
    referring_url = db.Column(db.String(2048), nullable=True)

def generate_unique_id():
    """Generates a unique ID for the shortened URL."""
    while True:
        unique_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        if not ShortLink.query.filter_by(unique_id=unique_id).first():
            return unique_id

@app.route('/create', methods=['POST'])
def create_link():
    """Create a new short link."""
    data = request.json
    project_name = data.get('project_name')
    destination_url = data.get('destination_url')

    if not project_name or not destination_url:
        return jsonify({'error': 'Project name and destination URL are required.'}), 400

    unique_id = generate_unique_id()
    new_link = ShortLink(project_name=project_name, destination_url=destination_url, unique_id=unique_id)
    db.session.add(new_link)
    db.session.commit()

    return jsonify({'unique_id': unique_id, 'short_url': f"https://app.shortifyapi.com/{unique_id}"})

@app.route('/<unique_id>', methods=['GET'])
def redirect_to_destination(unique_id):
    """Redirects to the destination URL and logs the redirect."""
    short_link = ShortLink.query.filter_by(unique_id=unique_id).first()

    if not short_link:
        return jsonify({'error': 'Short URL not found.'}), 404

    # Update redirect count
    short_link.redirect_count += 1
    db.session.commit()

    # Log the redirect
    referring_url = request.referrer
    redirect_log = RedirectLog(unique_id=unique_id, referring_url=referring_url)
    db.session.add(redirect_log)
    db.session.commit()

    return redirect(short_link.destination_url)

@app.route('/logs/<unique_id>', methods=['GET'])
def get_redirect_logs(unique_id):
    """Retrieve all logs for a given short link or all logs if unique_id is 0."""
    if unique_id == "0":
        logs = RedirectLog.query.all()
    else:
        logs = RedirectLog.query.filter_by(unique_id=unique_id).all()

    if not logs:
        return jsonify({'error': 'No logs found.'}), 404

    log_list = [
        {
            'id': log.id,
            'unique_id': log.unique_id,
            'redirect_date': log.redirect_date,
            'referring_url': log.referring_url
        } for log in logs
    ]

    return jsonify({'logs': log_list})

@app.route('/all_links', methods=['GET'])
def get_all_links():
    """Retrieve all rows and columns from the ShortLink table."""
    links = ShortLink.query.all()
    link_list = [
        {
            'id': link.id,
            'project_name': link.project_name,
            'destination_url': link.destination_url,
            'unique_id': link.unique_id,
            'redirect_count': link.redirect_count
        } for link in links
    ]

    return jsonify({'links': link_list})

@app.route('/update/<unique_id>', methods=['PUT'])
def update_link(unique_id):
    """Update a short link."""
    short_link = ShortLink.query.filter_by(unique_id=unique_id).first()

    if not short_link:
        return jsonify({'error': 'Short URL not found.'}), 404

    data = request.json
    if 'project_name' in data:
        short_link.project_name = data['project_name']
    if 'destination_url' in data:
        short_link.destination_url = data['destination_url']

    db.session.commit()
    return jsonify({'message': 'Short URL updated successfully.'})

@app.route('/delete/<unique_id>', methods=['DELETE'])
def delete_link(unique_id):
    """Delete a short link."""
    short_link = ShortLink.query.filter_by(unique_id=unique_id).first()

    if not short_link:
        return jsonify({'error': 'Short URL not found.'}), 404

    db.session.delete(short_link)
    db.session.commit()
    return jsonify({'message': 'Short URL deleted successfully.'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=80) 
