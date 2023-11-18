from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'  # Use SQLite as the database
db = SQLAlchemy(app)

# SQLAlchemy model for the Book table
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)

# Create the database and the Book table inside an application context
with app.app_context():
    db.create_all()


# Route to get all books
@app.route("/books", methods=["GET"])
def get_books():
    books = Book.query.all()
    book_list = [{"id": book.id, "title": book.title, "author": book.author} for book in books]
    return jsonify(book_list)

# Route to get a specific book by ID
@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = Book.query.get(book_id)
    if book:
        return jsonify({"id": book.id, "title": book.title, "author": book.author})
    return jsonify({"error": "Book not found"}), 404

# Route to create a new book
@app.route("/books", methods=["POST"])
def create_book():
    data = request.get_json()
    if "title" in data and "author" in data:
        new_book = Book(title=data["title"], author=data["author"])
        db.session.add(new_book)
        db.session.commit()
        return jsonify({"id": new_book.id, "title": new_book.title, "author": new_book.author}), 201
    return jsonify({"error": "Missing required fields"}), 400

# Route to update an existing book by ID
@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = Book.query.get(book_id)
    if book:
        data = request.get_json()
        if "title" in data:
            book.title = data["title"]
        if "author" in data:
            book.author = data["author"]
        db.session.commit()
        return jsonify({"id": book.id, "title": book.title, "author": book.author})
    return jsonify({"error": "Book not found"}), 404

# Route to delete a book by ID
@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify({"message": "Book deleted"})
    return jsonify({"error": "Book not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
