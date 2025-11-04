# simple-notes-application-38497-38508

Notes Backend (Flask)

- Framework: Flask + flask-smorest
- Port: 3001
- Docs: http://localhost:3001/docs
- Base URL: /notes

Quick Start

1) Create and activate a virtual environment (recommended)
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

2) Install dependencies
   cd notes_backend
   pip install -r requirements.txt

3) Run the server
   python run.py
   # Server runs on http://localhost:3001

4) Open API docs
   http://localhost:3001/docs

Health Endpoint

- GET /
  200 OK -> {"message":"Healthy"}

Notes Endpoints

- GET /notes
  200 OK -> [ { id, title, content, created_at, updated_at }, ... ]

- POST /notes
  Body: { "title": "My title", "content": "My content" }
  201 Created -> { id, title, content, created_at, updated_at }

- GET /notes/{id}
  200 OK -> { id, title, content, created_at, updated_at }
  404 Not Found if id does not exist

- PUT /notes/{id}
  Body (partial or full): { "title": "New", "content": "Updated" }
  200 OK -> updated note
  404 Not Found if id does not exist

- DELETE /notes/{id}
  204 No Content on success
  404 Not Found if id does not exist

cURL Examples

- List notes
  curl -s http://localhost:3001/notes

- Create a note
  curl -s -X POST http://localhost:3001/notes \
    -H "Content-Type: application/json" \
    -d '{"title":"First","content":"Hello"}'

- Get a note
  curl -s http://localhost:3001/notes/<id>

- Update a note
  curl -s -X PUT http://localhost:3001/notes/<id> \
    -H "Content-Type: application/json" \
    -d '{"content":"Updated text"}'

- Delete a note
  curl -s -X DELETE http://localhost:3001/notes/<id>

Notes on Persistence

- This implementation uses an in-memory store for simplicity. Data resets when the server restarts.
- To add persistence (e.g., SQLite via SQLAlchemy), introduce a Note model, migration steps, and update routes to use the database.
