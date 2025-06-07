import pytest
import requests

from peptidefeatures.features import (
    seq_length,
    aa_frequency,
    gravy,
    isoelectric_point,
    molecular_formula,
    molecular_weight,
    one_letter_code,
    three_letter_code,
)

# Any function that calls one of these functions is already covered by a test for invalid amino acids.
INVALID_SEQ = "ABC"


@pytest.mark.parametrize(
    "func, seq",
    [
        (seq_length, INVALID_SEQ),
        (aa_frequency, INVALID_SEQ),
        (three_letter_code, INVALID_SEQ),
    ],
)
def test_invalid_amino_acid(func, seq):
    with pytest.raises(ValueError) as e:
        func(seq)
    assert "Invalid amino acid symbol" in str(e.value)


def test_seq_length():
    assert 20 == seq_length("ACDEFGHIKLMNPQRSTVWY")
    assert 50 == seq_length("LHVEDNDEGSPMYMTRCVAWEHITINTNKHYQLYIMWRDGMWYDRMIPAQ")


def test_aa_frequency():
    freq = aa_frequency("AAACCDEEFFF")
    assert {
        "A": 3,
        "C": 2,
        "D": 1,
        "E": 2,
        "F": 3,
        "G": 0,
        "H": 0,
        "I": 0,
        "K": 0,
        "L": 0,
        "M": 0,
        "N": 0,
        "P": 0,
        "Q": 0,
        "R": 0,
        "S": 0,
        "T": 0,
        "V": 0,
        "W": 0,
        "Y": 0,
    } == freq
    assert 20 == len(freq)


def test_molecular_weight():
    assert pytest.approx(799.832) == molecular_weight("PEPTIDE")
    assert pytest.approx(5730, rel=1e-3) == molecular_weight(
        "AGSCCDCILIQNNADMDTDYVCGLVTQMRHGVLEPHILWWAIMWSCHEMI"
    )


def test_three_letter_code():
    assert "ProGluProThrIleAspGlu" == three_letter_code("PEPTIDE")
    assert (
        "LeuTrpTrpTyrPheMetLysProGluLysLeuAlaGlyGluAsnLysGluProLeuGlnMetMetIleHisTyrIleTyrHisValCysCysTrpAsnGluPheGlyCysAspProGlyValGluLysPheArgProGluMetAlaLeu"
        == three_letter_code("LWWYFMKPEKLAGENKEPLQMMIHYIYHVCCWNEFGCDPGVEKFRPEMAL")
    )


def test_one_letter_code():
    assert "PEPTIDE" == one_letter_code("ProGluProThrIleAspGlu")
    assert "YLCSIKSTPPLVFGQVDNVHFCMEIPKSFDVRENSRWVDDALEFVYYQVG" == one_letter_code(
        "TyrLeuCysSerIleLysSerThrProProLeuValPheGlyGlnValAspAsnValHisPheCysMetGluIleProLysSerPheAspValArgGluAsnSerArgTrpValAspAspAlaLeuGluPheValTyrTyrGlnValGly"
    )
    with pytest.raises(ValueError) as e:
        one_letter_code("Pro Glu Pro Thr Ile Asp Glu")
    assert "Invalid input" in str(e.value)
    with pytest.raises(ValueError) as e:
        one_letter_code("PrGluProThrIleAspGlu")
    assert "Invalid three letter code" in str(e.value)


def test_gravy():
    assert pytest.approx(-1.414) == gravy("PEPTIDE")
    assert pytest.approx(-0.744) == gravy(
        "ENFNDTHIIVINCNHVCAECRDTPGWHKCKVPIRMQQMRKWPAESNTRYI"
    )


def test_molecular_formula():
    assert "C5H9NO4" == molecular_formula("E")
    assert "C34H53N7O15" == molecular_formula("PEPTIDE")
    assert "C266H401N69O78S5" == molecular_formula(
        "WQNTDTSMIESSPIGHKDHRTLPTYQWERCWGKSVMELIVCSIWTLYICE"
    )


def test_isoelectric_point():
    assert type(isoelectric_point("PEPTIDE", "kozlowski")) is float
    assert type(isoelectric_point("PEPTIDE", "bjellqvist")) is float
    with pytest.raises(ValueError) as e:
        isoelectric_point("PEPTIDE", "foo")
    assert "Unknown option" in str(e.value)


def test_external_ipc2_availability():
    url = "https://ipc2.mimuw.edu.pl/ipc-2.0.1.zip"
    res = requests.head(url, allow_redirects=True, timeout=5)
    assert 200 == res.status_code
