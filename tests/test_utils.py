from peptidefeatures.utils import sanitize_sequence

def test_sanitize_sequence():
    assert "PEPTIDE" == sanitize_sequence("pEPtiDe :)")