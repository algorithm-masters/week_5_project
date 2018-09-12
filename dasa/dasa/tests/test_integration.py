import json


# def test_home_route_successful(testapp):
#     """Test Home route exists"""
#     import pdb;pdb.set_trace()
#     response = testapp.head(headers=200)
#
#     assert response.status_code == 200


def test_registration(testapp):
    """Test registration for one user."""
    account = {
        'email': 'test1@example.com',
        'password': 'hello',
    }

    response = testapp.post(
        '/api/v1/auth/register',
        json.dumps(account)
    )

    # import pdb; pdb.set_trace()
    assert response.status_code == 201
    assert response.json['token']


def test_invalid_registration(testapp):
    """Test failed registration."""
    account = {
        'email': 'test_two@example.com',
    }

    response = testapp.post(
        '/api/v1/auth/register',
        json.dumps(account),
        status='4**'
    )
    assert response.status_code == 400
    # import pdb; pdb.set_trace()


def test_login(testapp):
    """Test login successful."""
    account = {
        'email': 'test1@example.com',
        'password': 'hello',
    }

    response = testapp.post(
        '/api/v1/auth/login',
        json.dumps(account)
    )
    assert response.status_code == 201
    assert response.json['token']


def test_duplicate_login(testapp):
    """Test login with duplicate keys."""
    account = {
        'email': 'test1@example.com',
        'password': 'hello',
    }

    response = testapp.post(
        '/api/v1/auth/login',
        json.dumps(account)
    )
    assert response.status_code == 409
    assert response.json['token']






# def test_stocks_lookup(testapp):
#     """Test stock lookup is successful."""
#     response = testapp.get('/api/v1/lookup/aapl')
#     assert response.status_code == 200
#     # assert response.json[''] == ''
#
#
# def test_invalid_lookup_methods(testapp):
#     """Test invalid stook lookup failed"""
#     response = testapp.get('/api/v1/lookup/aapl', status='4**')
#     assert response.status_code == 405
#     response = testapp.delete('/api/v1/lookup/aapl', status='4**')
#     assert response.status_code == 405
#     response = testapp.post('/api/v1/lookup/aapl', status='4**')
#     assert response.status_code == 405