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
    _charge_at_ph,
    _charge_density,
    _boman_index,
    _aliphatic_index,
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
    # Benchmark values from ExPASy (Gasteiger et al., 2005)
    assert 20 == _seq_length("ACDEFGHIKLMNPQRSTVWY")
    assert 50 == _seq_length("LHVEDNDEGSPMYMTRCVAWEHITINTNKHYQLYIMWRDGMWYDRMIPAQ")


def test_aa_frequency():
    # Benchmark values from ExPASy (Gasteiger et al., 2005)
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
    # Benchmark values from ExPASy (Gasteiger et al., 2005)
    assert pytest.approx(799.83) == _molecular_weight("PEPTIDE")
    assert pytest.approx(5724.67, rel=1e-3) == _molecular_weight(
        "AGSCCDCILIQNNADMDTDYVCGLVTQMRHGVLEPHILWWAIMWSCHEMI"
    )


def test_three_letter_code():
    # Benchmark values from Sequence Manipulation Suite (Stothard, 2000)
    assert "ProGluProThrIleAspGlu" == _three_letter_code("PEPTIDE")
    assert (
        "LeuTrpTrpTyrPheMetLysProGluLysLeuAlaGlyGluAsnLysGluProLeuGlnMetMetIleHisTyrIleTyrHisValCysCysTrpAsnGluPheGlyCysAspProGlyValGluLysPheArgProGluMetAlaLeu"
        == _three_letter_code("LWWYFMKPEKLAGENKEPLQMMIHYIYHVCCWNEFGCDPGVEKFRPEMAL")
    )


def test_one_letter_code():
    # Benchmark values from Sequence Manipulation Suite (Stothard, 2000)
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
    # Benchmark values from ExPASy (Gasteiger et al., 2005)
    assert pytest.approx(-1.414) == _gravy("PEPTIDE")
    assert pytest.approx(-0.744) == _gravy(
        "ENFNDTHIIVINCNHVCAECRDTPGWHKCKVPIRMQQMRKWPAESNTRYI"
    )


def test_molecular_formula():
    # Benchmark value from Nomenclature and symbolism for amino acids and peptides (IUPAC et al., 1984)
    assert "C5H9NO4" == _molecular_formula("E")
    # Benchmark values from ExPASy (Gasteiger et al., 2005)
    assert "C34H53N7O15" == _molecular_formula("PEPTIDE")
    assert "C266H401N69O78S5" == _molecular_formula(
        "WQNTDTSMIESSPIGHKDHRTLPTYQWERCWGKSVMELIVCSIWTLYICE"
    )


def test_isoelectric_point():
    assert type(_isoelectric_point("PEPTIDE", "kozlowski")) is float
    assert type(_isoelectric_point("PEPTIDE", "bjellqvist")) is float
    with pytest.raises(ValueError) as e:
        _isoelectric_point("PEPTIDE", "foo")
    assert "Unknown option" in str(e.value)


def test_compute_features():
    params = {"gravy": True}
    res = _compute_features(df=TEST_DATA, params=params)
    assert "GRAVY" in res.columns
    assert "Molecular weight" not in res.columns
    res_grouped = res.groupby("Sequence")["GRAVY"].nunique()
    assert (res_grouped <= 1).all()


def test_aromaticity():
    # Benchmark values from Sequence Manipulation Suite (Stothard, 2000)
    assert pytest.approx(0.0) == _aromaticity("PEPTIDE")
    assert pytest.approx(0.08) == _aromaticity(
        "PKMMDHQPIKTYWCMIGKPNREEIEIAKKMMAEMTDNDWPLHQMPFCSKL"
    )


def test_aa_classification():
    # Benchmark values from (Pommié et al., 2004)
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


def test_charge_at_ph():
    assert type(_charge_at_ph("PEPTIDE", 7.0)) is float


def test_charge_density():
    # Benchmark values from modlAMP (Müller et al., 2017)
    assert pytest.approx(-0.00375, abs=1e-5) == _charge_density("PEPTIDE", 7.0)
    assert pytest.approx(0.00036, abs=1e-5) == _charge_density(
        "LWSKKWMGGTQDRDVACGHFGKMWILEDTQLGSEKGLSSNTRSYRYQQHP", 7.0
    )


def test_boman_index():
    assert type(_boman_index("PEPTIDE")) is float


def test_aliphatic_index():
    # Benchmark values from ExPASy (Gasteiger et al., 2005)
    assert pytest.approx(55.71) == _aliphatic_index("PEPTIDE")
    assert pytest.approx(70.20) == _aliphatic_index(
        "DPTWFWLEFSLYEERSMDGAPGDGLYFQDDMLDFCLKQKINIVWHRYLKY"
    )
