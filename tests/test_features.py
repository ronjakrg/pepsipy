import pytest
from peptidefeatures.features import aa_number, aa_frequency, three_letter_code, gravy, molecular_formula, molecular_weight

# Any function that calls one of these functions is already covered by a test for invalid amino acids.
INVALID_SEQ = "ABC"
@pytest.mark.parametrize("func, seq", [
    (aa_number, INVALID_SEQ),
    (aa_frequency, INVALID_SEQ),
    (three_letter_code, INVALID_SEQ),
])

def test_invalid_amino_acid(func, seq):
    with pytest.raises(ValueError) as e:
        func(seq)
    assert "Invalid amino acid symbol" in str(e.value)

def test_aa_number():
    assert 20 == aa_number("ACDEFGHIKLMNPQRSTVWY")
    assert 50 == aa_number("LHVEDNDEGSPMYMTRCVAWEHITINTNKHYQLYIMWRDGMWYDRMIPAQ")

def test_aa_frequency():
    freq = aa_frequency("AAACCDEEFFF")
    assert {'A': 3, 'C': 2, 'D': 1, 'E': 2, 'F': 3, 'G': 0, 'H': 0, 'I': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'V': 0, 'W': 0, 'Y': 0} == freq
    assert 20 == len(freq)
    
def test_molecular_weight():
    assert pytest.approx(799.832) == molecular_weight("PEPTIDE")
    assert pytest.approx(5730, rel=1e-3) == molecular_weight("AGSCCDCILIQNNADMDTDYVCGLVTQMRHGVLEPHILWWAIMWSCHEMI")

def test_three_letter_code():
    assert "ProGluProThrIleAspGlu" == three_letter_code("PEPTIDE")
    assert "LeuTrpTrpTyrPheMetLysProGluLysLeuAlaGlyGluAsnLysGluProLeuGlnMetMetIleHisTyrIleTyrHisValCysCysTrpAsnGluPheGlyCysAspProGlyValGluLysPheArgProGluMetAlaLeu" == three_letter_code("LWWYFMKPEKLAGENKEPLQMMIHYIYHVCCWNEFGCDPGVEKFRPEMAL")

def test_gravy():
    assert pytest.approx(-1.414) == gravy("PEPTIDE")
    assert pytest.approx(-0.744) == gravy("ENFNDTHIIVINCNHVCAECRDTPGWHKCKVPIRMQQMRKWPAESNTRYI")

def test_molecular_formula():
    assert "C34H53N7O15" == molecular_formula("PEPTIDE")
    assert "C266H401N69O78S5" == molecular_formula("WQNTDTSMIESSPIGHKDHRTLPTYQWERCWGKSVMELIVCSIWTLYICE")
