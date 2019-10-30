import unittest
import requests
from copy import copy


class OurTestClass(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls._book = {"title": "My Book",
                     "author": "Dmytro Pochernin"}
        cls._book2 = {"title": "Autobiography",
                      "author": "Dmytro Pochernin"}

        cls._URL_BOOKS = "http://pulse-rest-testing.herokuapp.com/books/"
        cls._URL_ROLES = "http://pulse-rest-testing.herokuapp.com/roles/"

        cls._role1 = {"name": "Dmytro Pochernin",
                      "type": "dpochernin test",
                      "level": 1,
                      "book": ""}
        cls._role2 = {"name": "Marina Pochernina",
                      "type": "dpochernin test",
                      "level": 1,
                      "book": ""}

    @classmethod
    def tearDownClass(cls) -> None:
        for book in requests.get("http://pulse-rest-testing.herokuapp.com/books/").json():
            if book["author"] == "Dmytro Pochernin":
                requests.delete(url=f'http://pulse-rest-testing.herokuapp.com/books/{book["id"]}')
        for role in requests.get("http://pulse-rest-testing.herokuapp.com/roles/").json():
            if role["type"] == "dpochernin test":
                requests.delete(url=f'http://pulse-rest-testing.herokuapp.com/roles/{role["id"]}')

    def setUp(self):
        self._book_id = requests.post(url=self._URL_BOOKS, data=self._book).json()['id']
        self._role1["book"] = f'{self._URL_BOOKS}{self._book_id}'
        self._role2["book"] = f'{self._URL_BOOKS}{self._book_id}'
        self._role_id_1 = requests.post(url=self._URL_ROLES, data=self._role1).json()['id']

    def tearDown(self) -> None:
        requests.delete(f'{self._URL_BOOKS}{str(self._book_id)}')

    def test_book_create(self):
        response = requests.post(url=self._URL_BOOKS, data=self._book)
        book_id = response.json()['id']
        self.assertEqual(201, response.status_code)
        temp_book = self._book
        temp_book['id'] = book_id
        self.assertEqual(response.json(), temp_book)

    def test_get_book_by_id(self):
        response = requests.get(url=f'{self._URL_BOOKS}{self._book_id}')
        self._book['id'] = self._book_id
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self._book)

    def test_book_create_with_id(self):
        temp_book = self._book
        temp_book['id'] = '50000'
        response = requests.post(url=self._URL_BOOKS, data=temp_book)
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(response.json()['id'], temp_book['id'])

    def test_book_create_empty_data(self):
        response = requests.post(url=self._URL_BOOKS, data={})
        self.assertEqual(400, response.status_code)
        self.assertEqual(response.json()['title'][0], 'This field is required.')
        self.assertEqual(response.json()['author'][0], 'This field is required.')

    def test_book_create_wrong_data(self):  # !!!!!
        data = {"title": {"title": "My Book",
                          "author": "Dmytro Pochernin"},
                "author": "Dmytro Pochernin"}
        response = requests.post(url=self._URL_BOOKS, data=data)
        self.assertNotEqual(201, response.status_code,
                            f'Must verify data type in json, response {response.status_code}')

    def test_book_delete(self):
        response = requests.delete(f'{self._URL_BOOKS}{self._book_id}')
        self.assertEqual(response.status_code, 204)
        response = requests.get(f'{self._URL_BOOKS}{self._book_id}')
        self.assertEqual(response.status_code, 404)

    def test_book_lengt(self):
        temp_book = {'title': '1' * 51, 'author': '1' * 51}
        response = requests.post(url=self._URL_BOOKS, data=temp_book)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['title'][0], 'Ensure this field has no more than 50 characters.')
        self.assertEqual(response.json()['author'][0], 'Ensure this field has no more than 50 characters.')

    def test_edit_book(self):
        response = requests.put(f'{self._URL_BOOKS}{self._book_id}', self._book2)
        self.assertEqual(response.status_code, 200)
        self._book2['id'] = response.json()['id']
        response = requests.get(f'{self._URL_BOOKS}{self._book_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self._book2)

    def test_del_on_book_root(self):
        response = requests.delete(f'{self._URL_BOOKS}')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json()['detail'], 'Method "DELETE" not allowed.')

    def test_put_on_book_root(self):
        response = requests.put(f'{self._URL_BOOKS}')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json()['detail'], 'Method "PUT" not allowed.')

    def test_creat_role(self):
        response = requests.post(self._URL_ROLES, self._role2)
        self.assertEqual(response.status_code, 201)
        self._role2['id'] = response.json()['id']
        self.assertEqual(self._role2, response.json())

    def test_get_role(self):
        response = requests.get(f'{self._URL_ROLES}{self._role_id_1}')
        self.assertEqual(response.status_code, 200)
        self._role1['id'] = response.json()['id']
        self.assertEqual(self._role1, response.json())

    def test_del_role(self):
        response = requests.delete(f'{self._URL_ROLES}{self._role_id_1}')
        self.assertEqual(response.status_code, 204)
        response = requests.get(f'{self._URL_ROLES}{self._role_id_1}')
        self.assertEqual(response.status_code, 404)

    def test_edit_role(self):
        response = requests.put(f'{self._URL_ROLES}{self._role_id_1}', self._role2)
        self.assertEqual(response.status_code, 200)
        self._role2['id'] = response.json()['id']
        response = requests.get(f'{self._URL_ROLES}{self._role_id_1}')
        self.assertEqual(self._role2, response.json())

    def test_creat_empty_role(self):
        response = requests.post(self._URL_ROLES)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'name': ['This field is required.'], 'type': ['This field is required.']})

    def test_limit_value_roles(self):
        temp_role = copy(self._role1)
        temp_role['name'] = '1' * 201
        temp_role['type'] = '1' * 256
        temp_role['level'] = -2147483649
        response = requests.put(f'{self._URL_ROLES}{self._role_id_1}', temp_role)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['name'][0], 'Ensure this field has no more than 200 characters.')
        self.assertEqual(response.json()['type'][0], 'Ensure this field has no more than 255 characters.')
        self.assertEqual(response.json()['level'][0], 'Ensure this value is greater than or equal to -2147483648.')
        temp_role['level'] = 2147483648
        response = requests.put(f'{self._URL_ROLES}{self._role_id_1}', temp_role)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['level'][0], 'Ensure this value is less than or equal to 2147483647.')


myTestSuit = unittest.TestLoader().loadTestsFromTestCase(OurTestClass)

if __name__ == "__main__":
    from HtmlTestRunner import HTMLTestRunner

    unittest.main(verbosity=2, testRunner=HTMLTestRunner(output=r".\\"))
