def test_upload_sem_login(client):
    response = client.post('/upload')
    assert response.status_code == 403  # Deve bloquear sem estar logado
