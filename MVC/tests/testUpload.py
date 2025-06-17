def test_upload_sem_login(client): # teste
    response = client.post('/upload') # ação: tentar entrar na página de upload
    assert response.status_code == 403  # verificação: verificar se o usuário consegue realizar o upload sem o login
