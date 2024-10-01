## BUK

1. GET all books (with pagination and optional filters):
```bash
curl "http://localhost:5000/books?page=1&limit=10&genre=Fiction"
```

2. GET a specific book by ID:
```bash
curl http://localhost:5000/books/<id>
```

3. POST a new book:
```bash
curl -X POST http://localhost:5000/books \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test title",
    "author": "Test Author",
    "genre": "Test Genre",
    "publication_date": "0001-10-01",
    "price": 234
  }'
```

4. PUT update an existing book:
```bash
curl -X PUT http://localhost:5000/books/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "test update title",
    "price": 23424 
  }'
```

5. DELETE a book:
```bash
curl -X DELETE http://localhost:5000/books/<id>
```

6. Test the root route:
```bash
curl http://localhost:5000/
```

