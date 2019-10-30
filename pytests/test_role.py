import requests


class TestRole:
    def test_creat_role(self, url_roles, role2):
        role2_t = role2
        response = requests.post(url_roles, role2_t)
        assert response.status_code == 201
        role2_t['id'] = response.json()['id']
        assert (role2_t == response.json())

    def test_get_role(self, url_roles, role_id, role1):
        response = requests.get(f'{url_roles}{role_id}')
        assert response.status_code == 200
        role1_t = role1
        role1_t['id'] = response.json()['id']
        assert role1_t == response.json()

    def test_del_role(self, url_roles, role_id):
        role_id_t = role_id
        response = requests.delete(f'{url_roles}{role_id_t}')
        assert response.status_code == 204
        response = requests.get(f'{url_roles}{role_id_t}')
        assert response.status_code == 404

    def test_edit_role(self, url_roles, role_id, role2):
        role_id_t = role_id
        role2_t = role2
        response = requests.put(f'{url_roles}{role_id_t}', role2_t)
        assert response.status_code == 200
        role2_t['id'] = response.json()['id']
        response = requests.get(f'{url_roles}{role_id_t}')
        assert role2_t, response.json()

    def test_creat_empty_role(self, url_roles):
        response = requests.post(url_roles)
        assert response.status_code == 400
        assert response.json() == {'name': ['This field is required.'], 'type': ['This field is required.']}

    def test_limit_value_roles(self, url_roles, role1, role_id):
        temp_role = role1
        role_id_t = role_id
        temp_role['name'] = '1' * 201
        temp_role['type'] = '1' * 256
        temp_role['level'] = -2147483649
        response = requests.put(f'{url_roles}{role_id_t}', temp_role)
        assert response.status_code == 400
        assert response.json()['name'][0] == 'Ensure this field has no more than 200 characters.'
        assert response.json()['type'][0] == 'Ensure this field has no more than 255 characters.'
        assert response.json()['level'][0] == 'Ensure this value is greater than or equal to -2147483648.'
        temp_role['level'] = 2147483648
        response = requests.put(f'{url_roles}{role_id_t}', temp_role)
        assert response.status_code == 400
        assert response.json()['level'][0] == 'Ensure this value is less than or equal to 2147483647.'