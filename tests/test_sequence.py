from peptidefeatures.features.sequence import aa_number, aa_frequency

def test_aa_number():
    assert aa_number("ACDEFGHIKLMNPQRSTVWY") == 20

def test_aa_frequency():
    freq = aa_frequency("AAACCDEEFFF")
    assert freq == {'A': 3, 'C': 2, 'D': 1, 'E': 2, 'F': 3, 'G': 0, 'H': 0, 'I': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'V': 0, 'W': 0, 'Y': 0}
    assert len(freq) == 20