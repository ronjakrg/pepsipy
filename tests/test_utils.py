from peptidefeatures.utils import sanitize_sequence, get_group

def test_sanitize_sequence():
    assert "PEPTIDE" == sanitize_sequence("pEPtiDe :)")


def test_get_group():
    groups = ["AD", "CTR"]
    assert "AD" == get_group("AD01_C1_INSOLUBLE_01", groups)
    assert "None" == get_group(":)", groups)