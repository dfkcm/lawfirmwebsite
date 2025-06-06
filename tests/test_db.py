import os
import pytest

# Ensure in-memory SQLite is used
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app import app, db
from models import Contact


def test_contact_insert_and_query():
    with app.app_context():
        db.drop_all()
        db.create_all()

        sample = Contact(
            full_name="John Doe",
            email="john@example.com",
            subject="Greetings",
            message="Hello World"
        )
        db.session.add(sample)
        db.session.commit()

        retrieved = Contact.query.first()
        assert retrieved is not None
        assert retrieved.full_name == "John Doe"
        assert retrieved.email == "john@example.com"
        assert retrieved.subject == "Greetings"
        assert retrieved.message == "Hello World"
