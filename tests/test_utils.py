from peptidefeatures.utils import sanitize_seq, get_group


def test_sanitize_seq():
    assert "PEPTIDE" == sanitize_seq("pEPtiDe :)")


def test_get_group():
    groups = ["AD", "CTR"]
    assert "AD" == get_group("AD01_C1_INSOLUBLE_01", groups)
    assert "None" == get_group(":)", groups)
