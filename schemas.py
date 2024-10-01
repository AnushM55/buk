from flask_marshmallow import Marshmallow
from marshmallow import ValidationError
from models import Book

ma = Marshmallow()

class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book
        load_instance = True

    def validate_price(self, value):
        if value <= 0:
            raise ValidationError("Price must be greater than 0.")

book_schema = BookSchema()
books_schema = BookSchema(many=True)

