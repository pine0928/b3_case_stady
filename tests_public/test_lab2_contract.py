from labs.lab2_burst import starter

def test_lab2_api_is_present():
    assert callable(starter.direction_only_bursts)
    assert callable(starter.alternative_bursts)
