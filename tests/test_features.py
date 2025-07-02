import pytest
import requests

from constants import TEST_DATA
from pepsi.features import (
    _seq_length,
    _aa_frequency,
    _gravy,
    _isoelectric_point,
    _molecular_formula,
    _molecular_weight,
    _one_letter_code,
    _three_letter_code,
    _compute_features,
    _aromaticity,
    _aa_classification,
)

# Any function that calls one of these functions is already covered by a test for invalid amino acids.
INVALID_SEQ = "ABC"


@pytest.mark.parametrize(
    "func, seq",
    [
        (_seq_length, INVALID_SEQ),
        (_aa_frequency, INVALID_SEQ),
        (_three_letter_code, INVALID_SEQ),
    ],
)
def test_invalid_amino_acid(func, seq):
    with pytest.raises(ValueError) as e:
        func(seq)
    assert "Invalid amino acid symbol" in str(e.value)


def test_seq_length():
    assert 20 == _seq_length("ACDEFGHIKLMNPQRSTVWY")
    assert 50 == _seq_length("LHVEDNDEGSPMYMTRCVAWEHITINTNKHYQLYIMWRDGMWYDRMIPAQ")


def test_aa_frequency():
    freq = _aa_frequency("AAACCDEEFFF")
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
    assert pytest.approx(799.832) == _molecular_weight("PEPTIDE")
    assert pytest.approx(5730, rel=1e-3) == _molecular_weight(
        "AGSCCDCILIQNNADMDTDYVCGLVTQMRHGVLEPHILWWAIMWSCHEMI"
    )


def test_three_letter_code():
    assert "ProGluProThrIleAspGlu" == _three_letter_code("PEPTIDE")
    assert (
        "LeuTrpTrpTyrPheMetLysProGluLysLeuAlaGlyGluAsnLysGluProLeuGlnMetMetIleHisTyrIleTyrHisValCysCysTrpAsnGluPheGlyCysAspProGlyValGluLysPheArgProGluMetAlaLeu"
        == _three_letter_code("LWWYFMKPEKLAGENKEPLQMMIHYIYHVCCWNEFGCDPGVEKFRPEMAL")
    )


def test_one_letter_code():
    assert "PEPTIDE" == _one_letter_code("ProGluProThrIleAspGlu")
    assert "YLCSIKSTPPLVFGQVDNVHFCMEIPKSFDVRENSRWVDDALEFVYYQVG" == _one_letter_code(
        "TyrLeuCysSerIleLysSerThrProProLeuValPheGlyGlnValAspAsnValHisPheCysMetGluIleProLysSerPheAspValArgGluAsnSerArgTrpValAspAspAlaLeuGluPheValTyrTyrGlnValGly"
    )
    with pytest.raises(ValueError) as e:
        _one_letter_code("Pro Glu Pro Thr Ile Asp Glu")
    assert "Invalid input" in str(e.value)
    with pytest.raises(ValueError) as e:
        _one_letter_code("PrGluProThrIleAspGlu")
    assert "Invalid three letter code" in str(e.value)


def test_gravy():
    assert pytest.approx(-1.414) == _gravy("PEPTIDE")
    assert pytest.approx(-0.744) == _gravy(
        "ENFNDTHIIVINCNHVCAECRDTPGWHKCKVPIRMQQMRKWPAESNTRYI"
    )


def test_molecular_formula():
    assert "C5H9NO4" == _molecular_formula("E")
    assert "C34H53N7O15" == _molecular_formula("PEPTIDE")
    assert "C266H401N69O78S5" == _molecular_formula(
        "WQNTDTSMIESSPIGHKDHRTLPTYQWERCWGKSVMELIVCSIWTLYICE"
    )


def test_isoelectric_point():
    # Warning: This method is currently disabled to decrease the project's size.
    # assert type(_isoelectric_point("PEPTIDE", "kozlowski")) is float
    assert type(_isoelectric_point("PEPTIDE", "bjellqvist")) is float
    with pytest.raises(ValueError) as e:
        _isoelectric_point("PEPTIDE", "foo")
    assert "Unknown option" in str(e.value)


def test_external_ipc2_availability():
    url = "https://ipc2.mimuw.edu.pl/ipc-2.0.1.zip"
    res = requests.head(url, allow_redirects=True, timeout=5)
    assert 200 == res.status_code


def test_compute_features():
    options = {
        "three_letter_code": False,
        "molecular_formula": False,
        "seq_length": False,
        "molecular_weight": False,
        "gravy": True,
        "isoelectric_point": False,
        "isoelectric_point_option": "bjellqvist",
        "aromaticity": False,
    }
    res = _compute_features(df=TEST_DATA, params=options)
    assert "GRAVY" in res.columns
    assert "Molecular weight" not in res.columns
    res_grouped = res.groupby("Sequence")["GRAVY"].nunique()
    assert (res_grouped <= 1).all()


def test_aromaticity():
    assert pytest.approx(0.0) == _aromaticity("PEPTIDE")
    assert pytest.approx(0.08) == _aromaticity(
        "PKMMDHQPIKTYWCMIGKPNREEIEIAKKMMAEMTDNDWPLHQMPFCSKL"
    )


def test_aa_classification():
    assert {
        "Aliphatic": 7,
        "Sulfur": 4,
        "Hydroxyl": 9,
        "Basic": 6,
        "Acidic": 2,
        "Amide": 4,
        "Other": 18,
    } == _aa_classification(
        "FIHIPNAWWGADCWCRTWRMQPKSWVFFSQTGAWTFPCPESIKTKTSWNP", "chemical"
    )
    assert {
        "Non-polar": 29,
        "Uncharged": 13,
        "Charged": 8,
    } == _aa_classification(
        "FIHIPNAWWGADCWCRTWRMQPKSWVFFSQTGAWTFPCPESIKTKTSWNP", "charge"
    )
    with pytest.raises(ValueError) as e:
        _aa_classification("PEPTIDE", "foo")
    assert "Unknown option" in str(e.value)
