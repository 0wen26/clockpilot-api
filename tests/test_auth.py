def test_login_success(client, test_user):
    response = client.post(
        "/api/auth/login",  # Añade el prefijo /api/auth
        data={"username": "test@example.com", "password": "123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_fail(client, test_user):
    # Contraseña incorrecta
    response = client.post(
        "/api/auth/login",  # Añade el prefijo /api/auth
        data={"username": "test@example.com", "password": "wrong"}
    )
    assert response.status_code == 401

    # Usuario no existe
    response = client.post(
        "/api/auth/login",  # Añade el prefijo /api/auth
        data={"username": "nonexistent@example.com", "password": "123"}
    )
    assert response.status_code == 401