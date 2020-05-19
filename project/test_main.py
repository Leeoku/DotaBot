import pytest
from heroes import heroes
from main import is_valid_hero

@pytest.mark.parametrize("hero_name, expected", [
    ("JET", False),
    ("1", False),
    ("techies", True),
    ("legion commander", True),
    #("", False)
])
def test_valid_hero(hero_name, expected):
    assert is_valid_hero(hero_name) is expected