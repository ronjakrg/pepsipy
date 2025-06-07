import pandas as pd

from peptidefeatures.utils import sanitize_seq, get_group, get_distinct_seq


def test_sanitize_seq():
    assert "PEPTIDE" == sanitize_seq("pEPtiDe :)")


def test_get_group():
    groups = ["AD", "CTR"]
    assert "AD" == get_group("AD01_C1_INSOLUBLE_01", groups)
    assert "None" == get_group(":)", groups)


def test_get_distinct_seq():
    data = {
        "Sample": [
            "AD01_C1_INSOLUBLE_01",
            "CTR01_C1_INSOLUBLE_01",
            "CTR01_C1_INSOLUBLE_01",
        ],
        "Protein ID": ["A0A075B6S2", "A0A075B6R2", "A0A075B6R2"],
        "Sequence": ["FSGVPDR", "VTISVDK", "VTISVDK"],
        "Intensity": [936840, 33411000, 33411000],
        "PEP": [0.0068633, 0.057623, 0.057623],
    }
    df = pd.DataFrame(data)
    assert get_distinct_seq(df).equals(
        pd.DataFrame({"Sequence": ["FSGVPDR", "VTISVDK"]})
    )
