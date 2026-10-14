import pytest

from app import app
from database import init_db, get_db_connection


@pytest.fixture
def client(tmp_path, monkeypatch):
    test_database = tmp_path / "test_smarttable.db"

    monkeypatch.setattr(
        "database.DATABASE_PATH",
        test_database
    )

    init_db()

    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"New order" in response.data


def test_menu_page(client):
    response = client.get("/menu")
    assert response.status_code == 200
    assert b"Paneer Tikka" in response.data


def test_help_page(client):
    response = client.get("/help")
    assert response.status_code == 200


def test_bill_page(client):
    response = client.get("/bill")
    assert response.status_code == 200


def test_order_without_items(client):
    response = client.post("/place-order", data={})
    assert response.status_code == 400
    assert b"Please select at least one item" in response.data


def test_order_with_items(client):
    response = client.post(
        "/place-order",
        data={
            "quantity_2": "2",
            "quantity_6": "1"
        }
    )

    assert response.status_code == 200
    assert b"ORDER CONFIRMED" in response.data


def test_order_is_saved(client):
    client.post(
        "/place-order",
        data={
            "quantity_2": "2",
            "quantity_6": "1"
        }
    )

    connection = get_db_connection()
    order_count = connection.execute(
        "SELECT COUNT(*) FROM orders"
    ).fetchone()[0]
    connection.close()

    assert order_count == 1


def test_help_request_is_saved(client):
    response = client.post(
        "/help",
        data={
            "reason": "Need assistance",
            "message": "Please help with my order"
        }
    )

    assert response.status_code == 200
    assert b"Your assistance request has been submitted!" in response.data

    connection = get_db_connection()
    request_count = connection.execute(
        "SELECT COUNT(*) FROM help_requests"
    ).fetchone()[0]
    connection.close()

    assert request_count == 1


def test_invalid_payment_method(client):
    response = client.post(
        "/bill",
        data={"payment_method": "Invalid"}
    )

    assert response.status_code == 200
    assert b"Please select a valid payment method." in response.data