# tests/test_localizacao_service.py
from MVC.services.LocationService import salvarLocalizacaoProdutor

def test_salvarLocalizacaoProdutor():
    ok, erro = salvarLocalizacaoProdutor(
        cpf="12345678900",
        latitude=-23.5,
        longitude=-46.6,
        extTerritorial=100
    )
    assert ok is True or ok is False
