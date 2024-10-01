"""
This is file is created to insert the test data
"""

from flask import Flask
from database import db, init_db
from routes import api
from models import Book
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookstore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app)
app.register_blueprint(api)

def add_sample_data():
    books = [
        Book(title="To Kill a Mockingbird", author="Harper Lee", genre="Fiction", publication_date=datetime(1960, 7, 11).date(), price=12.99),
        Book(title="1984", author="George Orwell", genre="Science Fiction", publication_date=datetime(1949, 6, 8).date(), price=10.99),
        Book(title="Pride and Prejudice", author="Jane Austen", genre="Romance", publication_date=datetime(1813, 1, 28).date(), price=9.99),
        Book(title="The Great Gatsby", author="F. Scott Fitzgerald", genre="Fiction", publication_date=datetime(1925, 4, 10).date(), price=11.99),
        Book(title="To the Lighthouse", author="Virginia Woolf", genre="Modernist", publication_date=datetime(1927, 5, 5).date(), price=14.99),
    ]
    
    for book in books:
        db.session.add(book)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        add_sample_data()  # Add this line to populate the database
    app.run(debug=True)

