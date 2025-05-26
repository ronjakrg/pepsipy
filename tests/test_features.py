from peptidefeatures.features import aa_number, aa_frequency, three_letter_code, molecular_weight


def test_aa_number():
    assert aa_number("ACDEFGHIKLMNPQRSTVWY") == 20

def test_aa_frequency():
    freq = aa_frequency("AAACCDEEFFF")
    assert freq == {'A': 3, 'C': 2, 'D': 1, 'E': 2, 'F': 3, 'G': 0, 'H': 0, 'I': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'V': 0, 'W': 0, 'Y': 0}
    assert len(freq) == 20
    
def test_molecular_weight():
    assert 799.832 == molecular_weight("PEPTIDE")

def test_three_letter_code():
    assert "ProGluProThrIleAspGlu" == three_letter_code("PEPTIDE")
