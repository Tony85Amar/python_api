from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100))
    author = db.Column(db.String(100))
    publisher = db.Column(db.String(100))

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()

    return jsonify([
        {
            "id": book.id,
            "book_name": book.book_name,
            "author": book.author,
            "publisher": book.publisher
        }
        for book in books
    ])

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()

    book = Book(
        book_name=data['book_name'],
        author=data['author'],
        publisher=data['publisher']
    )

    db.session.add(book)
    db.session.commit()

    return jsonify({"message": "Book added"})

@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get(id)
    data = request.get_json()

    book.book_name = data['book_name']
    book.author = data['author']
    book.publisher = data['publisher']

    db.session.commit()

    return jsonify({"message": "Book updated"})

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)

    db.session.delete(book)
    db.session.commit()

    return jsonify({"message": "Book deleted"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)