
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from models import Book
from schemas import book_schema, books_schema
from database import db
from datetime import datetime

api = Blueprint('api', __name__)

@api.route('/books', methods=['GET'])
def get_books():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('limit', 10, type=int)
    genre = request.args.get('genre')
    author = request.args.get('author')

    query = Book.query

    if genre:
        query = query.filter(Book.genre == genre)
    if author:
        query = query.filter(Book.author == author)

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    books = pagination.items

    base_url = request.base_url
    result = {
        'current_page': pagination.page,
        'total_books': pagination.total,
        'total_pages': pagination.pages,
        'next_page': f"{base_url}?page={pagination.next_num}&limit={per_page}&genre={genre or ''}&author={author or ''}" if pagination.has_next else None,
        'previous_page': f"{base_url}?page={pagination.prev_num}&limit={per_page}&genre={genre or ''}&author={author or ''}" if pagination.has_prev else None,
        'books': books_schema.dump(books)
    }

    return jsonify(result)

@api.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get_or_404(id, description="Book not found")
    return book_schema.jsonify(book)

@api.route('/books', methods=['POST'])
def add_book():
    try:
        data = book_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"error": "Validation failed", "messages": err.messages}), 400

    new_book = Book(
        title=data['title'],
        author=data['author'],
        genre=data['genre'],
        publication_date=datetime.strptime(data['publication_date'], '%Y-%m-%d').date(),
        price=data['price']
    )

    db.session.add(new_book)
    db.session.commit()

    return jsonify({"message": "Book added successfully", "book": book_schema.dump(new_book)}), 201

@api.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get_or_404(id, description="Book not found")

    try:
        data = book_schema.load(request.json, partial=True)
    except ValidationError as err:
        return jsonify({"error": "Validation failed", "messages": err.messages}), 400

    for key, value in data.items():
        if key == 'publication_date':
            value = datetime.strptime(value, '%Y-%m-%d').date()
        setattr(book, key, value)

    db.session.commit()

    return jsonify({"message": "Book updated successfully", "book": book_schema.dump(book)})

@api.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id, description="Book not found")
    db.session.delete(book)
    db.session.commit()

    return jsonify({"message": "Book deleted successfully"})

@api.errorhandler(404)
def not_found(error):
    return jsonify({"error": str(error)}), 404

@api.errorhandler(400)
def bad_request(error):
    return jsonify({"error": str(error)}), 400
