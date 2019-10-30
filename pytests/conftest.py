import pytest
import requests


@pytest.fixture(scope="session")
def url_book():
    return "http://pulse-rest-testing.herokuapp.com/books/"


@pytest.fixture(scope="session")
def url_roles():
    return "http://pulse-rest-testing.herokuapp.com/roles/"


@pytest.fixture(scope="session")
def book():
    return {"title": "My Book",
            "author": "Dmytro Pochernin"}


@pytest.fixture(scope="session")
def book2():
    return {"title": "Autobiography",
            "author": "Dmytro Pochernin"}


@pytest.fixture()
def book_id(url_book, book):
    return requests.post(f'{url_book}', book).json()['id']


@pytest.fixture(scope="session")
def role1():
    return {"name": "Dmytro Pochernin",
            "type": "dpochernin test",
            "level": 1,
            "book": None}


@pytest.fixture(scope="session")
def role2():
    return {"name": "Marina Pochernina",
            "type": "dpochernin test",
            "level": 1,
            "book": None}

@pytest.fixture()
def role_id(url_roles, role1):
    return requests.post(f'{url_roles}', role1).json()['id']

@pytest.fixture(autouse=True, scope="session")
def cleanup():
    yield
    for book in requests.get(f'http://pulse-rest-testing.herokuapp.com/books').json():
        if book["author"] == "Dmytro Pochernin":
            requests.delete(f'http://pulse-rest-testing.herokuapp.com/books/{book["id"]}')
    for role in requests.get("http://pulse-rest-testing.herokuapp.com/roles/").json():
        if role["type"] == "dpochernin test":
            requests.delete(url=f'http://pulse-rest-testing.herokuapp.com/roles/{role["id"]}')
