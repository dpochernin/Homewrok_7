from copy import copy

import requests


class TestBook:
    # _book_id = None

    # def test_book_create(self, url_book, book):
    #     response = requests.post(url=url_book, data=book)
    #     self._book_id = response.json()['id']
    #     assert 201 == response.status_code
    #     book['id'] = self._book_id
    #     assert requests.get(f'{url_book}{self._book_id}').json() == book
    #
    # def test_book_delete(self, url_book):
    #     response = requests.delete(f'{url_book}{self._book_id}')
    #     assert response.status_code == 200

    def test_book_create(self, url_book, book):
        response = requests.post(url=url_book, data=book)
        book_id = response.json()['id']
        assert 201 == response.status_code
        temp_book = book
        temp_book['id'] = book_id
        assert (response.json(), temp_book)

    def test_get_book_by_id(self, url_book, book, book_id):
        b_id = book_id
        response = requests.get(url=f'{url_book}{b_id}')
        book_t = book
        book_t['id'] = b_id

        assert response.status_code == 200
        assert response.json() == book_t

    def test_book_create_with_id(self, url_book, book):
        temp_book = copy(book)
        temp_book['id'] = '50000'
        response = requests.post(url=url_book, data=temp_book)
        assert response.status_code == 201
        assert response.json()['id'] != temp_book['id']

    def test_book_create_empty_data(self, url_book, book):
        response = requests.post(url=url_book, data={})
        assert 400 == response.status_code
        assert response.json()['title'][0] == 'This field is required.'
        assert response.json()['author'][0] == 'This field is required.'

    def test_book_create_wrong_data(self, url_book, book):  # !!!!!
        data = {"title": {"title": "My Book",
                          "author": "Dmytro Pochernin"},
                "author": "Dmytro Pochernin"}
        response = requests.post(url=url_book, data=data)
        assert 201 != response.status_code

    def test_book_delete(self, url_book, book_id):
        response = requests.delete(f'{url_book}{book_id}')
        assert response.status_code == 204
        response = requests.get(f'{url_book}{book_id}')
        assert response.status_code == 404

    def test_book_lengt(self, url_book):
        temp_book = {'title': '1' * 51, 'author': '1' * 51}
        response = requests.post(url=url_book, data=temp_book)
        assert response.status_code == 400
        assert response.json()['title'][0] == 'Ensure this field has no more than 50 characters.'
        assert response.json()['author'][0] == 'Ensure this field has no more than 50 characters.'

    def test_edit_book(self, url_book, book2, book_id):
        book_id_t = book_id
        book2_t = book2
        response = requests.put(f'{url_book}{book_id_t}', book2_t)
        assert response.status_code == 200
        book2_t['id'] = response.json()['id']
        response = requests.get(f'{url_book}{book_id_t}')
        assert response.status_code == 200
        assert response.json() == book2_t

    def test_del_on_book_root(self, url_book):
        response = requests.delete(f'{url_book}')
        assert response.status_code == 405
        assert response.json()['detail'] == 'Method "DELETE" not allowed.'

    def test_put_on_book_root(self, url_book):
        response = requests.put(f'{url_book}')
        assert response.status_code == 405
        assert response.json()['detail'] == 'Method "PUT" not allowed.'
