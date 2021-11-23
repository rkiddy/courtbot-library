
import os
import courtbot

def test_has_properties():

    court = courtbot.get_state("CA")

    assert court.courts

def test_get_list():

    court = courtbot.get_state("CA")

    result = court.get_list('Santa Clara', '2021-09-23', 0)

    assert len(result) > 0

def test_get_empty_list():

    court = courtbot.get_state("CA")

    result = court.get_list('Sonoma', '2021-09-23', 0)

    assert len(result) == 0

def test_get_case():

    court = courtbot.get_state("CA")

    result = court.get_case('Santa Clara', '2021-09-23', 'C1918672')

    assert result['caseName'] == 'The People of the State of California\nvs.\nPEREZ, JOSE SOLEDAD'

def test_fetch():

    court = courtbot.get_state("CA")

    if os.path.exists("data/CA/Santa Clara/2021-09-24.json"):
       os.remove("data/CA/Santa Clara/2021-09-24.json")

    assert os.path.exists("data/CA/Santa Clara/2021-09-24.json") == False

    court.get_list('Santa Clara', '2021-09-24', 1)

    assert os.path.exists("data/CA/Santa Clara/2021-09-24.json") == True

