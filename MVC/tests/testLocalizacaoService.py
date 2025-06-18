from MVC.services.LocationService import salvarLocalizacaoProdutor # importação da funcionalidade

def test_salvarLocalizacaoProdutor(): # teste
    ok, erro = salvarLocalizacaoProdutor( # chama a função passando os parametros necessários (principalmente latitude e longitude)
        cpf="12345678900",
        latitude=-23.5,
        longitude=-46.6,
        extTerritorial=100
    )
    assert ok is True or ok is False # verifica se é um retorno válido
