from flask_smorest import Blueprint, abort
from flask.views import MethodView
from marshmallow import Schema, fields, validate, EXCLUDE
from typing import Dict, Any
from uuid import uuid4
from datetime import datetime

# In-memory store for simplicity. Can be replaced by SQLite if needed.
NOTES_STORE: Dict[str, Dict[str, Any]] = {}


class NoteBaseSchema(Schema):
    """Base schema for note fields."""
    class Meta:
        unknown = EXCLUDE

    title = fields.Str(required=True, validate=validate.Length(min=1, max=200), description="Title of the note")
    content = fields.Str(required=True, validate=validate.Length(min=1), description="Content/body of the note")


class NoteCreateSchema(NoteBaseSchema):
    """Schema for creating a note."""
    pass


class NoteUpdateSchema(Schema):
    """Schema for updating a note (partial updates allowed)."""
    class Meta:
        unknown = EXCLUDE

    title = fields.Str(required=False, validate=validate.Length(min=1, max=200), description="Title of the note")
    content = fields.Str(required=False, validate=validate.Length(min=1), description="Content/body of the note")


class NoteSchema(NoteBaseSchema):
    """Full representation of a note."""
    id = fields.Str(required=True, description="Unique identifier for the note")
    created_at = fields.DateTime(required=True, description="Creation timestamp in ISO format")
    updated_at = fields.DateTime(required=True, description="Last update timestamp in ISO format")


blp = Blueprint(
    "Notes",
    "notes",
    url_prefix="/notes",
    description="CRUD endpoints for managing notes"
)


def _get_note_or_404(note_id: str) -> Dict[str, Any]:
    """Internal helper to fetch a note or abort with 404."""
    note = NOTES_STORE.get(note_id)
    if not note:
        abort(404, message=f"Note with id '{note_id}' not found")
    return note


@blp.route("/", methods=["GET", "POST"])
class NotesCollection(MethodView):
    # PUBLIC_INTERFACE
    def get(self):
        """List all notes.
        Returns a list of notes.
        """
        return list(NOTES_STORE.values()), 200

    # PUBLIC_INTERFACE
    @blp.arguments(NoteCreateSchema)
    @blp.response(201, NoteSchema)
    def post(self, json_data: Dict[str, Any]):
        """Create a new note.
        Body: { title: string, content: string }
        Returns created note with id.
        """
        note_id = str(uuid4())
        now = datetime.utcnow().isoformat() + "Z"
        note = {
            "id": note_id,
            "title": json_data["title"],
            "content": json_data["content"],
            "created_at": now,
            "updated_at": now,
        }
        NOTES_STORE[note_id] = note
        return note, 201


@blp.route("/<string:note_id>", methods=["GET", "PUT", "DELETE"])
class NotesResource(MethodView):
    # PUBLIC_INTERFACE
    @blp.response(200, NoteSchema)
    def get(self, note_id: str):
        """Get a specific note by id.
        Path params:
          - note_id: string
        Returns the note.
        """
        note = _get_note_or_404(note_id)
        return note, 200

    # PUBLIC_INTERFACE
    @blp.arguments(NoteUpdateSchema)
    @blp.response(200, NoteSchema)
    def put(self, json_data: Dict[str, Any], note_id: str):
        """Update a note by id (full or partial).
        Body may include title and/or content.
        Returns the updated note.
        """
        note = _get_note_or_404(note_id)
        changed = False
        if "title" in json_data:
            note["title"] = json_data["title"]
            changed = True
        if "content" in json_data:
            note["content"] = json_data["content"]
            changed = True
        if changed:
            note["updated_at"] = datetime.utcnow().isoformat() + "Z"
        NOTES_STORE[note_id] = note
        return note, 200

    # PUBLIC_INTERFACE
    def delete(self, note_id: str):
        """Delete a note by id.
        Returns 204 on success.
        """
        _ = _get_note_or_404(note_id)
        del NOTES_STORE[note_id]
        return "", 204
