from src.features.sequence import aa_number

def test_aa_number():
    assert aa_number("ACDEFGHIKLMNPQRSTVWY") == 20