import json


def test_registration_1(testapp):
    """Test registration for one user."""
    account = {
        'email': 'testUser1@example.com',
        'password': 'hello',
    }

    response = testapp.post(
        '/api/v1/auth/register',
        json.dumps(account)
    )

    # import pdb; pdb.set_trace()
    assert response.status_code == 201
    assert response.json['token']


def test_registration_2(testapp):
    """Test registration for one user."""
    account = {
        'email': 'testUser2@example.com',
        'password': 'hello',
    }

    response = testapp.post(
        '/api/v1/auth/register',
        json.dumps(account)
    )

    # import pdb; pdb.set_trace()
    assert response.status_code == 201
    assert response.json['token']


def test_duplicate_registration(testapp):
    """Test login with duplicate username: testUser1@example.com."""
    account = {
        'email': 'testUser1@example.com',
        'password': 'hello',
    }

    response = testapp.post(
        '/api/v1/auth/register',
        json.dumps(account),
        status='4**'
    )
    assert response.status_code == 400


def test_invalid_registration(testapp):
    """Test failed registration with no password."""
    account = {
        'email': 'fake_account@example.com',
    }

    response = testapp.post(
        '/api/v1/auth/register',
        json.dumps(account),
        status='4**'
    )
    assert response.status_code == 400
    # import pdb; pdb.set_trace()


def test_login(testapp):
    """Test login successful for testUser1."""
    account = {
        'email': 'testUser1@example.com',
        'password': 'hello',
    }

    response = testapp.post(
        '/api/v1/auth/login',
        json.dumps(account)
    )
    assert response.status_code == 200
    assert response.json['token']


def test_create_analysis(testapp):
    """Log in as a user to test post analysis to display JSON object api/v1/analysis """
    account = {
        'email': 'testUser1@example.com',
        'password': 'hello',
    }

    token = testapp.post('/api/v1/auth/login', json.dumps(account)).json['token']

    text = {"text": "In my younger and more vulnerable years my father gave me some advice that "
                    "I've been turning over in my mind ever since. Whenever you feel like criticizing anyone, "
                    "he told me, just remember that all the people in this world haven't had the advantages "
                    "that you've had."}

    testapp.authorization = ('Bearer', token)
    response = testapp.post('/api/v1/analysis', json.dumps(text))

    assert response.status_code == 201


def test_delete_user2_is_successful(testapp):
    """Login as testUser 1 to delete testUser2   """
    account = {
        'email': 'testUser1@example.com',
        'password': 'hello',
    }

    token = testapp.post('/api/v1/auth/login', json.dumps(account)).json['token']

    user_id = {'account_id': '2',
               'email': 'testUser1@example.com',
               'password': 'hello'
               }

    testapp.authorization = ('Bearer', token)

    response = testapp.delete('/api/v1/admin/delete/2', json.dumps(user_id), status='2**')

    assert response.status_code == 204


# def test_delete_user2_is_not_authorized(testapp):
#     """Not logged in as a user and delete user fails   """
#     # account = {
#     #     'email': 'testUser1@example.com',
#     #     'password': 'hello',
#     # }
#
#     # token = testapp.post('/api/v1/auth/login', json.dumps(account)).json['token']
#
#     user_id = {'account_id': '2',
#                'email': 'hackeruser@example.com',
#                'password': 'hello'
#                }
#
#     # testapp.authorization = ('Bearer', token)
#
#     response = testapp.delete('/api/v1/admin/delete/2', json.dumps(user_id), status='4**')
#
#     assert response.status_code == 400


def test_get_all_users(testapp):
    """Test for admin to retrieve all active users"""
    account = {
        'email': 'testUser1@example.com',
        'password': 'hello',
    }

    response = testapp.get('/api/v1/users', json.dumps(account), status='2**')

    assert response.status_code == 200


def test_user_delete_own_account_is_successful(testapp):
    """Test when the user deletes their own account"""
    account = {
        'email': 'testUser1@example.com',
        'password': 'hello',
    }

    token = testapp.post('/api/v1/auth/login', json.dumps(account)).json['token']

    user_id = {'account_id': '1',
               'email': 'testUser1@example.com',
               'password': 'hello'
               }

    testapp.authorization = ('Bearer', token)

    response = testapp.delete('/api/v1/admin/delete/1', json.dumps(user_id), status='2**')

    assert response.status_code == 204









































