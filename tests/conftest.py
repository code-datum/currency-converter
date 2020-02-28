import pytest


@pytest.fixture
def supply():
    aa = 54
    bb = 34
    return [aa, bb]


@pytest.fixture
def supply_url():
    return "https://reqres.in/api"
